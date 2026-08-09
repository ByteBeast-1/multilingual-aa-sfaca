"""
api.py
------
FastAPI backend for SFA-CA Multilingual AI Attribution System.
Deploy to Hugging Face Spaces (FastAPI SDK).
"""

from __future__ import annotations

import os
import sys
import re
from typing import Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import torch
import torch.nn.functional as F
import uvicorn

# ── PEFT torchao compatibility patch ─────────────────────────────────────────
# Replace dispatch_torchao directly (avoids recursive is_torchao_available wrapping)
try:
    import peft.tuners.lora.torchao as _lora_torchao
    _lora_torchao.dispatch_torchao = lambda *a, **kw: None
except Exception:
    pass
# ─────────────────────────────────────────────────────────────────────────────

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from model import SFACAModel, build_tokenizer, NUM_CLASSES
from clusters import get_cluster, all_clusters
from data_loader import ID2LABEL

# ── Global model cache ────────────────────────────────────────────────────────
_MODEL = None
_TOKENIZER = None
_DEVICE = None


def _load_model():
    global _MODEL, _TOKENIZER, _DEVICE
    if _MODEL is not None:
        return

    _DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"[SFA-CA] Loading model on {_DEVICE}...")

    _TOKENIZER = build_tokenizer()
    _MODEL = SFACAModel(clusters=all_clusters()).to(_DEVICE)

    adapters_dir = os.path.join(os.path.dirname(__file__), "..", "results", "adapters")
    if os.path.exists(adapters_dir):
        from peft import set_peft_model_state_dict
        for cluster in all_clusters():
            adapter_file = os.path.join(adapters_dir, cluster, "adapter_model.bin")
            classifier_file = os.path.join(adapters_dir, cluster, "classifier.pt")
            if os.path.exists(adapter_file):
                try:
                    weights = torch.load(adapter_file, map_location=_DEVICE)
                    set_peft_model_state_dict(_MODEL.backbone, weights, adapter_name=cluster)
                    if os.path.exists(classifier_file):
                        _MODEL.classifier.load_state_dict(
                            torch.load(classifier_file, map_location=_DEVICE)
                        )
                    print(f"  ✓ Loaded adapter: {cluster}")
                except Exception as e:
                    print(f"  ! Adapter {cluster} load failed: {e}")

    _MODEL.eval()
    print("[SFA-CA] Model ready.")


@asynccontextmanager
async def lifespan(app: FastAPI):
    _load_model()
    yield


# ── FastAPI app ───────────────────────────────────────────────────────────────
app = FastAPI(
    title="SFA-CA Multilingual AI Attribution API",
    description="Script-Family-Aware Contrastive Adaptation for Multi-LLM Detection",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # Allow GitHub Pages and all origins
    allow_credentials=False,      # Must be False when allow_origins is ["*"] for browser CORS compliance
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Request / Response models ─────────────────────────────────────────────────
class AnalyzeRequest(BaseModel):
    text: str
    max_length: int = 256


class AnalyzeResponse(BaseModel):
    verdict: str                          # "AI-Generated" or "Human-Written"
    confidence: float                     # 0–1
    ai_probability: float
    human_probability: float
    top_generator: str
    top_generator_confidence: float
    script_cluster: str
    probabilities: dict[str, float]       # {label: probability}
    sanitized_text_preview: str


# ── Helpers ───────────────────────────────────────────────────────────────────
_MATH_PATTERN = re.compile(
    r"(\$\$[\s\S]+?\$\$|\$[^$\n]+?\$|\\begin\{[^}]+\}[\s\S]+?\\end\{[^}]+\})"
)

def _detect_script_cluster(text: str) -> str:
    cyrillic = len(re.findall(r"[\u0400-\u04FF]", text))
    greek    = len(re.findall(r"[\u0370-\u03FF]", text))
    arabic   = len(re.findall(r"[\u0600-\u06FF]", text))
    hanzi    = len(re.findall(r"[\u4E00-\u9FFF]", text))
    latin    = len(re.findall(r"[a-zA-Z]", text))

    counts = {
        "cyrillic": cyrillic,
        "greek": greek,
        "arabic": arabic,
        "hanzi": hanzi,
        "latin": latin
    }

    best = max(counts, key=counts.get)
    return best if counts[best] > 0 else "latin"


def _sanitize(text: str) -> tuple[str, bool]:
    cleaned, n = _MATH_PATTERN.subn(" [MATH] ", text)
    return cleaned.strip(), n > 0


# ── Endpoints ─────────────────────────────────────────────────────────────────
@app.get("/")
def root():
    return {
        "status": "online",
        "model": "SFA-CA v1.0",
        "classes": list(ID2LABEL.values()),
        "clusters": all_clusters(),
    }


@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": _MODEL is not None}


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(req: AnalyzeRequest):
    if _MODEL is None:
        raise HTTPException(status_code=503, detail="Model not loaded yet.")

    if not req.text or len(req.text.strip()) < 10:
        raise HTTPException(status_code=400, detail="Text too short (min 10 chars).")

    sanitized, had_math = _sanitize(req.text)
    cluster = _detect_script_cluster(sanitized)

    enc = _TOKENIZER(
        sanitized,
        return_tensors="pt",
        max_length=req.max_length,
        truncation=True,
        padding=True,
    ).to(_DEVICE)

    with torch.no_grad():
        logits = _MODEL(enc["input_ids"], enc["attention_mask"], cluster)
        probs = F.softmax(logits, dim=-1).squeeze().cpu().tolist()

    # Build label → probability dict
    prob_dict = {ID2LABEL[i]: round(float(p), 4) for i, p in enumerate(probs)}

    human_prob = prob_dict.get("human", 0.0)
    ai_prob = round(1.0 - human_prob, 4)

    # Top non-human generator
    ai_probs = {k: v for k, v in prob_dict.items() if k != "human"}
    top_gen = max(ai_probs, key=ai_probs.get)

    verdict = "Human-Written" if human_prob >= 0.5 else "AI-Generated"
    confidence = human_prob if verdict == "Human-Written" else ai_prob

    return AnalyzeResponse(
        verdict=verdict,
        confidence=round(confidence, 4),
        ai_probability=ai_prob,
        human_probability=round(human_prob, 4),
        top_generator=top_gen,
        top_generator_confidence=round(ai_probs[top_gen], 4),
        script_cluster=cluster,
        probabilities=prob_dict,
        sanitized_text_preview=sanitized[:300],
    )


if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=7860, reload=False)
