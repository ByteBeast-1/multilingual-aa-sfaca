"""
train.py
--------
Trains ONE cluster's LoRA adapter at a time (run this once per cluster,
e.g. once for "latin", once for "cyrillic", etc. -- this matches
Experiment 1 / in-cluster training).

Usage (from the project root, after activating your venv):
    python src/train.py --cluster latin --data data/raw/multitude_v3.csv \
        --epochs 3 --batch_size 8 --lr 2e-4

Run this inside Colab after `git clone`-ing your repo -- see README.md
for the exact Colab cell commands.
"""

import argparse
import os
import torch
from torch.utils.data import DataLoader
from torch.optim import AdamW
from sklearn.metrics import f1_score
import wandb

from model import SFACAModel, build_tokenizer
from data_loader import load_multitude_csv, filter_by_clusters, filter_by_split, AttributionDataset
from contrastive_loss import combined_loss
from clusters import all_clusters


def train_one_cluster(args):
    wandb.init(
        project="sfa-ca-multilingual-attribution",
        name=f"train-{args.cluster}",
        config=vars(args),
    )

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    # ---- Data ----
    df = load_multitude_csv(args.data)
    cluster_df = filter_by_clusters(df, [args.cluster])
    print(f"Cluster '{args.cluster}': {len(cluster_df)} total samples")

    # Use MULTITuDE's own provided train/test split (not a random one --
    # this matches the base paper's evaluation setup exactly).
    train_df = filter_by_split(cluster_df, "train")
    val_df = filter_by_split(cluster_df, "test")
    print(f"  -> {len(train_df)} train / {len(val_df)} test samples")

    tokenizer = build_tokenizer()
    train_ds = AttributionDataset(train_df, tokenizer, max_length=args.max_length)
    val_ds = AttributionDataset(val_df, tokenizer, max_length=args.max_length)

    train_loader = DataLoader(train_ds, batch_size=args.batch_size, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=args.batch_size, shuffle=False)

    # ---- Model ----
    model = SFACAModel(clusters=all_clusters()).to(device)
    model.set_active_cluster(args.cluster)

    # Only the active adapter's params + classifier head are trainable.
    trainable_params = [p for p in model.parameters() if p.requires_grad]
    optimizer = AdamW(trainable_params, lr=args.lr)

    # ---- Training loop ----
    best_val_f1 = -1.0
    save_path = f"results/adapters/{args.cluster}"
    
    use_amp = (device.type == "cuda")
    scaler = torch.amp.GradScaler("cuda", enabled=use_amp)

    for epoch in range(args.epochs):
        model.train()
        total_loss = 0.0

        for batch in train_loader:
            input_ids = batch["input_ids"].to(device)
            attention_mask = batch["attention_mask"].to(device)
            labels = batch["labels"].to(device)

            optimizer.zero_grad()

            with torch.amp.autocast("cuda", enabled=use_amp):
                embeddings = model.get_embedding(input_ids, attention_mask, args.cluster)
                logits = model.classifier(embeddings)

                loss = combined_loss(
                    logits, embeddings, labels,
                    contrastive_weight=args.contrastive_weight,
                )

            scaler.scale(loss).backward()
            scaler.step(optimizer)
            scaler.update()

            total_loss += loss.item()

        avg_train_loss = total_loss / len(train_loader)
        val_f1 = evaluate(model, val_loader, args.cluster, device)

        print(f"Epoch {epoch+1}/{args.epochs} | train_loss={avg_train_loss:.4f} | val_macro_f1={val_f1:.4f}")
        wandb.log({"epoch": epoch + 1, "train_loss": avg_train_loss, "val_macro_f1": val_f1})

        # Save checkpoint if validation F1 improved
        if val_f1 > best_val_f1:
            best_val_f1 = val_f1
            os.makedirs(save_path, exist_ok=True)
            from peft import get_peft_model_state_dict
            adapter_weights = get_peft_model_state_dict(model.backbone, adapter_name=args.cluster)
            torch.save(adapter_weights, os.path.join(save_path, "adapter_model.bin"))
            torch.save(model.classifier.state_dict(), os.path.join(save_path, "classifier.pt"))
            print(f"  --> Saved new best checkpoint with val_macro_f1={best_val_f1:.4f}")

    print(f"Training finished. Best validation F1: {best_val_f1:.4f}")
    wandb.finish()


@torch.no_grad()
def evaluate(model, loader, cluster_name, device):
    model.eval()
    all_preds, all_labels = [], []
    use_amp = (device.type == "cuda")

    for batch in loader:
        input_ids = batch["input_ids"].to(device)
        attention_mask = batch["attention_mask"].to(device)
        labels = batch["labels"]

        with torch.amp.autocast("cuda", enabled=use_amp):
            logits = model(input_ids, attention_mask, cluster_name)
        preds = logits.argmax(dim=1).cpu()

        all_preds.extend(preds.tolist())
        all_labels.extend(labels.tolist())

    return f1_score(all_labels, all_preds, average="macro")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--cluster", type=str, required=True,
                        choices=all_clusters(),
                        help="Which script/family cluster to train an adapter for.")
    parser.add_argument("--data", type=str, required=True,
                        help="Path to the MULTITuDE CSV file.")
    parser.add_argument("--epochs", type=int, default=3)
    parser.add_argument("--batch_size", type=int, default=8)
    parser.add_argument("--lr", type=float, default=2e-4)
    parser.add_argument("--max_length", type=int, default=512)
    parser.add_argument("--contrastive_weight", type=float, default=0.5)
    args = parser.parse_args()

    train_one_cluster(args)
