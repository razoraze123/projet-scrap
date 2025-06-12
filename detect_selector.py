import sys
import re
import argparse
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

def choose_best_element(soup: BeautifulSoup):
    """Return the most promising element in the snippet."""
    best = None
    best_score = float('-inf')
    for el in soup.find_all(True):
        sc = compute_score(el)
        if sc > best_score:
            best_score = sc
            best = el
    return best

def refine_candidate(el):
    """If the element contains a single anchor, return that anchor."""
    anchors = el.find_all('a', recursive=True)
    if len(anchors) == 1:
        return anchors[0]
    return el

def has_good_id(tag) -> bool:
    tag_id = tag.get("id")
    return tag_id is not None and not is_dynamic_id(tag_id)

def build_selector(elem) -> str:
    """Build a short yet robust CSS selector for the element."""
    parts = []
    current = elem
    first = True
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
    args = parser.parse_args()

    if args.file:
        with open(args.file, 'r', encoding='utf-8') as f:
            html = f.read()
    else:
        html = prompt_input()

    soup = BeautifulSoup(html, 'html.parser')
    target = choose_best_element(soup)
    if target:
        target = refine_candidate(target)
    if target is None:
        return
    selector = build_selector(target)
    print(f"\u2705 S\u00e9lecteur g\u00e9n\u00e9r\u00e9 : {selector}")

if __name__ == '__main__':
    main()
