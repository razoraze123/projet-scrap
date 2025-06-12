import sys
import argparse
from bs4 import BeautifulSoup
from intelligence import analyser_question
from css_selector_generator import build_selector
from src.memoire_generale import ajouter_interaction


_LABEL_TAGS = {
    "lien": ["a"],
    "titre": ["h1", "h2", "h3", "h4", "h5", "h6"],
    "image": ["img"],
    "texte": ["p", "div"],
    "bouton": ["button"],
}

def trouver_elements(soup: BeautifulSoup, label: str):
    tags = _LABEL_TAGS.get(label, None)
    if tags:
        return soup.find_all(tags)
    return soup.find_all(True)

def choisir_meilleur(elements):
    if not elements:
        return None
    return max(elements, key=lambda el: len(el.get_text(strip=True)))

def generer_selecteur(html: str, question: str) -> str:
    label = analyser_question(question)
    soup = BeautifulSoup(html, "html.parser")
    elements = trouver_elements(soup, label)
    cible = choisir_meilleur(elements)
    if cible is None:
        return ""
    selector = build_selector(cible)
    try:
        ajouter_interaction(
            "prediction",
            {"question": question, "html": html, "reponse": selector},
        )
    except Exception:
        pass
    return selector

def main():
    parser = argparse.ArgumentParser(
        description="Detecteur intelligent de selecteur CSS"
    )
    parser.add_argument("question", help="Question en langage naturel")
    parser.add_argument("file", nargs="?", help="Fichier HTML, default stdin")
    args = parser.parse_args()

    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            html = f.read()
    else:
        html = sys.stdin.read()

    ajouter_interaction("texte_libre", {"message": args.question})
    try:
        selector = generer_selecteur(html, args.question)
        ajouter_interaction("reponse", {"texte": selector})
    except Exception as e:
        ajouter_interaction("erreur", {"exception": str(e)})
        raise
    print(selector)

if __name__ == "__main__":
    main()
