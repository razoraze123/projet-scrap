from pathlib import Path
import sys
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from css_selector_generator import is_dynamic_id, build_selector


def test_is_dynamic_id():
    assert is_dynamic_id("item12345")
    assert not is_dynamic_id("header")


def test_build_selector_with_id():
    html = "<div id='main'><span>Text</span></div>"
    soup = BeautifulSoup(html, "html.parser")
    selector = build_selector(soup.div)
    assert selector == "#main"
