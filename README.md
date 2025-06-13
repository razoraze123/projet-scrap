# Assistant HTML IA

Ce projet propose un petit assistant capable de comprendre des requêtes en langage naturel ("Quel est le titre ?", "Montre-moi l'image", etc.) et d'indiquer quel élément HTML est visé. Un modèle DistilBERT est entraîné localement pour classer les demandes parmi six labels : `titre`, `bouton`, `image`, `prix`, `lien`, `description`.

## Installation

Installez les dépendances :

```bash
pip install -r requirements.txt
```

### Utilisation de la CLI

Toutes les actions principales sont accessibles via `cli.py` :

```bash
python cli.py generate         # génère un dataset HTML
python cli.py train-classifier # entraîne le classifieur
python cli.py train-selector   # entraîne le modèle de sélecteur
python cli.py predict-selector-html page.html # prédit le sélecteur
python cli.py serve            # lance le serveur Flask
```

## Entraîner le modèle

Le dataset se trouve dans `data/intents.jsonl`. Lancez l'entraînement (CPU) :

```bash
python -m src.train_classifier
```

Cette commande peut aussi être exécutée via `python cli.py train-classifier`.

Le modèle et le tokenizer seront sauvegardés dans `model/trained_model/`.

## Tester en ligne de commande

```bash
python src/predictor.py "Montre-moi le prix"
cat page.html | python src/html_only_predictor.py
```

## Interface graphique

Une interface minimaliste est disponible :

```bash
python src/interface_gui.py
```

Entrez une question et cliquez sur **Prédire** : le label prédit s'affichera.

Une version utilisant **PySide6** est aussi disponible :
```bash
python src/interface_pyside6.py
```

### Interface d'apprentissage

Lancement de l'application de suivi d'entraînement :

```bash
python apprentissage_pour_ia.py --config config.yaml
```
