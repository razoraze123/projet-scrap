# Assistant HTML IA

Ce projet propose un petit assistant capable de comprendre des requêtes en langage naturel ("Quel est le titre ?", "Montre-moi l'image", etc.) et d'indiquer quel élément HTML est visé. Un modèle DistilBERT est entraîné localement pour classer les demandes parmi six labels : `titre`, `bouton`, `image`, `prix`, `lien`, `description`.

## Installation

Installez les dépendances :

```bash
pip install -r requirements.txt
```

## Entraîner le modèle

Le dataset se trouve dans `data/intents.jsonl`. Lancez l'entraînement (CPU) :

```bash
python src/train_classifier.py
```

Le modèle et le tokenizer seront sauvegardés dans `model/trained_model/`.

## Tester en ligne de commande

```bash
python src/predictor.py "Montre-moi le prix"
```

## Interface graphique

Une interface minimaliste est disponible :

```bash
python src/interface_gui.py
```

Entrez une question et cliquez sur **Prédire** : le label prédit s'affichera.
