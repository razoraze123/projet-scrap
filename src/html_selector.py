"""Prediction utility for HTML selector model."""
from pathlib import Path
import config

import torch
from transformers import AutoModelForSequenceClassification, DistilBertTokenizerFast
from src.memoire_generale import ajouter_interaction

MODEL_DIR = config.HTML_SELECTOR_MODEL_DIR
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
    selector = _id2label[pred_id]
    try:
        ajouter_interaction(
            "prediction",
            {"question": question, "html": html, "reponse": selector},
        )
    except Exception:
        pass
    return selector
