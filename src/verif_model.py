"""Utility script to verify that a trained model is present and loadable."""

from pathlib import Path
from transformers import AutoTokenizer, AutoModelForSequenceClassification

MODEL_PATH = Path(__file__).resolve().parents[1] / "model" / "trained_model"

REQUIRED_FILES = [
    "config.json",
    "pytorch_model.bin",
    "tokenizer_config.json",
    "vocab.txt",
    "special_tokens_map.json",
]


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    path = MODEL_PATH
    missing = []
    for fname in REQUIRED_FILES:
        file_path = path / fname
        if not file_path.is_file():
            missing.append(fname)
    if not missing:
        rel = path.relative_to(repo_root)
        print(f"\u2705 Tous les fichiers nécessaires sont présents dans '{rel}'")
    else:
        for m in missing:
            print(f"\u274C Fichier manquant : {m}")
        print("\n\uD83D\uDCA1 Conseil : Assure-toi d'appeler `.save_pretrained()` après l'entraînement du modèle ET du tokenizer.")
        return

    try:
        AutoTokenizer.from_pretrained(path)
        AutoModelForSequenceClassification.from_pretrained(path)
        print("\n\u2705 Modèle et tokenizer chargés avec succès \u2714\ufe0f")
    except OSError as e:
        print(f"\u274C Erreur lors du chargement : {e}")
        print("\n\uD83D\uDCA1 Conseil : Vérifie le chemin absolu ou relance l'entraînement en appelant `.save_pretrained()`")


if __name__ == "__main__":
    main()
