import sys
import re
import argparse
from bs4 import BeautifulSoup

INLINE_TAGS = {
    "span", "i", "b", "em", "strong", "small", "label"
}

STRUCTURAL_TAGS = {
    "div", "section", "article", "nav", "main",
    "h1", "h2", "h3", "h4", "h5", "h6",
    "a", "p", "ul", "ol", "li"
}

GENERIC_TAGS = {"div", "span", "li", "ul", "ol", "p"}

GENERIC_CLASSES = {
    "container", "wrapper", "wrap", "box", "block",
    "row", "col", "inner", "outer", "bold"
}

POSITIVE_KEYWORDS = {
    "title", "desc", "description", "content", "card",
    "item", "nav", "link", "button"
}

def is_dynamic_id(value: str) -> bool:
    """Return True if the id looks auto‑generated (contains long digits)."""
    return bool(re.search(r"\d{2,}", value)) or len(value) > 30

def has_keyword(value: str) -> bool:
    low = value.lower()
    return any(k in low for k in POSITIVE_KEYWORDS)

def is_generic(value: str) -> bool:
    return value.lower() in GENERIC_CLASSES

def compute_score(tag) -> int:
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
    parts = []
    current = elem
    first = True
    while current and current.name != '[document]':
        if has_good_id(current):
            parts.append(f"#{current['id']}")
            break
        classes = [c for c in current.get('class', []) if not is_generic(c)]
        if first:
            # candidate element - keep tag
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

def generate_selector_candidates(tag) -> list:
    """Return a list of possible CSS selectors for the given element."""
    if tag is None:
        return []

    candidates = []

    classes = tag.get('class', []) or []
    parent = tag.parent

    parent_sel = ''
    if parent and parent.name != '[document]':
        parent_sel = build_selector(parent)

    # 1. Parent context with tag only
    if parent_sel:
        candidates.append(f"{parent_sel} {tag.name}")
    else:
        candidates.append(tag.name)

    # 2. Parent classes only if available
    if parent_sel and parent:
        parent_classes = [c for c in parent.get('class', []) if not is_generic(c)]
        if parent_classes:
            pcls = ''.join(f'.{c}' for c in parent_classes)
            candidates.append(f"{pcls} {tag.name}")

    # 3. Tag with its own classes
    if classes:
        candidates.append(tag.name + ''.join(f'.{c}' for c in classes))
        candidates.append(''.join(f'.{c}' for c in classes))

    # 4. Full path including classes
    if parent_sel:
        own = tag.name
        if classes:
            own += ''.join(f'.{c}' for c in classes)
        candidates.append(f"{parent_sel} {own}")

    # 5. id selector when present
    if has_good_id(tag):
        candidates.append(f"#{tag['id']}")

    # Deduplicate while preserving order
    seen = set()
    unique = []
    for sel in candidates:
        if sel and sel not in seen:
            unique.append(sel)
            seen.add(sel)
    return unique

def explain_selector(selector: str) -> str:
    """Return a short human explanation for a CSS selector."""
    if selector.startswith('#'):
        return "Bas\u00e9 sur l'identifiant unique de l'\u00e9l\u00e9ment, tr\u00e8s fiable."
    if selector.startswith('.') and ' ' not in selector:
        return "Utilise uniquement la ou les classes : rapide mais peut correspondre \u00e0 plusieurs \u00e9l\u00e9ments."
    if ' ' in selector:
        return "Combinaison d'\u00e9l\u00e9ments pour cibler pr\u00e9cis\u00e9ment la structure."
    return "S\u00e9lecteur simple bas\u00e9 sur la balise et ses classes."

def _score_candidate(selector: str) -> float:
    """Internal heuristic to score selectors and choose the best."""
    score = 0.0
    if selector.startswith('#'):
        score += 100
    if selector and selector[0].isalpha():
        score += 5
    classes = re.findall(r'\.([\w-]+)', selector)
    for cls in classes:
        if is_generic(cls):
            score -= 8
        else:
            score += 2
    spaces = selector.count(' ')
    score += spaces  # context is usually good
    score -= 2 * spaces
    score -= len(selector) / 10
    return score

def display_choices(tag) -> None:
    """Print all selector candidates with explanations and highlight the best."""
    candidates = generate_selector_candidates(tag)
    if not candidates:
        print("Aucun s\u00e9lecteur trouv\u00e9.")
        return

    # Rank candidates and keep the top three
    ranked = sorted(candidates, key=_score_candidate, reverse=True)
    top = ranked[:3]
    best = top[0]

    print("\U0001F3AF S\u00e9lecteurs propos\u00e9s :\n")
    for idx, sel in enumerate(top, 1):
        exp = explain_selector(sel)
        print(f"{idx}. {sel}\n   \u2192 {exp}\n")
    print(f"\u2705 Choix recommand\u00e9 : {best}")

def generate_selector(html: str) -> str:
    """Return the best CSS selector for the given HTML snippet."""
    soup = BeautifulSoup(html, 'html.parser')
    target = choose_best_element(soup)
    if target:
        target = refine_candidate(target)
    if target is None:
        return ''
    return build_selector(target)

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
        html = sys.stdin.read()

    soup = BeautifulSoup(html, 'html.parser')
    target = choose_best_element(soup)
    if target:
        target = refine_candidate(target)
    if target is None:
        return

    display_choices(target)

if __name__ == '__main__':
    main()
