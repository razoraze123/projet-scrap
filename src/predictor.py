"""Utilities for loading the trained intent classifier and predicting labels."""

from pathlib import Path
import config

import torch
from transformers import AutoModelForSequenceClassification, DistilBertTokenizerFast
from src.memoire_generale import ajouter_interaction

MODEL_DIR = config.CLASSIFIER_MODEL_DIR
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
    label = id2label[pred_id]
    try:
        ajouter_interaction(
            "prediction",
            {"question": text, "reponse": label},
        )
    except Exception:
        pass  # Logging failure should not break prediction
    return label


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        sentence = " ".join(sys.argv[1:])
    else:
        sentence = input("Texte: ")
    ajouter_interaction("texte_libre", {"message": sentence})
    try:
        label = predict_intent(sentence)
        ajouter_interaction("reponse", {"texte": label})
    except Exception as e:
        ajouter_interaction("erreur", {"exception": str(e)})
        raise
    print(label)
