"""Main class implementing content detection logic."""
from __future__ import annotations

from bs4 import BeautifulSoup
from bs4.element import Tag
from typing import Iterable, List, Optional

from .strategies import (
    DEFAULT_CONTENT_KEYWORDS,
    GENERIC_CLASSES,
    INLINE_TAGS,
    KeywordStrategy,
    SemanticTagStrategy,
    DensityStrategy,
    StructureStrategy,
    Strategy,
)

class ContentFinder:
    """Detects the main content element of an HTML document."""

    def __init__(
        self,
        html: str,
        *,
        custom_keywords: Optional[Iterable[str]] = None,
        exclude_selectors: Optional[Iterable[str]] = None,
    ) -> None:
        """Initialize the finder.

        Parameters
        ----------
        html:
            The HTML document to analyse.
        custom_keywords:
            Additional keywords to prioritise in class or id names.
        exclude_selectors:
            CSS selectors for elements to remove before analysis.
        """
        self.soup = BeautifulSoup(html, "html.parser")
        self.keywords = list(DEFAULT_CONTENT_KEYWORDS)
        if custom_keywords:
            self.keywords.extend(custom_keywords)
        self.exclude_selectors = list(exclude_selectors or [])
        for sel in self.exclude_selectors:
            for el in self.soup.select(sel):
                el.extract()

        self._strategies: List[Strategy] = [
            KeywordStrategy(self.keywords),
            SemanticTagStrategy(),
            DensityStrategy(),
            StructureStrategy(),
        ]
        self._content_element: Optional[Tag] = None

    def find_content_element(self) -> Optional[Tag]:
        """Return the element with the highest score."""
        best_el: Optional[Tag] = None
        best_score = float("-inf")
        for el in self.soup.find_all(True):
            score = 0.0
            for strat in self._strategies:
                score += strat.score(el)
            if score > best_score:
                best_score = score
                best_el = el
        self._content_element = best_el
        return best_el

    # -- Selector utilities -------------------------------------------------
    def _build_selector_chain(self, element: Tag) -> List[str]:
        chain: List[str] = []
        el = element
        while el and el.parent and el.name != "body":
            if el.name not in INLINE_TAGS:
                tag = el.name
                classes = [c for c in el.get("class", []) if c not in GENERIC_CLASSES]
                if classes:
                    tag += "." + ".".join(classes)
                chain.append(tag)
            parent = el.parent
            if any(gc in parent.get("class", []) for gc in GENERIC_CLASSES):
                break
            el = parent
        return list(reversed(chain))

    def get_robust_selector(self) -> Optional[str]:
        """Return a detailed CSS selector for the content element."""
        if not self._content_element:
            return None
        return " ".join(self._build_selector_chain(self._content_element))

    def get_short_selector(self) -> Optional[str]:
        """Return a short unique selector, using ID when possible."""
        if not self._content_element:
            return None
        el = self._content_element
        if el.get("id"):
            return f"#{el.get('id')}"
        classes = el.get("class", [])
        if classes:
            return f"{el.name}." + ".".join(classes)
        return el.name

    def get_xpath(self) -> Optional[str]:
        """Return the XPath of the content element."""
        if not self._content_element:
            return None
        path_parts = []
        el: Optional[Tag] = self._content_element
        while el is not None and isinstance(el, Tag):
            parent = el.parent
            if parent is None:
                break
            index = 1
            for sibling in parent.find_all(el.name, recursive=False):
                if sibling is el:
                    break
                index += 1
            path_parts.append(f"{el.name}[{index}]")
            el = parent if parent.name != "[document]" else None
        return "/" + "/".join(reversed(path_parts))

