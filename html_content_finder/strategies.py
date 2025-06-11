"""Scoring strategies for detecting the main content element."""
from __future__ import annotations

from bs4.element import Tag, NavigableString

DEFAULT_CONTENT_KEYWORDS = ["rte", "content", "desc", "description", "prose", "article-body"]

SEMANTIC_POSITIVE = {"article": 5, "main": 5, "section": 2}
SEMANTIC_NEGATIVE = {"nav": -5, "header": -5, "footer": -5, "aside": -5}

INLINE_TAGS = ["span", "b", "i", "strong", "em", "a"]
GENERIC_CLASSES = ["tabcontent", "container", "wrapper", "header", "footer", "nav"]

class Strategy:
    """Base class for scoring strategies."""

    def score(self, element: Tag) -> float:
        raise NotImplementedError

class KeywordStrategy(Strategy):
    """Scores elements based on presence of keywords in class or id."""

    def __init__(self, keywords: list[str]):
        self.keywords = [kw.lower() for kw in keywords]

    def score(self, element: Tag) -> float:
        score = 0.0
        classes = " ".join(element.get("class", [])).lower()
        element_id = (element.get("id") or "").lower()
        for kw in self.keywords:
            if kw in classes:
                score += 5
                if any(c == kw for c in element.get("class", [])):
                    score += 3
            if kw in element_id:
                score += 5
                if element_id == kw:
                    score += 3
        return score

class SemanticTagStrategy(Strategy):
    """Scores semantic HTML5 tags positively or negatively."""

    def score(self, element: Tag) -> float:
        score = 0.0
        score += SEMANTIC_POSITIVE.get(element.name, 0)
        score += SEMANTIC_NEGATIVE.get(element.name, 0)
        return score

class DensityStrategy(Strategy):
    """Scores elements based on text density."""

    def score(self, element: Tag) -> float:
        text_parts = []
        for child in element.children:
            if isinstance(child, NavigableString):
                text_parts.append(str(child))
        direct_text = "".join(text_parts).strip()
        if not direct_text:
            return 0.0
        html_length = len(str(element))
        ratio = len(direct_text) / html_length if html_length else 0
        return ratio * 10

class StructureStrategy(Strategy):
    """Penalises elements that mostly contain navigation or form elements."""

    NAV_FORM_TAGS = {"a", "input", "button", "select", "option", "form"}

    def score(self, element: Tag) -> float:
        child_tags = [child.name for child in element.find_all(True, recursive=False)]
        if not child_tags:
            return 0.0
        nav_count = sum(1 for t in child_tags if t in self.NAV_FORM_TAGS)
        ratio = nav_count / len(child_tags)
        return -ratio * 10
