Ce dépôt vise l'extraction automatique d'éléments HTML à l'aide de sélecteurs CSS. On y trouve des scripts Python et Node.js pour générer des jeux de données, entraîner des modèles et tester la prédiction des sélecteurs.

Structure générale
------------------
- **data/** : jeux de données JSONL/CSV.
- **src/** : code Python pour l'entraînement et l'inférence.
- **templates/** et **static/** : petits fichiers pour l'interface Flask.
- Divers scripts à la racine (JS, Python) pour générer/valider les jeux de données et tester l'IA.

Principaux fichiers
-------------------
- `css_selector_generator.py` : heuristiques pour créer un sélecteur à partir d'un bloc HTML.
- `detect_selector.py` et `detecteur.py` : versions plus complètes utilisant ces heuristiques et/ou un modèle de compréhension de questions.
- `intelligence.py` : pipeline zero‑shot DistilBERT pour transformer une question en label (lien, titre, image...).
- `web_interface.py` / `interface_test.py` : interfaces Flask ou console pour tester la génération.
- `generate_dataset.py`, `clean_dataset.js`, `generate_selectors.js`… : scripts de génération d'ensembles {html, selector}.
- `convert_jsonl_to_csv.py` : conversion en CSV.
- `src/train_classifier.py` : entraînement du classifieur DistilBERT sur `data/intents.jsonl`.
- `src/train_html_selector_model.py` : entraînement d'un modèle DistilBERT prenant `[QUESTION] ... [HTML] ...` comme entrée et produisant le sélecteur cible.

Jeux de données
---------------
- `dataset.jsonl` / `dataset_clean.jsonl` : blocs HTML générés aléatoirement.
- `dataset_with_selector_multi.jsonl` : paires {html, selector} créées automatiquement (5 445 lignes).
- `dataset_with_selector.csv` : même contenu au format CSV (5 446 lignes avec l'en‑tête).
- `html_selector_dataset.jsonl` : 600 exemples associant question, HTML et sélecteur correct pour entraîner le modèle de sélection.
- `intents.jsonl` : 180 phrases en français annotées avec le label (titre, bouton, lien, …).

Lancement d’un entraînement
---------------------------
1. Installer les dépendances :
   ```bash
   pip install -r requirements.txt
   ```
2. Vérifier/obtenir les jeux de données générés (`data/`).
3. Entraîner le classifieur de questions :
   ```bash
   python src/train_classifier.py
   ```
4. Entraîner le modèle question + HTML → sélecteur :
   ```bash
   python src/train_html_selector_model.py
   ```
   Les modèles et tokenizers sont enregistrés dans `model/`.

Points de vigilance
-------------------
- Les scripts Node.js nécessitent `npm install` pour `css-selector-generator` et `jsdom` si l'on souhaite régénérer les sélecteurs.
- Les fichiers `auto`, `book`, `camera` sont vides et servent seulement d'exemple de noms de pages.
- Le projet s’appuie sur DistilBERT (HuggingFace). En cas de nouvelle collecte de données, penser à mettre à jour les jeux de données dans `data/` avant relancer l'entraînement.
