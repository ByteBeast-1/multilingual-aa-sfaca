import os
import sys
import yaml
import re
import torch
import torch.nn as nn

import compat

from model import SFACAModel, build_tokenizer
from clusters import all_clusters
from data_loader import ID2LABEL

def detect_script_cluster(text: str) -> str:
    """
    Detects script family cluster by inspecting Unicode ranges of characters.
    Handles Japanese kana and Persian/Urdu explicitly.
    """
    if not text:
        return "latin"

    # Unicode-block based counts, ignoring digits, punctuation, etc.
    cyrillic = len(re.findall(r"[\u0400-\u04FF\u0500-\u052F]", text))
    greek = len(re.findall(r"[\u0370-\u03FF\u1F00-\u1FFF]", text))
    arabic = len(re.findall(r"[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF]", text))
    hanzi = len(re.findall(r"[\u4E00-\u9FFF]", text))
    kana = len(re.findall(r"[\u3040-\u309F\u30A0-\u30FF]", text))
    latin = len(re.findall(r"[\u0041-\u005A\u0061-\u007A\u00C0-\u024F\u1E00-\u1EFF]", text))

    counts = {
        "cyrillic": cyrillic,
        "greek": greek,
        "arabic": arabic,
        "hanzi": hanzi + kana,  # Map Japanese kana to nearest cluster (Hanzi)
        "latin": latin
    }

    best = max(counts, key=counts.get)
    return best if counts[best] > 0 else "latin"

class InferenceEngine:
    def __init__(self, use_stub=False):
        config_path = os.path.join(os.path.dirname(__file__), "..", "configs", "default.yaml")
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)
            
        self.max_length = self.config.get("max_length", 128)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.clusters = all_clusters()
        self.use_stub = use_stub
        
        self.tokenizer = None
        self.backbone = None
        self.classifiers = nn.ModuleDict()
        
        if not self.use_stub:
            self._load_model()

    def _load_model(self):
        adapter_dir = os.environ.get("ADAPTER_DIR")
        if not adapter_dir:
            raise ValueError("ADAPTER_DIR environment variable must be set to load models.")
            
        self.tokenizer = build_tokenizer(self.config["backbone"])
        self.model = SFACAModel(
            backbone_name=self.config["backbone"],
            num_classes=len(ID2LABEL),
            clusters=self.clusters
        )
        
        # Load adapters and heads
        for cluster in self.clusters:
            adapter_path = os.path.join(adapter_dir, cluster)
            head_path = os.path.join(adapter_path, "classifier_head.pt")
            
            if not os.path.exists(adapter_path):
                print(f"Warning: Adapter missing for cluster '{cluster}' at {adapter_path}")
                continue
                
            self.model.backbone.load_adapter(adapter_path, adapter_name=cluster)
            
            if os.path.exists(head_path):
                head_state = torch.load(head_path, map_location=self.device)
                
                # Clone the base classifier structure
                head = nn.Sequential(
                    nn.Linear(self.model.classifier[0].in_features, self.model.classifier[0].out_features),
                    nn.GELU(),
                    nn.Dropout(0.1),
                    nn.Linear(self.model.classifier[3].in_features, self.model.classifier[3].out_features)
                )
                head.load_state_dict(head_state)
                self.classifiers[cluster] = head
            else:
                print(f"Warning: Missing classifier head for '{cluster}' at {head_path}")
                
        self.model.to(self.device)
        self.model.eval()

    def predict(self, text: str, cluster: str):
        if self.use_stub:
            # Deterministic stub output for testing
            import hashlib
            h = int(hashlib.md5(text.encode()).hexdigest(), 16)
            human_prob = (h % 100) / 100.0
            return {"human": human_prob, "ai": 1.0 - human_prob, "generator": "Stub-LLM", "generator_prob": 1.0 - human_prob}

        if cluster not in self.classifiers:
            raise ValueError(f"No classifier head loaded for cluster '{cluster}'.")

        enc = self.tokenizer(
            text,
            return_tensors="pt",
            max_length=self.max_length,
            truncation=True,
            padding=True,
        ).to(self.device)

        with torch.no_grad():
            self.model.set_active_cluster(cluster)
            outputs = self.model.backbone(input_ids=enc["input_ids"], attention_mask=enc["attention_mask"])
            pooled = outputs.last_hidden_state[:, 0, :]
            
            # Use the cluster-specific head!
            logits = self.classifiers[cluster](pooled)
            probs = torch.nn.functional.softmax(logits, dim=-1).squeeze().cpu().tolist()

        prob_dict = {ID2LABEL[i]: round(float(p), 4) for i, p in enumerate(probs)}
        human_prob = prob_dict.get("human", 0.0)
        ai_prob = round(1.0 - human_prob, 4)

        ai_probs = {k: v for k, v in prob_dict.items() if k != "human"}
        top_gen = max(ai_probs, key=ai_probs.get) if ai_probs else "Unknown"
        top_gen_prob = ai_probs.get(top_gen, 0.0)

        return {
            "human": human_prob,
            "ai": ai_prob,
            "generator": top_gen,
            "generator_prob": round(top_gen_prob, 4),
            "probabilities": prob_dict
        }
