# NOTICE (FR)

Ce fichier récapitule rapidement les étapes principales du projet.

1. Installez les dépendances :

    ```bash
    pip install -r requirements.txt
    ```

2. Vérifiez la présence des jeux de données dans `data/`.

3. Lancez l'entraînement des modèles :

    ```bash
    python -m src.train_classifier
    python -m src.train_html_selector_model
    ```
    (les commandes `python cli.py train-classifier` et
    `python cli.py train-selector` sont équivalentes)

    Les fichiers générés seront sauvegardés dans `model/`.

4. Le script `cli.py` permet de générer le dataset,
   d'entraîner les modèles et de lancer le serveur.
