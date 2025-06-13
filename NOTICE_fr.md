# NOTICE (FR)

Ce fichier récapitule rapidement les étapes principales du projet.

1. Installez les dépendances :

    ```bash
    pip install -r requirements.txt
    ```

2. Vérifiez la présence des jeux de données dans `data/`.

3. Lancez l'entraînement des modèles :

    ```bash
    python src/train_classifier.py
    python src/train_html_selector_model.py
    ```

    Les fichiers générés seront sauvegardés dans `model/`.

4. Le script `cli.py` permet de générer le dataset,
   d'entraîner les modèles et de lancer le serveur.
