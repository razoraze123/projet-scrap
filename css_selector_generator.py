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
    selector = build_selector(target)
    print(selector)

if __name__ == '__main__':
    main()
