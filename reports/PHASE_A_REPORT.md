# Phase A Report (Final)

## What Changed
- **Archiving**: `git mv`-ed unused config and scripts into `archive/`. Kept all necessary files untouched.
- **Git Ignore**: Properly added `.venv/` to `.gitignore` and removed the stray untracked scratch files.
- **Inference Refactor**: Removed `use_stub` logic entirely from `src/inference.py`. Re-wrote `InferenceEngine` to support injected models, tokenizers, and classifiers, allowing for comprehensive real testing.
- **Routing Module**: `detect_script` now returns a rich dictionary containing `cluster`, `counts`, `mixed`, `supported`, and `routing_confidence`, preventing unsupported scripts from silently defaulting to 'latin' without tracking.
- **App & API**: Both `app.py` and `backend/api.py` were refactored to consume the real model payload. With `ADAPTER_DIR` unset, neither file crashes on import; they wait until the model is actively invoked.
- **Comprehensive Tests**: Wrote real tests covering the router table (16 cases), head isolation (mocking distinct heads and asserting logits diverge), parity check with the raw model, `ADAPTER_DIR` error throwing, and contrastive loss (checking bounds).
- **Dependencies**: Was instructed to compare against `notebooks/kaggle/KAGGLE_PIP_FREEZE.txt` and pin `torch`, `transformers`, `peft` based on it, but **the freeze file was not found in the repository or file system**. It was skipped for now and should be handled once uploaded.

## Output of the isolated failure run
When breaking the `InferenceEngine` loader deliberately to use the same head for all clusters:
```
============================= test session starts =============================
platform win32 -- Python 3.10.5, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\dev\multilingual-aa-sfaca
plugins: anyio-4.15.1, platformdirs-4.12.2
collected 1 item

tests\test_inference.py F                                                [100%]

================================== FAILURES ===================================
_____________________________ test_head_isolation _____________________________

mock_transformers = (<MagicMock name='from_pretrained' id='2412272468032'>, <MagicMock name='get_peft_model' id='2412272852112'>, <MagicMock name='build_tokenizer' id='2412272856384'>)

    def test_head_isolation(mock_transformers):
        ...
            # Logits should be different
>           assert res1["logits"] != res2["logits"]
E           assert [-0.16302280128002167, 0.0641879290342331, ...] != [-0.16302280128002167, 0.0641879290342331, ...]

tests\test_inference.py:120: AssertionError
```

## Test Output

```
============================= test session starts =============================
platform win32 -- Python 3.10.5, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\dev\multilingual-aa-sfaca
plugins: anyio-4.15.1, platformdirs-4.12.2
collected 21 items

tests\test_inference.py .....................                            [100%]

============================== warnings summary ===============================
app.py:169
  C:\dev\multilingual-aa-sfaca\app.py:169: UserWarning: The parameters have been moved from the Blocks constructor to the launch() method in Gradio 6.0: theme. Please pass these parameters to launch() instead.
    with gr.Blocks(theme=custom_theme, title="SFA-CA Multilingual AI Text Attribution System") as app:

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
======================= 21 passed, 1 warning in 12.12s ========================
```

## Failure Mode Tracking Table

| ID | Issue | Status | Evidence |
|---|---|---|---|
| F2 | Shared classifier head overwritten at load | Fixed | `test_head_isolation` proves distinct heads don't contaminate. |
| F6 | Inference truncation to 256 tokens | Not in this phase | Will be addressed in Phase E. |
| F7 | `api.py`'s own sanitizer and `[MATH]` placeholder | Not in this phase | `test_sanitizer` captures current broken `[MATH]` behavior. Phase E/F. |
| F11 | Script router gaps (accents, kana, Hangul, unsupported scripts) | Fixed | `test_router_cases` verifies 16 scripts including Hangul and Hebrew. |

## Git Status Verification

Output of `git status -sb` after cleanup:
```
## phase-a
 M app.py
 M backend/api.py
 M src/inference.py
 M tests/test_inference.py
```

Output of `git diff --name-status --diff-filter=D main..phase-a` (Empty as requested):
```
```
