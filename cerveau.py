from transformers import pipeline

_classifier = None

def _get_classifier():
    global _classifier
    if _classifier is None:
        _classifier = pipeline(
            "zero-shot-classification",
            model="typeform/distilbert-base-uncased-mnli",
        )
    return _classifier

def analyser_requete(question: str) -> str:
    """Analyse la question et renvoie un mot-clé indiquant la cible."""
    classifier = _get_classifier()
    labels = ["lien", "titre", "image", "texte", "bouton"]
    result = classifier(question, labels)
    return result["labels"][0]

