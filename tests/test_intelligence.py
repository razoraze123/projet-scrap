import types
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

import intelligence


def test_keyword_detection():
    assert intelligence.analyser_question("Quel est le titre ?", debug=False) == "titre"


def test_pipeline_fallback(monkeypatch):
    fake = types.SimpleNamespace(__call__=lambda self, *a, **k: {
        "labels": ["image"],
        "scores": [0.9],
    })
    monkeypatch.setattr(intelligence, "_classifier", fake)
    assert intelligence.analyser_question("quelle image", debug=False) == "image"
