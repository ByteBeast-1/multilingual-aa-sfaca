# Phase A Report

## What Changed
- Archived dead files into `archive/` directory: `src/evaluate_antigravity.py`, `configs/default_config.yaml`, `Project_Report_Script_Family_Adapters ( small explaination).docx`, and `SFA-CA_Project_Report (small explaination).docx`. Removed `tempCodeRunnerFile.python`.
- Unified and pinned dependencies into a single `requirements.txt` at the root, removing `backend/requirements.txt`. Exact versions matching the test environment were pinned.
- Created `configs/default.yaml` setting `max_length: 128` and other parameters for inference/training.
- Created `src/inference.py` featuring the `InferenceEngine` class and `detect_script_cluster` router function to centralize loading the backbone, adapters, and heads securely.
- Refactored `app.py` and `backend/api.py` to use `InferenceEngine` from `src/inference.py`, replacing their duplicate script routing logic and flawed model loading.
- Created `tests/test_inference.py` to assert correct import routing, cluster detection (Latin, Cyrillic, Arabic, Hanzi, Kana, Greek), and stub behavior.

## Exact Commands Run
- `mkdir archive; git mv src/evaluate_antigravity.py archive/; git mv configs/default_config.yaml archive/; git mv "Project_Report_Script_Family_Adapters ( small explaination).docx" archive/; git mv "SFA-CA_Project_Report (small explaination).docx" archive/; git rm tempCodeRunnerFile.python; git commit -m "phaseA: archive dead files"`
- `git add configs/default.yaml; git commit -m "phaseA: create default config"`
- `git add src/inference.py; git commit -m "phaseA: create inference module"`
- `git add app.py backend/api.py; git commit -m "phaseA: refactor to use inference module"`
- `git rm backend/requirements.txt; git add requirements.txt; git commit -m "phaseA: unify and pin requirements"`
- `mkdir tests`
- `pytest -v tests/ > pytest_output.txt 2>&1; cat pytest_output.txt`
- `git add tests/; git commit -m "phaseA: add tests for inference module and router"`

## Test Output

```
============================= test session starts =============================
platform win32 -- Python 3.10.5, pytest-9.1.1, pluggy-1.6.0 -- C:\Users\sande\AppData\Local\Programs\Python\Python310\python.exe
cachedir: .pytest_cache
rootdir: C:\dev\multilingual-aa-sfaca
plugins: anyio-4.14.2
collecting ... collected 4 items

tests/test_inference.py::test_imports PASSED                             [ 25%]
tests/test_inference.py::test_inference_engine_missing_adapter_dir PASSED [ 50%]
tests/test_inference.py::test_inference_engine_stub_predict PASSED       [ 75%]
tests/test_inference.py::test_script_cluster_detection PASSED            [100%]

============================== warnings summary ===============================
app.py:187
  C:\dev\multilingual-aa-sfaca\app.py:187: UserWarning: The parameters have been moved from the Blocks constructor to the launch() method in Gradio 6.0: theme. Please pass these parameters to launch() instead.
    with gr.Blocks(theme=custom_theme, title="SFA-CA Multilingual AI Text Attribution System") as app:

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
======================== 4 passed, 1 warning in 17.93s ========================
```

## Numbers Produced
No numbers produced in this phase (no evaluation run).

## Open Issues / Could Not Do
- The Gradio `Blocks(theme=...)` warning might need to be resolved in a UI pass later by passing it to `launch()`.
- The `max_length: 128` should be verified against Kaggle training values, as requested.
