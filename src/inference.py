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

def detect_script(text: str) -> dict:
    if not text:
        return {"cluster": "latin", "counts": {}, "routing_confidence": 0.0, "mixed": False, "supported": False}

    # Unicode-block based counts, ignoring digits, punctuation, etc.
    cyrillic = len(re.findall(r"[\u0400-\u04FF\u0500-\u052F]", text))
    greek = len(re.findall(r"[\u0370-\u03FF\u1F00-\u1FFF]", text))
    arabic = len(re.findall(r"[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF]", text))
    hanzi = len(re.findall(r"[\u4E00-\u9FFF]", text))
    kana = len(re.findall(r"[\u3040-\u309F\u30A0-\u30FF]", text))
    latin = len(re.findall(r"[\u0041-\u005A\u0061-\u007A\u00C0-\u024F\u1E00-\u1EFF]", text))
    hangul = len(re.findall(r"[\uAC00-\uD7AF\u1100-\u11FF]", text))
    hebrew = len(re.findall(r"[\u0590-\u05FF]", text))
    devanagari = len(re.findall(r"[\u0900-\u097F]", text))

    counts = {
        "cyrillic": cyrillic,
        "greek": greek,
        "arabic": arabic,
        "hanzi": hanzi + kana + hangul,  # Map Japanese/Korean to nearest cluster (Hanzi)
        "latin": latin,
        "unsupported": hebrew + devanagari
    }

    # Filter out empty clusters
    active_counts = {k: v for k, v in counts.items() if v > 0}
    total = sum(active_counts.values())
    
    if total == 0:
        return {"cluster": "latin", "counts": {}, "routing_confidence": 0.0, "mixed": False, "supported": False}

    best = max(counts, key=counts.get)
    supported = (best != "unsupported")
    routing_confidence = counts[best] / total
    mixed = len([c for c, v in active_counts.items() if c != "unsupported"]) > 1
    
    if not supported:
        best = "latin"
        
    return {
        "cluster": best,
        "counts": active_counts,
        "routing_confidence": round(routing_confidence, 4),
        "mixed": mixed,
        "supported": supported
    }

def detect_script_cluster(text: str) -> str:
    """
    Wrapper for detect_script that returns only the cluster string.
    """
    return detect_script(text)["cluster"]


class InferenceEngine:
    def __init__(self, config=None, tokenizer=None, model=None, classifiers=None, device=None):
        if config is None:
            config_path = os.path.join(os.path.dirname(__file__), "..", "configs", "default.yaml")
            with open(config_path, "r") as f:
                self.config = yaml.safe_load(f)
        else:
            self.config = config
            
        self.max_length = self.config.get("max_length", 128)
        self.device = device if device is not None else torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.clusters = all_clusters()
        
        self.tokenizer = tokenizer
        self.model = model
        self.classifiers = classifiers if classifiers is not None else nn.ModuleDict()

    def load_from_dir(self, adapter_dir=None):
        if adapter_dir is None:
            adapter_dir = os.environ.get("ADAPTER_DIR")
        if not adapter_dir:
            raise ValueError("ADAPTER_DIR environment variable must be set to load models.")
            
        self.tokenizer = build_tokenizer(self.config.get("backbone", "xlm-roberta-large"))
        self.model = SFACAModel(
            backbone_name=self.config.get("backbone", "xlm-roberta-large"),
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
                head.eval()
                self.classifiers[cluster] = head
            else:
                print(f"Warning: Missing classifier head for '{cluster}' at {head_path}")
                
        self.model.to(self.device)
        self.model.eval()

    def predict(self, text: str, cluster: str):
        if self.model is None or self.tokenizer is None:
             raise RuntimeError("Model and tokenizer not loaded. Call load_from_dir() first or provide them.")

        if cluster not in self.classifiers:
            raise ValueError(f"No classifier head loaded for cluster '{cluster}'.")

        enc = self.tokenizer(
            text,
            return_tensors="pt",
            max_length=self.max_length,
            truncation=True,
            padding=True,
        )
        if hasattr(enc, "to"):
            enc = enc.to(self.device)
        else:
            enc = {k: v.to(self.device) if hasattr(v, "to") else v for k, v in enc.items()}

        with torch.no_grad():
            self.model.set_active_cluster(cluster)
            outputs = self.model.backbone(input_ids=enc["input_ids"], attention_mask=enc["attention_mask"])
            pooled = outputs.last_hidden_state[:, 0, :]
            
            logits = self.classifiers[cluster](pooled)
            probs = torch.nn.functional.softmax(logits, dim=-1).squeeze().cpu().tolist()
            # If batch size was 1, probs is a list. But if we passed single text, it's 1D.
            if isinstance(probs, float):  # Fallback for 1-class
                probs = [probs]

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
            "probabilities": prob_dict,
            "logits": logits.squeeze().cpu().tolist()
        }
