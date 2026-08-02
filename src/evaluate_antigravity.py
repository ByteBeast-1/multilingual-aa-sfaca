import argparse
import os
import yaml
import torch
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, f1_score, classification_report, confusion_matrix
from transformers import AutoTokenizer

from clusters import ScriptClusterManager
from data_loader import get_dataloaders
from model import SFACAModel

def parse_args():
    parser = argparse.ArgumentParser(description="Evaluate Multilingual AA SFACA Model")
    parser.add_argument("--config", type=str, default="configs/default_config.yaml", help="Path to config YAML")
    parser.add_argument("--model_path", type=str, default="results/checkpoints/sfaca_model.pt", help="Path to saved model checkpoint")
    return parser.parse_args()

def main():
    args = parse_args()

    with open(args.config, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    cluster_manager = ScriptClusterManager(config["data"]["cluster_mapping_path"])
    backbone_name = config["model"]["backbone"]
    tokenizer = AutoTokenizer.from_pretrained(backbone_name)

    dataloaders = get_dataloaders(
        raw_dir=config["data"]["raw_data_dir"],
        low_resource_dir=config["data"]["low_resource_dir"],
        tokenizer=tokenizer,
        cluster_manager=cluster_manager,
        batch_size=config["data"]["eval_batch_size"],
        max_seq_length=config["data"]["max_seq_length"]
    )

    model = SFACAModel(
        backbone_name=backbone_name,
        num_authors=10,
        use_lora=config["model"]["use_lora"],
        lora_r=config["model"]["lora_r"],
        lora_alpha=config["model"]["lora_alpha"],
        lora_dropout=config["model"]["lora_dropout"],
        target_modules=config["model"]["target_modules"]
    ).to(device)

    if os.path.exists(args.model_path):
        model.load_state_dict(torch.load(args.model_path, map_location=device))
        print(f"Loaded weights from {args.model_path}")
    else:
        print(f"Warning: Model checkpoint not found at {args.model_path}. Running with initialized weights.")

    model.eval()
    all_preds = []
    all_targets = []
    all_clusters = []

    with torch.no_grad():
        for batch in dataloaders["val"]:
            input_ids = batch["input_ids"].to(device)
            attention_mask = batch["attention_mask"].to(device)
            author_ids = batch["author_id"].to(device)
            cluster_ids = batch["cluster_id"].to(device)

            outputs = model(input_ids=input_ids, attention_mask=attention_mask)
            logits = outputs["logits"]
            preds = torch.argmax(logits, dim=1)

            all_preds.extend(preds.cpu().numpy())
            all_targets.extend(author_ids.cpu().numpy())
            all_clusters.extend(cluster_ids.cpu().numpy())

    acc = accuracy_score(all_targets, all_preds)
    f1_macro = f1_score(all_targets, all_preds, average="macro", zero_division=0)
    f1_weighted = f1_score(all_targets, all_preds, average="weighted", zero_division=0)

    print(f"\n--- Evaluation Results ---")
    print(f"Accuracy:    {acc:.4f}")
    print(f"F1 Macro:    {f1_macro:.4f}")
    print(f"F1 Weighted: {f1_weighted:.4f}")

    results_dir = config["evaluation"]["results_dir"]
    os.makedirs(results_dir, exist_ok=True)

    metrics_df = pd.DataFrame([{
        "Accuracy": acc,
        "F1_Macro": f1_macro,
        "F1_Weighted": f1_weighted
    }])
    metrics_df.to_csv(os.path.join(results_dir, "f1_summary_table.csv"), index=False)
    print(f"Saved evaluation metrics to {results_dir}/f1_summary_table.csv")

if __name__ == "__main__":
    main()
