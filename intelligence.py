"""Analyse d'une question en langage naturel."""

try:
    from transformers import pipeline
except Exception:  # pragma: no cover - optional dependency
    pipeline = None

MODEL_NAME = "distilbert-base-multilingual-cased"
LABELS = ["titre", "description", "prix", "image", "lien", "bouton"]

if pipeline is not None:
    try:
        _classifier = pipeline("zero-shot-classification", model=MODEL_NAME)
    except Exception:  # pragma: no cover - model loading may fail
        _classifier = None
else:  # pragma: no cover - transformers absent
    _classifier = None

_KEYWORDS = {
    "titre": ["titre", "title"],
    "description": ["description"],
    "prix": ["prix", "price"],
    "image": ["image", "photo"],
    "lien": ["lien", "url", "adresse"],
    "bouton": ["bouton", "button"],
}


def analyser_question(question: str, debug: bool = True) -> str:
    """Return the most probable label for the question."""
    q = question.lower()
    for label, words in _KEYWORDS.items():
        if any(w in q for w in words):
            return label

    if _classifier is None:
        # Fallback when transformers or model is unavailable
        return LABELS[0]

    result = _classifier(question, candidate_labels=LABELS)
    label = result["labels"][0]

    if debug:
        print("\n\U0001F4CA Classement des labels :")
        for l, score in zip(result["labels"], result["scores"]):
            print(f" - {l.ljust(12)} : {round(score * 100, 2)} %")
        print(f"\n\u2705 Meilleure prédiction : **{label}**")

    return label

if __name__ == "__main__":
    print("\U0001F9E0 Pose une question sur ce que tu veux extraire (Ctrl+C pour quitter)\n")
    try:
        while True:
            question = input("❓ Que veux-tu extraire ? → ")
            analyser_question(question)
    except KeyboardInterrupt:
        print("\n\U0001F44B Session terminée.")
