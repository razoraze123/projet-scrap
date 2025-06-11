"""Utility functions for generating CSS selectors from HTML snippets."""

from __future__ import annotations

from bs4 import BeautifulSoup

# Keywords that typically identify a content block
CONTENT_KEYWORDS = ["rte", "content", "desc", "description", "prose"]
# Tags that should not appear in the selector chain
INLINE_TAGS = ["span", "b", "i", "strong", "em", "a"]
# Classes that are too generic to be useful in a selector
GENERIC_CLASSES = ["tabcontent", "container", "wrapper"]


def _has_relevant_class(element) -> bool:
    classes = element.get("class", [])
    class_str = " ".join(classes).lower()
    if not classes:
        return False
    return (
        any(kw in class_str for kw in CONTENT_KEYWORDS)
        and not any(gc in classes for gc in GENERIC_CLASSES)
    )


def _build_chain(element) -> list[str]:
    chain: list[str] = []
    el = element
    while el and el.name not in {"body", "[document]"}:
        if el.name not in INLINE_TAGS:
            tag = el.name
            classes = [c for c in el.get("class", []) if c not in GENERIC_CLASSES]
            if classes:
                tag += "." + ".".join(classes)
            chain.append(tag)
        parent = el.parent
        if not parent or any(gc in parent.get("class", []) for gc in GENERIC_CLASSES):
            break
        el = parent
    return list(reversed(chain))


def generate_css_selector_from_html(html_snippet: str) -> str:
    """Return a CSS selector targeting the most relevant element in ``html_snippet``.

    The function searches for anchor tags inside headings or inside elements
    whose class attribute contains keywords such as ``rte`` or ``description``.
    The resulting selector is constructed by combining the element and its
    ancestors while skipping inline tags and generic containers.
    """

    soup = BeautifulSoup(html_snippet, "html.parser")

    candidate = None

    # Priority 1: link inside a heading
    for heading in soup.find_all([f"h{i}" for i in range(1, 7)]):
        anchor = heading.find("a")
        if anchor:
            candidate = anchor
            break

    # Priority 2: element with relevant classes
    if candidate is None:
        for el in soup.find_all(True):
            if _has_relevant_class(el):
                candidate = el.find("a") or el
                break

    # Priority 3: first <a> tag
    if candidate is None:
        candidate = soup.find("a")

    # Fallback: first tag in the snippet
    if candidate is None:
        candidate = soup.find(True)

    chain = _build_chain(candidate)
    selector = " ".join(chain)

    # Optional alternative selector using the direct parent if different
    alt_selector = None
    parent = candidate.parent if candidate else None
    if (
        parent
        and parent.name not in INLINE_TAGS
        and not any(gc in parent.get("class", []) for gc in GENERIC_CLASSES)
    ):
        chain_alt = _build_chain(parent) + [candidate.name]
        classes = [c for c in candidate.get("class", []) if c not in GENERIC_CLASSES]
        if classes:
            chain_alt[-1] += "." + ".".join(classes)
        alt_selector = " ".join(chain_alt)

    if alt_selector and alt_selector != selector:
        return selector + "\n" + alt_selector
    return selector
