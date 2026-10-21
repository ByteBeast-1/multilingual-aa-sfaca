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

## Not done, and why

1. **No trained adapters, so the real model has not been run.** The adapters and `multitude_v3_clean.csv` are in your private Kaggle dataset (`sandeep01321/dataset`); they are not in the repo.
   The README matrix numbers are unverified (see `AGENT_BRIEF.md` F12/F13/F15).
2. **Retraining on the local RTX 4050 (6 GB)** is blocked on the CSV and on `data/processed/splits_8class.csv`.
3. **GitHub Pages only hosts static files.** Set `window.SFACA_API_URL` in `docs/config.js` to wherever `backend/api.py` runs (a Hugging Face Space, a VM, or a tunnel). Without that, the page loads but cannot analyze.
4. **Not built:** highlighted `.docx`/`.pdf` export (HTML only), evidence tab, Dockerfile, CI.

## Run locally

```bash
pip install -r requirements.txt
SFACA_STUB=1 python backend/api.py          # demo with placeholder scores
ADAPTER_DIR=results/adapters python backend/api.py   # real model, after training
```

Open http://localhost:7860.
