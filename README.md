# SFA-CA: Script-Family-Aware Contrastive Adapters
### Low-Resource Multilingual Authorship Attribution of AI-Generated Text

Group 6 | Text Analytics
G. Jyothish (CB.AI.U4AID24114), J. S. Badri (CB.AI.U4AID24120),
K. Chakradhar Reddy (CB.AI.U4AID24122), Sandeep S (CB.AI.U4AID24149)

---

## What this is

An extension of La Cava et al., *"Authorship Attribution in Multilingual
Machine-Generated Texts"* (ACL 2026). We add script/family-aware LoRA
adapters on top of a frozen XLM-RoBERTa-large backbone, trained with a
contrastive objective, to improve cross-lingual transfer for identifying
which LLM generated a given text.

## Project structure

```
sfa-ca-multilingual-attribution/
├── data/
│   ├── raw/              # downloaded MULTITuDE v3 CSV goes here
│   └── clusters/         # (reserved for cluster-specific data splits)
├── src/
│   ├── clusters.py       # language -> script/family cluster mapping
│   ├── data_loader.py    # loads + filters MULTITuDE data
│   ├── model.py          # frozen backbone + per-cluster LoRA adapters
│   ├── contrastive_loss.py
│   └── train.py          # trains one cluster's adapter at a time
├── configs/              # (add your yaml experiment configs here)
├── results/              # F1 tables, confusion matrices, saved adapters
├── requirements.txt
└── README.md
```

## Setup (do this once, in VS Code, locally)

```bash
python -m venv attribution_env
source attribution_env/bin/activate      # Windows: attribution_env\Scripts\activate
pip install -r requirements.txt

huggingface-cli login       # paste your free HF token when prompted
wandb login                 # paste your free wandb API key when prompted
```

Write and edit all your `.py` files here in VS Code. Commit and push to
GitHub regularly:

```bash
git add .
git commit -m "Add clusters.py and data loader"
git push
```

## Getting your data

1. Download MULTITuDE v3 from Zenodo (referenced in the base paper).
2. Place the CSV at `data/raw/multitude_v3.csv`.
3. Make sure it has at least these columns: `text`, `label`, `lang`
   (see `data_loader.py` docstring for the expected label vocabulary).

## Running the actual training (do this in Colab, not locally)

Open a new Colab notebook, select **Runtime > Change runtime type > GPU**,
then run:

```python
# Cell 1: get your code
!git clone https://github.com/<your-username>/sfa-ca-multilingual-attribution.git
%cd sfa-ca-multilingual-attribution
!pip install -r requirements.txt

# Cell 2: log in (paste tokens when prompted)
!huggingface-cli login
!wandb login

# Cell 3: upload your MULTITuDE CSV to data/raw/, or download it directly here

# Cell 4: train one cluster's adapter (repeat once per cluster)
!python src/clusters.py          # sanity check the cluster mapping first
!python src/train.py --cluster latin --data data/raw/multitude_v3.csv --epochs 3
!python src/train.py --cluster cyrillic --data data/raw/multitude_v3.csv --epochs 3
```

Repeat the last command once per cluster (`latin`, `cyrillic`, `greek`,
`arabic`, `hanzi`). Each run saves its adapter to
`results/adapters/<cluster_name>/` and logs metrics to your wandb dashboard.

## Quick sanity checks before your first real run

```bash
python src/clusters.py     # prints the cluster mapping -- check it looks right
python src/model.py        # downloads xlm-roberta-large once, runs a tiny forward pass
python src/contrastive_loss.py   # tests the loss on random data
```

If all three run without errors, you're ready to point `train.py` at real data.

## Next steps (after this starter code works)

- **Experiment 2**: write an `evaluate_cross_cluster.py` script that loads
  one cluster's adapter and tests it on a *different* cluster's held-out
  data (zero-shot transfer).
- **Experiment 3**: add your low-resource languages to
  `clusters.py -> LOW_RESOURCE_LANGUAGES` and repeat training/eval.
- **Experiment 4 (ablation)**: add a "no-adapter" and "single-shared-adapter"
  variant of `model.py` to compare against SFA-CA.
- **Notation robustness**: add a preprocessing step (regex-based masking of
  LaTeX/code/citations) before tokenization, and re-run evaluation.
