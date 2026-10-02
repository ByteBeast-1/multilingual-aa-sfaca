# AGENT BRIEF: SFA-CA (Script-Family-Aware Contrastive Adaptation)

Read this whole file before doing anything. Place it in the repo root and treat it as the source of truth for this project. If the human's message conflicts with this file, ask which one wins.

## 0. How you must work

1. **One phase at a time.** Do the phase the human names, then STOP and wait for approval. Never start the next phase on your own.
2. **Plan first.** Before editing, post: the files you will touch, the commands you will run, the risks. Wait for "approved".
3. **End every phase with `reports/PHASE_<X>_REPORT.md`** containing: what changed (file list), exact commands run, test output (pasted), numbers produced (each with the file it came from), open issues, and what you could NOT do.
4. **Small commits.** One logical change per commit, message format `phaseX: what and why`. Never rewrite history. Never force-push.
5. **Ask when blocked.** You cannot run Kaggle GPU jobs, call paid APIs without keys, or push to Hugging Face without a token. Write the scripts/notebooks, tell the human exactly what to run, and wait for results.
6. **Never delete data or results.** Move to `archive/` instead.

## 1. Honesty rules (non-negotiable)

- NEVER invent, estimate, round up, or hand-edit a metric. Every number in README, docs, UI, report or slides must come from a file in `results/` that a script generated. Record the command and git commit hash next to it.
- NEVER tune, select checkpoints, or choose thresholds on the test split. Test is touched once per final evaluation.
- If a result gets worse after fixing a bug, report it as is. Lower honest numbers are expected after the data fixes below and are fine.
- The UI and docs must say "likelihood" and never say "proof" or "guilty". A detector gives evidence, not certainty. Include a limitations section with real measured failure cases.
- If you cannot verify a claim, remove or reword it and list it in the report.

## 2. Project goal (what "done" looks like)

A deployed prototype where a user pastes text or uploads `.txt/.md/.docx/.pdf` and gets:
1. Overall **% AI vs % Human**.
2. **Which generator** most likely wrote the AI parts, with the probability for every class.
3. **Where** the AI text is: per-passage highlighting, with a plot of AI probability across the document.
4. **Notation handling**: LaTeX math and code are detected, excluded from scoring, and shown with dark grey shading.
5. **A downloadable copy of the same file** with AI passages highlighted (red tiers by probability) and notation dark-grey, plus a legend.
6. An **Evidence tab** showing measured metrics (see Phase D), not claims.

Supported scripts: Latin, Cyrillic, Greek, Arabic, Hanzi (Chinese) with one LoRA adapter each on a frozen `xlm-roberta-large`.

## 3. Audit findings you must fix (verified from the repo)

| # | Finding | Where |
|:-|:-|:-|
| F1 | The `Gemini-2.5-Flash` and `Claude-Haiku-4.5` classes are built from 30 hand-written English sentences each, repeated ~1,800 times per language, in BOTH train and test. Test set = copies of train set; model never saw real Gemini/Claude text; English text labeled as Arabic/Chinese etc. Every 10-class result is inflated by this (the README headline numbers came from earlier 8-class runs, see F15). | `src/augment_gemini_claude.py` |
| F2 | Training saves a separate `classifier.pt` per cluster, but `app.py` and `backend/api.py` load all of them into ONE shared head in a loop. Only the last loaded survives, so non-Latin clusters use the wrong head. | `app.py` ~L80, `backend/api.py` `_load_model` |
| F3 | The MULTITuDE **test** split is used as validation and the best epoch is chosen on it. | `src/train.py` |
| F4 | No baseline script exists for the "+19.46% over monolithic baseline" claim. No latency benchmark exists for "<27 ms". `results/` is gitignored, so evidence for the 5x5 matrix is not in the repo. | docs, `.gitignore` |
| F5 | Contrastive loss runs on single-cluster batches, so it cannot pull the same generator together "across scripts". Either implement mixed-script batches or change the claim to "within-cluster supervised contrastive loss". | `src/train.py`, `src/contrastive_loss.py` |
| F6 | Inference truncates input to 256 tokens (only the start of a file is analysed); training length differs (default 512, README uses 128). Must match training. | `app.py`, `backend/api.py` |
| F7 | API has its own regex sanitizer using a `[MATH]` placeholder never seen in training, no calibration, duplicating `src/sanitizer.py`. | `backend/api.py` |
| F8 | NDI calibration (`calibration_factor=0.35`) is an untested heuristic. | `src/sanitizer.py` |
| F9 | `docs/app.js` hardcodes a temporary `trycloudflare.com` URL. | `docs/app.js` |
| F10 | Dead/stale files: `src/evaluate_antigravity.py` (imports nonexistent names), `configs/default_config.yaml` (different model/lr, unused), `tempCodeRunnerFile.python` (unrelated quantum code). README says 7 LLMs, docs say 9. | repo root, `src/`, `configs/` |
| F11 | Script router counts Latin letters with `[a-zA-Z]`, so it mishandles accents, Japanese kana, Persian/Urdu extra letters. Mixed-script text is routed by a single document-level vote. | `backend/api.py` |
| F12 | The 20 off-diagonal values of the README 5x5 transfer matrix, the "+19.46%" and the "<27 ms" claims do NOT appear in the Kaggle notebook outputs. The matrices the notebook actually computed differ a lot. Treat the README matrix as UNVERIFIED until reproduced or removed. | `README.md`, `notebooks/kaggle/` |
| F13 | No seeds were ever set, and the same config gave very different results across reruns (e.g. Greek 0.7853 vs 0.6314, Arabic 0.8762 vs 0.7981 on the same clean data). Single-run numbers are not reliable; mean ± std over seeds is mandatory. | `notebooks/kaggle/`, `src/train.py` |
| F14 | The "low-resource zero-shot" run for Tamil (`ta`) found no data and created a **dummy evaluation suite**. The only real zero-shot numbers are for `ca`, `ga`, `gd` (Latin script, not Indic/African). Remove any Indic/African claim unless real data is evaluated. | `src/low_resource_eval.py` |
| F15 | The headline per-cluster F1s in the README (0.8762, 0.7853, 0.7743, 0.6696) came from early runs on the CLEAN 8-class data (train counts match). The later 10-class runs (template classes) gave different numbers and are what the current adapters were trained on. The clean 8-class adapters were probably overwritten. Docs wrongly call everything "10-class". | notebook cells, README |
| F16 | W&B API keys were hard-coded in the Kaggle notebook. Never put secrets in notebooks or code; use Kaggle Secrets / env vars. Never commit the original notebook; use the REDACTED copy. | `notebooks/kaggle/` |

See `notebooks/kaggle/KAGGLE_RUN_FACTS.md` for the verified run table, hardware and timings. Where it conflicts with README/docs, the facts file wins.

## 4. Phases

### Phase A: Repo hygiene and bug fixes
- Move dead files (F10) to `archive/`; make one config (`configs/default.yaml`) that `train.py` actually reads (backbone, lora_r/alpha/dropout, lr, epochs, max_length, batch size, seed, contrastive weight, temperature).
- Create `src/inference.py` as the ONLY inference path. It loads the backbone once, one adapter + one classifier head per cluster, and activates both together (fixes F2). `app.py` and `backend/api.py` must import it.
- Fix the router (F11): Unicode-block based, ignore digits/punctuation/Latin-in-other-script quotes, handle Japanese kana and Persian/Urdu letters explicitly (map to nearest cluster and flag `routing_confidence`).
- Add `tests/` with pytest: router, sanitizer, file parser, loss (no NaN on batches with no positives), inference head-per-cluster test (loading two clusters must give different head weights).
- Add `requirements.txt` with pinned versions and a `requirements-dev.txt`.
- **Done when:** `pytest -q` passes on CPU; `app.py` and the API both call `src/inference.py`; no file mentions `evaluate_antigravity` or the quantum code.

### Phase B: Data
- Inspect the real CSV (`multitude_v3_clean.csv`): columns, text lengths, whether a source/prompt/article id exists. Report what you find before changing anything.
- **Default decision: 8-class main task** (human + the 7 real MULTITuDE generators). Remove the template-based Gemini/Claude rows from every training and evaluation path. Keep a `--class_set 10` flag only for an optional real-data experiment.
- **Optional B2 (only if the human supplies API keys):** generate REAL Gemini-2.5-Flash and Claude-Haiku-4.5 text for each language in the five clusters using prompts derived from MULTITuDE (or the human source text if prompts are unavailable). Record model, params, date, prompt template. Each source text must appear in only one split. Check provider terms before use and tell the human what you assumed.
- Build leakage-safe splits: keep MULTITuDE `test` untouched; carve a `val` from `train` grouped by source id (or by normalized-text hash if no id). Add `scripts/check_leakage.py`: asserts zero overlap across train/val/test by normalized-text hash and by source id; exits non-zero on failure. Run it in CI and before every training run.
- Deduplicate exact and near-duplicate texts (report counts removed).
- Print and save class balance per cluster and per split (`results/data_stats.csv`). If classes are imbalanced, use class-weighted loss or balanced sampling and say so.
- **Done when:** leakage check passes; data stats saved; the human has approved the 8-class decision.

### Phase C: Training (the human runs the GPU jobs on Kaggle; you write everything)
- Provide a Kaggle notebook (`notebooks/kaggle_train.ipynb`) and a CLI `src/train.py` with: `--cluster`, `--seed`, `--class_set`, `--lora_r`, `--contrastive_weight`, `--max_length`, `--max_train_samples`, `--out_dir`. It must: select the best epoch on **val only**, save adapter + that cluster's head + `config.json` (all args + git hash + data hash) + `metrics.json`, and push the folder to a Kaggle output dataset or the HF Hub after each run (sessions get wiped).
- Add a **smoke-test mode** (`--smoke`: 1 epoch, 500 samples) and print time per 1,000 samples so the human can budget the real runs.
- Add a **shuffled-label sanity run** (small cluster, labels shuffled): macro-F1 must be near chance (about 1/num_classes). If it is not, there is leakage or a bug. Stop and report.
- Experiments to support (write the commands in `EXPERIMENTS.md`, ordered by priority):
  1. Each of 5 clusters, 3 seeds (42, 43, 44), contrastive weight 0.5.
  2. **Monolithic baseline:** one model on all clusters (single LoRA, same backbone, same data, same splits, same seeds).
  3. **Ablation:** contrastive weight 0 vs 0.5 on at least Latin and one non-Latin cluster.
  4. **Ablation:** LoRA rank 8/16/32 on one or two clusters.
  5. **Optional F5 fix:** mixed-script batches (sample from all clusters, activate the matching adapter per sub-batch). If not done, reword the claim everywhere to "within-cluster".
- Cap very large clusters (Latin) with `--max_train_samples` and record the cap. Never silently subsample.
- **Done when:** `results/runs/<cluster>_seed<k>/metrics.json` exists for every planned run, and the report lists time per run.

### Phase D: Evaluation and the Evidence package
Write `scripts/make_evidence.py`, which reads `results/runs/*` and produces `results/evidence/evidence.json` plus CSVs/PNGs. It must include:
1. Per-cluster macro-F1 and accuracy as mean ± std over seeds (val AND test, clearly labelled).
2. Per-class F1 and a confusion matrix per cluster.
3. **Binary human-vs-AI**: F1 and AUROC, derived from `1 - P(human)`.
4. **Calibration:** reliability curve and expected calibration error (ECE). Fit temperature scaling on **val** and apply on test. Report ECE before/after.
5. SFA-CA vs monolithic baseline, with the same seeds. The "+X%" headline must be computed here or deleted.
6. Ablation tables (contrastive on/off, LoRA rank).
7. The 5x5 cross-cluster matrix computed by `evaluate_cross_cluster.py` on the TEST split, saved as CSV, using the matching head for each adapter.
8. Low-resource zero-shot results (`low_resource_eval.py`), only if data exists; else state "not evaluated".
9. **Localization benchmark** (required for the highlight feature): build synthetic mixed documents from test texts of the same language with known per-paragraph labels (human paragraphs + AI paragraphs from one generator). Score the highlighter at sentence level (precision, recall, F1 for the AI class) for window sizes 64/128/256 tokens. Pick the window size on val-built mixtures, report on test-built mixtures.
10. **Sanitizer benchmark:** a small labelled set (at least 20 human LaTeX/code-heavy documents and 20 AI-written LaTeX/code-heavy documents; the human may need to supply or approve them). Report false-positive and false-negative rates with the heuristic calibration ON vs OFF. Keep the heuristic only if it measurably helps; otherwise remove it and keep NDI as a displayed warning.
11. **Latency:** p50/p95 per 1,000-character document and per 5-page file, with hardware name recorded.
12. A `limitations.json` listing measured weak spots (short texts, mixed script, paraphrased AI text, specific confused generator pairs).
- **Done when:** `evidence.json` validates against a schema, and every number the UI/README will show exists in it.

### Phase E: Inference engine (`src/inference.py`)
Pipeline: parse -> sanitize -> segment -> route -> batch infer -> calibrate -> aggregate.
- **Sanitize:** use `src/sanitizer.py` only. Return spans `(start, end, type)` for math/code so the original text offsets are preserved for highlighting. Do NOT substitute placeholders into model input; remove notation spans from the text the model sees.
- **Segment:** the classifier was trained on whole texts of a fixed token length, so scoring single short sentences is out-of-distribution. Use overlapping token windows of the length chosen in Phase D (stride about half the window), then give each sentence the average probability of the windows covering it. Sentences shorter than a minimum are marked `too_short` and not scored.
- **Route:** per document by default; if more than one script has substantial share, route per segment and return `mixed_script: true`.
- **Batch** all windows, no per-window model reloads, `torch.no_grad`, fp16 on GPU. Enforce limits: max file size and max windows per request, returning a clear error.
- **Aggregate:** document AI% = length-weighted mean of segment AI probabilities (`1 - P(human)` after temperature scaling). Document generator probabilities = AI-probability-weighted mean of the generator distributions over segments. Report `confidence` as the margin between the top two classes and a `low_evidence` flag for short or notation-heavy input.
- **Response schema (must match exactly; the UI depends on it):**
```json
{
  "ai_pct": 62.4, "human_pct": 37.6,
  "generator_probs": {"human": 0.376, "Mistral-7B-Instruct-v0.2": 0.31, "...": 0.0},
  "top_generator": "Mistral-7B-Instruct-v0.2",
  "script": "Latin", "adapter": "latin", "routing_confidence": 0.98, "mixed_script": false,
  "ndi": 0.04, "calibrated": false, "low_evidence": false, "warnings": [],
  "segments": [
    {"start": 0, "end": 142, "text": "...", "type": "text", "ai_prob": 0.81, "scored": true},
    {"start": 142, "end": 171, "text": "$E=mc^2$", "type": "notation", "ai_prob": null, "scored": false}
  ]
}
```
- **Done when:** unit tests cover offsets (concatenating `segments[*].text` reproduces the cleaned original), empty input, very long input, mixed script, and notation-only input; the localization benchmark runs through this exact code path.

### Phase F: API (FastAPI, `backend/api.py`)
- `GET /health` (model loaded, adapters present, version, git hash).
- `POST /api/analyze`: multipart with either `text` or `file`; returns the schema above.
- `POST /api/export`: same inputs plus `format` (`original` or `html`); returns the highlighted file (Phase G).
- `GET /api/evidence`: serves `evidence.json`.
- Input validation, size limits, timeouts, clear JSON errors, no stack traces to clients, restrict CORS to the deployed frontend origin via env var, no file persistence (process in memory/tmp and delete).
- Tests with FastAPI `TestClient` using a tiny stub model so CI runs on CPU.
- **Done when:** `pytest -q` passes and a curl example per endpoint is in `backend/README.md`.

### Phase G: Highlighted file export (`src/exporters.py`)
Colors: AI passages red tiers by probability (about 0.5-0.65 light, 0.65-0.8 medium, above 0.8 strong); notation = dark grey (shading, readable text); unscored/too_short = no highlight. Add a legend and a short summary (AI%, top generator, date, model version, disclaimer).
- **.docx:** open the uploaded document with `python-docx`, split runs at segment boundaries, apply run shading (`w:shd`) because Word's built-in highlight palette is too limited for tiers. Preserve existing formatting, tables, headers. Output the same file name with `_highlighted` suffix.
- **.pdf:** with PyMuPDF, locate segment text via `page.search_for` and add highlight annotations. Works only for text PDFs; scanned PDFs return a clear error. If a segment can't be located, collect it and add to a summary page; if too many fail, fall back to a clean re-rendered report PDF and say so in `warnings`.
- **.txt/.md:** return the same text with HTML highlights as `.html`, plus an annotated `.md` using markers.
- Golden-file tests with 2 docx, 2 pdf, 1 md samples in `tests/data/`.
- **Done when:** output opens correctly in Word/Acrobat (the human will check visually), and the number of failed-to-locate segments is reported.

### Phase H: Frontend (`frontend/`)
Use the provided `sfaca_ui.html` prototype as the visual reference. Keep it minimal. DO NOT add a sidebar, chat, agents, history or admin pages.
- Layout: header, input card (tabs: Paste text / Upload file), results below.
- Results: donut with "% AI / % Human"; 10-class (or 8-class) generator bars; badges for script, adapter, NDI, calibration, low-evidence warnings; per-passage bar plot (click to jump); highlighted document view (red tiers, dark grey notation, tooltip with probability); "N of M passages flagged"; **Download highlighted file** button.
- **Evidence tab:** reads `/api/evidence`; shows metrics tables, confusion matrix, reliability curve, baseline comparison, localization and sanitizer results, and the limitations list. Every number shown must come from `evidence.json`.
- Replace the demo `demo()` function with the real API; keep the `API_URL` as a config value from an env/`config.js`, never hardcoded to a tunnel.
- Responsive, light/dark, accessible contrast, keyboard focus, loading and error states, clear message for unsupported/scanned PDFs.
- Wording: "likely", "evidence", never "proof". Show a short responsible-use note.
- **Done when:** a manual script in the report walks through paste text, upload docx, upload pdf, notation-heavy text, and an error case, with screenshots.

### Phase I: QA and robustness
- Test: very short text, empty input, 50-page PDF, scanned PDF, mixed Arabic+English, emoji, RTL text, huge single paragraph, text with only math, text with Unicode normalization differences.
- Re-run `check_leakage.py`, full `pytest`, and the end-to-end script `scripts/e2e.py` (uploads sample files to a running API and checks response schema and export files).
- GitHub Actions CI: lint + pytest on CPU.
- **Done when:** the report includes a table of edge cases with the observed behavior and any known failures.

### Phase J: Deployment
- `Dockerfile` (CPU by default, optional GPU), `.dockerignore`, pinned requirements. Load the backbone from the HF cache and adapters+heads from the Hugging Face Hub (confirm `push_to_hub.py` uploads the classifier head and `config.json` too, not only the adapter).
- Target: a Hugging Face Space (Docker SDK) serving the FastAPI backend and the static frontend from the same app, so there is one URL. Provide a `deploy/README.md` with exact steps and required secrets/env vars (`HF_TOKEN`, `ALLOWED_ORIGINS`, adapter repo ids).
- Add a `/health` check, model warm-up at startup, and request concurrency limits. Document expected CPU latency and cold start from the Phase D benchmark. If CPU is too slow, offer int8 dynamic quantization and re-run the metrics to show the accuracy cost.
- **Done when:** the deployed URL passes `scripts/e2e.py`, and the report lists the URL, version, and git hash.

### Phase K: Documentation and final report
- Rewrite `README.md` and `MASTER_DOCUMENTATION.md` using only numbers from `evidence.json`. Fix the 7 vs 9 generators inconsistency and the shared-head wording. Add a "Limitations and responsible use" section and a reproducibility section (exact commands, seeds, data hash).
- Produce the slide outline and a 1-page results summary generated from `evidence.json`.
- **Done when:** a grep for every percentage in README/docs finds a matching entry in `results/`.

## 5. What the human must do (you cannot)
- Run Kaggle training and evaluation notebooks and bring back the output folders.
- Provide HF token, optional Gemini/Claude API keys, and approve data decisions.
- Visually check exported docx/pdf files in Word/Acrobat.
Tell the human precisely what to run and what files to return.

## 6. Stop conditions (stop and ask)
- Leakage check fails, or shuffled-label F1 is far above chance.
- Any metric improves suspiciously after a fix (more than a few points) without explanation.
- You are about to modify the test split, delete results, or change class definitions.
- A phase will take significantly longer than planned.
