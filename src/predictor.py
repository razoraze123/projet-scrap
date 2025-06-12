"""Utilities for loading the trained intent classifier and predicting labels."""

from pathlib import Path

import torch
from transformers import AutoModelForSequenceClassification, DistilBertTokenizerFast

MODEL_DIR = Path(__file__).resolve().parent.parent / "model" / "trained_model"
if not MODEL_DIR.exists():
    raise FileNotFoundError(f"Trained model directory not found: {MODEL_DIR}")

tokenizer = DistilBertTokenizerFast.from_pretrained(MODEL_DIR)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_DIR)
model.eval()

id2label = {int(k): v for k, v in model.config.id2label.items()}


def predict_intent(text: str) -> str:
    text = text.strip()
    if not text:
        raise ValueError("Input text is empty")
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
        pred_id = outputs.logits.argmax(dim=1).item()
    return id2label[pred_id]


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        sentence = " ".join(sys.argv[1:])
    else:
        sentence = input("Texte: ")
    print(predict_intent(sentence))
