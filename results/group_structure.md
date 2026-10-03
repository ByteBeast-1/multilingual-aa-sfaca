# Group Structure: Machine/Human Ratios per (Language, Outlet, Generator)

Computed from `data/processed/splits_8class.csv` (train+val rows).

## Summary per Generator

| Generator | Buckets | Share in [0.9,1.1] | Min ratio | Max ratio | Mean ratio |
|-----------|---------|-------------------|-----------|-----------|------------|
| Llama-2-70b-chat-hf | 80 | 100.0% | 0.917 | 1.000 | 0.978 |
| Mistral-7B-Instruct-v0.2 | 80 | 98.8% | 0.889 | 1.031 | 0.999 |
| aya-101 | 80 | 100.0% | 0.998 | 1.031 | 1.001 |
| gpt-3.5-turbo-0125 | 80 | 100.0% | 0.980 | 1.031 | 1.000 |
| opt-iml-max-30b | 80 | 100.0% | 0.917 | 1.031 | 0.986 |
| v5-Eagle-7B-HF | 80 | 100.0% | 0.941 | 1.031 | 0.999 |
| vicuna-13b | 80 | 100.0% | 0.983 | 1.031 | 0.999 |

## Worst Buckets (ratio < 0.9 or > 1.1)

| Generator | Language | Source | n_human | n_machine | ratio |
|-----------|----------|--------|---------|-----------|-------|
| Mistral-7B-Instruct-v0.2 | de | MassiveSumm_rt | 9 | 8 | 0.889 |