import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from inference import InferenceEngine, detect_script_cluster
import app
from backend import api

def test_imports():
    assert "InferenceEngine" in dir(app)
    assert "InferenceEngine" in dir(api)

def test_inference_engine_missing_adapter_dir():
    # Should raise ValueError when use_stub=False and ADAPTER_DIR is missing
    os.environ.pop("ADAPTER_DIR", None)
    with pytest.raises(ValueError, match="ADAPTER_DIR"):
        InferenceEngine(use_stub=False)

def test_inference_engine_stub_predict():
    engine = InferenceEngine(use_stub=True)
    res1 = engine.predict("hello", "latin")
    res2 = engine.predict("hello", "cyrillic")
    
    assert "human" in res1
    assert "ai" in res1
    assert "generator" in res1

def test_script_cluster_detection():
    # Latin
    assert detect_script_cluster("Hello world, this is a test.") == "latin"
    # Cyrillic
    assert detect_script_cluster("Привет мир") == "cyrillic"
    # Arabic
    assert detect_script_cluster("مرحبا بالعالم") == "arabic"
    # Hanzi/Kana
    assert detect_script_cluster("こんにちは世界") == "hanzi"
    assert detect_script_cluster("你好世界") == "hanzi"
    # Greek
    assert detect_script_cluster("γειά σου κόσμε") == "greek"
