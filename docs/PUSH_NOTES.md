# What to push, and what is still missing

Prepared locally in `C:\Users\sange\multilingual-aa-sfaca` (commits are local only; nothing was pushed).

## Changes made (ready to push from another account)

| File | Change |
|:-|:-|
| `src/analyzer.py` (new) | sanitize, sentence split, overlapping windows, per-window script routing, aggregation. Returns the response schema in `AGENT_BRIEF.md` (Phase E). |
| `src/router.py` (new) | `detect_script` moved out of `inference.py` so it has no torch dependency. |
| `src/inference.py` | 8-class labels (was 10), loads `adapter_model.bin` written by `train.py` (the old `load_adapter` call could not read it), batched `predict_probs`. |
| `src/sanitizer.py` | `find_notation_spans` returns math/code spans with offsets. |
| `src/exporters.py` (new) | Highlighted HTML report (red tiers, grey for math/code). |
| `src/stub_scorer.py` (new) | Placeholder scorer for demos/tests. The UI shows a "Demo mode" banner when it is active. |
| `src/model.py` | Default `NUM_CLASSES` 10 to 8. |
| `backend/api.py` | Rewritten: `/health`, `/api/analyze`, `/api/export`; upload limits; no stack traces; CORS via `ALLOWED_ORIGINS`. The old file crashed with an undefined `ai_probs`. |
| `docs/index.html`, `docs/config.js` | New UI (paste or upload, donut, generator bars, per-sentence plot, highlighted text, report download). `docs/app.js` and `docs/style.css` removed (they hard-coded a temporary trycloudflare URL). |
| `scripts/export_adapters.py` (new) | Picks the best run per cluster by validation F1. |
| `tests/test_api.py` (new), `tests/test_inference.py` | 47 tests pass on CPU. |

## Training and evaluation (done locally on the RTX 4050)

Data came from Kaggle `sandeep01321/sfaca-data` (hashes match `docs/DATA_CARD.md`). All five clusters were trained with
`scripts/train_all_local.sh` (seed 42, 3 epochs, length 128). Results are in `results/pipeline_eval.md`.
`scripts/calibrate.py` fits a per-script calibration on validation windows (`configs/calibration.json`, tracked); this fixed
human text being over-flagged as AI (Cyrillic human text was 93% AI before, 33% after). Re-run it whenever adapters change.

Not tracked by git (gitignored, must be uploaded separately): `results/adapters/*` (*.bin, *.pt) and `data/`.

## Not done, and why

1. **One seed only.** Your own notes show same-config runs varying by many points; treat these as a single sample. Seeds 43/44 and the monolithic baseline from `EXPERIMENTS.md` were not run.
2. **GitHub Pages only hosts static files.** Point `window.SFACA_API_URL` (or the Lovable `API_URL`, see `docs/LOVABLE_PROMPT.md`) at wherever `backend/api.py` runs. The adapters (about 15 MB each) must be uploaded to that host or to the Hugging Face Hub.
3. **Not built:** highlighted `.docx`/`.pdf` export (HTML only), evidence tab, Dockerfile, CI.

## Run locally

```bash
pip install -r requirements.txt
SFACA_STUB=1 python backend/api.py          # demo with placeholder scores
ADAPTER_DIR=results/adapters python backend/api.py   # real model, after training
```

Open http://localhost:7860.
