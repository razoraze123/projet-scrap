"""Analyse d'une question en langage naturel."""

from transformers import pipeline

MODEL_NAME = "distilbert-base-multilingual-cased"
LABELS = ["titre", "description", "prix", "image", "lien", "bouton"]

_classifier = pipeline("zero-shot-classification", model=MODEL_NAME)

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
