# projet-scrap

Ce dépôt fournit un petit outil graphique permettant d'obtenir rapidement un
sélecteur CSS à partir d'un extrait de code HTML.

## Utilisation

Lancez simplement :

```bash
python3 "python css_selector_gui.py"
```

Collez le HTML concerné puis cliquez sur **Générer le Sélecteur CSS**.

### Exemple minimal

```python
from css_selector_gui import generate_css_selector_from_html

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
