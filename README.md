# projet-scrap

Ce dépôt fournit un petit outil graphique permettant d'obtenir rapidement un
sélecteur CSS à partir d'un extrait de code HTML. Une bibliothèque plus
complète est également disponible pour détecter le bloc de contenu principal
dans un document.

## Utilisation de l'outil graphique

Lancez simplement :

```bash
python3 "python css_selector_gui.py"
```

Collez le HTML concerné puis cliquez sur **Générer le Sélecteur CSS**.
L'outil utilise la bibliothèque `html_content_finder` pour identifier
automatiquement le bloc de contenu principal et affiche le sélecteur robuste,
le sélecteur court et le chemin XPath.

## Utilisation de la bibliothèque

```python
from html_content_finder import ContentFinder

html_doc = """<html>...</html>"""
finder = ContentFinder(html_doc)
content_element = finder.find_content_element()

if content_element:
    print("Sélecteur robuste :", finder.get_robust_selector())
    print("Sélecteur court :", finder.get_short_selector())
    print("Chemin XPath :", finder.get_xpath())
```

### Exemple minimal

```python
from selector_utils import generate_css_selector_from_html

html = """
<div class="article">
    <p class="desc">Bonjour</p>
</div>
"""

print(generate_css_selector_from_html(html))
# affiche : "div.article p.desc"
```

L'algorithme parcourt désormais l'arbre afin de repérer la balise de contenu
la plus pertinente (classes contenant `rte`, `content`, `desc`, etc.) tout en
ignorant les conteneurs génériques tels que `container` ou `wrapper`.
