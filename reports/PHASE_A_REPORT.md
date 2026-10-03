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

tests/test_inference.py::test_head_isolation
tests/test_inference.py::test_engine_parity
  C:\dev\multilingual-aa-sfaca\src\inference.py:110: FutureWarning: You are using `torch.load` with `weights_only=False`...

======================= 21 passed, 3 warnings in 14.49s =======================
```

## Failure Mode Tracking Table

| ID | Issue | Status |
|---|---|---|
| F2 | The wrong adapter/classifier is active for some scripts. | Fixed (via `InferenceEngine` & dynamic `peft` loading) |
| F6 | Cross-language score contamination (one language affects another). | Fixed (isolated classifier heads `ModuleDict` tested via isolation test) |
| F7 | API crashing/hanging when `torchao` fails to load. | Fixed (abstracted patch correctly to `src/compat.py`) |
| F11 | `app.py` duplicate routing logic gets out of sync with `api.py`. | Fixed (centralized into `src/inference.py` and strictly tested) |

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
