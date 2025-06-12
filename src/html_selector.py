"""Prediction utility for HTML selector model."""
from pathlib import Path

import torch
from transformers import AutoModelForSequenceClassification, DistilBertTokenizerFast

MODEL_DIR = Path(__file__).resolve().parent.parent / "model" / "html_selector"
if not MODEL_DIR.exists():
    raise FileNotFoundError(f"Trained model directory not found: {MODEL_DIR}")

_tokenizer = DistilBertTokenizerFast.from_pretrained(MODEL_DIR)
_model = AutoModelForSequenceClassification.from_pretrained(MODEL_DIR)
_model.eval()

_id2label = {int(k): v for k, v in _model.config.id2label.items()}


def predire_selecteur(question: str, html: str) -> str:
    """Return predicted CSS selector for given question and HTML."""
    text = f"[QUESTION] {question.strip()} [HTML] {html.strip()}"
    inputs = _tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        logits = _model(**inputs).logits
        pred_id = logits.argmax(dim=1).item()
    return _id2label[pred_id]
