import sys
import re
import argparse
from typing import List, Tuple
from src.memoire_generale import ajouter_interaction
from bs4 import BeautifulSoup

# Inline and structural tags used to weight candidate elements
INLINE_TAGS = {
    "span", "i", "b", "em", "strong", "small", "label"
}

STRUCTURAL_TAGS = {
    "div", "section", "article", "nav", "main",
    "h1", "h2", "h3", "h4", "h5", "h6",
    "a", "p", "ul", "ol", "li"
}

# Tags that are too generic to rely on when building a selector
GENERIC_TAGS = {"div", "span", "li", "ul", "ol", "p"}

# Classes considered generic and usually not helpful for a selector
GENERIC_CLASSES = {
    "container", "wrapper", "wrap", "box", "block",
    "row", "col", "inner", "outer", "bold"
}

# Keywords that hint an element is interesting (title, card, ...)
POSITIVE_KEYWORDS = {
    "title", "desc", "description", "content", "card",
    "item", "nav", "link", "button"
}

def is_dynamic_id(value: str) -> bool:
    """Return True if the id looks auto-generated (contains long digits)."""
    return bool(re.search(r"\d{2,}", value)) or len(value) > 30

def has_keyword(value: str) -> bool:
    """Return True if the given string contains a positive keyword."""
    low = value.lower()
    return any(k in low for k in POSITIVE_KEYWORDS)

def is_generic(value: str) -> bool:
    """Return True if the class name is too generic."""
    return value.lower() in GENERIC_CLASSES

def compute_score(tag) -> int:
    """Score an element to estimate how good it is as a target."""
    score = 0
    name = tag.name.lower()

    if name in INLINE_TAGS:
        score -= 3
    if name in STRUCTURAL_TAGS:
        score += 2

    # Penalise very deep elements
    depth = 0
    parent = tag.parent
    while parent and parent.name != '[document]':
        depth += 1
        parent = parent.parent
    score -= depth

    # Favour elements that contain a fair amount of text
    text_length = len(tag.get_text(strip=True))
    density = text_length / (len(tag.find_all(True)) + 1)
    if text_length > 40:
        score += 2
    elif text_length > 15:
        score += 1
    if density > 30:
        score += 2
    elif density > 10:
        score += 1

    # Semantic headings have extra weight
    if name.startswith('h') and len(name) == 2 and name[1].isdigit():
        score += 2

    tag_id = tag.get("id")
    if tag_id:
        if not is_dynamic_id(tag_id):
            score += 5
            if has_keyword(tag_id):
                score += 1
        else:
            score -= 1

    classes = tag.get("class", [])
    for cls in classes:
        if is_generic(cls):
            score -= 2
        else:
            score += 3
            if has_keyword(cls):
                score += 1
    return score

def choose_best_elements(soup: BeautifulSoup, mode: str = 'all', limit: int = 3):
    """Return a list of promising elements in the snippet."""
    candidates: List[Tuple[int, any]] = []
    for el in soup.find_all(True):
        if mode == 'links' and el.name != 'a':
            continue
        if mode == 'text' and el.name not in {
            'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'
        }:
            continue
        sc = compute_score(el)
        candidates.append((sc, el))
    candidates.sort(key=lambda x: x[0], reverse=True)
    result = []
    selectors_seen = set()
    for score, el in candidates:
        candidate = refine_candidate(el)
        sel = build_selector(candidate)
        if sel in selectors_seen:
            continue
        selectors_seen.add(sel)
        result.append(candidate)
        if len(result) >= limit:
            break
    return result

def refine_candidate(el):
    """If the element contains a single anchor, return that anchor."""
    anchors = el.find_all('a', recursive=True)
    if len(anchors) == 1:
        return anchors[0]
    return el

def has_good_id(tag) -> bool:
    tag_id = tag.get("id")
    return tag_id is not None and not is_dynamic_id(tag_id)

def describe_element(elem: 'BeautifulSoup') -> str:
    """Return a short human explanation for what the element represents."""
    name = elem.name.lower()
    if name == 'a':
        return "Lien principal"
    if name in {'h1', 'h2', 'h3', 'h4', 'h5', 'h6'}:
        return "Titre de section"
    if name in {'ul', 'ol'}:
        return "Liste d'\u00e9l\u00e9ments"
    if name == 'p':
        return "Paragraphe de texte"
    return f"\u00c9l\u00e9ment {name}"

def build_selector(elem) -> str:
    """Build a short yet robust CSS selector for the element."""
    parts = []
    current = elem
    first = True
    max_levels = 4
    while current and current.name != '[document]':
        if has_good_id(current):
            # Prefer a stable id whenever possible
            parts.append(f"#{current['id']}")
            break
        classes = [c for c in current.get('class', []) if not is_generic(c)]
        if first:
            # For the candidate element keep the tag name
            if classes:
                part = current.name + ''.join(f'.{c}' for c in classes)
            else:
                part = current.name
            parts.append(part)
            first = False
        else:
            if classes:
                if current.name in GENERIC_TAGS:
                    part = ''.join(f'.{c}' for c in classes)
                else:
                    part = current.name + ''.join(f'.{c}' for c in classes)
                parts.append(part)
        current = current.parent
        if len(parts) >= max_levels:
            break
    parts.reverse()
    return ' '.join(parts)

def prompt_input() -> str:
    """Display a prompt and read HTML from stdin until EOF."""
    print(
        "\U0001F4E5 Collez ici l'extrait HTML \u00e0 analyser (puis appuyez sur Entr\u00e9e + Ctrl+Z (Windows) ou Ctrl+D (Mac/Linux)) :"
    )
    return sys.stdin.read()

def main():
    parser = argparse.ArgumentParser(
        description="Generate the most stable CSS selector from an HTML snippet"
    )
    parser.add_argument(
        "file", nargs="?", help="Optional HTML file. If omitted, read from stdin"
    )
    parser.add_argument(
        "--mode",
        choices=["auto", "links", "text", "all"],
        default="auto",
        help="Type d'\u00e9l\u00e9ments \u00e0 cibler"
    )
    args = parser.parse_args()

    if args.file:
        with open(args.file, 'r', encoding='utf-8') as f:
            html = f.read()
    else:
        html = prompt_input()
    try:
        ajouter_interaction("texte_libre", {"message": html})
    except Exception:
        pass

    soup = BeautifulSoup(html, 'html.parser')
    mode = args.mode
    search_mode = 'all' if mode == 'auto' else mode
    targets = choose_best_elements(soup, search_mode)
    if not targets:
        return
    for target in targets:
        target = refine_candidate(target)
        selector = build_selector(target)
        explanation = describe_element(target)
        try:
            ajouter_interaction(
                "prediction",
                {"html": str(target), "reponse": selector},
            )
        except Exception:
            pass
        print(f"\u2705 S\u00e9lecteur g\u00e9n\u00e9r\u00e9 : {selector}")
        print(f"\U0001F9E0 Explication : {explanation}\n")

if __name__ == '__main__':
    main()
