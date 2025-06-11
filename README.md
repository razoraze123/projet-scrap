# projet-scrap

Ce dépôt propose plusieurs outils pour faciliter le repérage de sélecteurs CSS et l'extraction de données depuis une page web.

## 1. Capture du sélecteur dans le navigateur

Chargez le fichier `selector_capture.js` dans la console de votre navigateur (Chrome/Firefox). Le script affiche un message puis attend un clic :

```javascript
// Dans la console devtools
// collez le contenu du fichier selector_capture.js
```

Cliquez ensuite sur l'élément ciblé. Le sélecteur unique est copié dans le presse‑papiers et stocké dans `window._lastCssSelector`.

## 2. Extraction avec Selenium

Le script `scraper.py` récupère le texte ou un attribut d'un élément à partir d'une URL et d'un sélecteur CSS :

```bash
python3 scraper.py "https://exemple.com" "div.article p.desc" -o resultat.csv
```

Options :

* `-a --attribute` – nom de l'attribut à extraire (par défaut, le texte interne)
* `-o --output` – fichier CSV ou XLSX de sortie

Le script utilise `webdriver-manager` pour télécharger automatiquement ChromeDriver.

## Bibliothèque historique

Les modules `html_content_finder` et `selector_utils` fournissent des fonctions avancées pour déterminer le bloc principal d'une page ou générer un sélecteur à partir d'un extrait HTML. Ils restent disponibles en complément.
