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



sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from inference import InferenceEngine, detect_script_cluster
from clusters import all_clusters
from data_loader import ID2LABEL

# ── Global model cache ────────────────────────────────────────────────────────
_ENGINE = None

def _load_model():
    global _ENGINE
    if _ENGINE is not None:
        return

    print("[SFA-CA] Loading Inference Engine...")
    _ENGINE = InferenceEngine()
    _ENGINE.load_from_dir()
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
    return {"status": "ok", "model_loaded": _ENGINE is not None}


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(req: AnalyzeRequest):
    if _ENGINE is None:
        raise HTTPException(status_code=503, detail="Model not loaded yet.")

    if not req.text or len(req.text.strip()) < 10:
        raise HTTPException(status_code=400, detail="Text too short (min 10 chars).")

    sanitized, had_math = _sanitize(req.text)
    cluster = detect_script_cluster(sanitized)

    try:
        result = _ENGINE.predict(sanitized, cluster)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    prob_dict = result["probabilities"]
    human_prob = result["human"]
    ai_prob = result["ai"]
    top_gen = result["generator"]

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
