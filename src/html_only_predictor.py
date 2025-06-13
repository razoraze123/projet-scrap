"""Prediction utility for HTML-only selector model."""

import argparse
import sys
from pathlib import Path

import torch
from transformers import (
    AutoModelForSequenceClassification,
    DistilBertTokenizerFast,
)

import config
from src.memoire_generale import ajouter_interaction

MODEL_DIR = config.HTML_ONLY_SELECTOR_MODEL_DIR
if not MODEL_DIR.exists():
    raise FileNotFoundError(
        f"Trained model directory not found: {MODEL_DIR}"
    )

_tokenizer = DistilBertTokenizerFast.from_pretrained(MODEL_DIR)
_model = AutoModelForSequenceClassification.from_pretrained(MODEL_DIR)
_model.eval()

_id2label = {int(k): v for k, v in _model.config.id2label.items()}


def predict_selector(html: str) -> str:
    """Return predicted CSS selector for given HTML snippet."""
    html = html.strip()
    if not html:
        raise ValueError("Input HTML is empty")
    inputs = _tokenizer(
        html,
        return_tensors="pt",
        truncation=True,
        padding=True,
    )
    with torch.no_grad():
        logits = _model(**inputs).logits
        pred_id = logits.argmax(dim=1).item()
    selector = _id2label[pred_id]
    try:
        ajouter_interaction(
            "prediction",
            {"html": html, "reponse": selector},
        )
    except Exception:
        pass
    return selector


def main(argv=None) -> None:
    """Run the predictor from the command line."""
    parser = argparse.ArgumentParser(
        description="Predict CSS selector from HTML snippet",
    )
    parser.add_argument("file", nargs="?", help="HTML file, default stdin")
    args = parser.parse_args(argv)

    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            html = f.read()
    else:
        html = sys.stdin.read()

    selector = predict_selector(html)
    print(selector)


if __name__ == "__main__":
    main()
