from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
MODEL_DIR = BASE_DIR / "model"

# Dataset paths
INTENTS_FILE = DATA_DIR / "intents.jsonl"
HTML_SELECTOR_FILE = DATA_DIR / "html_selector_dataset.jsonl"
HTML_ONLY_SELECTOR_FILE = DATA_DIR / "dataset_with_selector.csv"

# Model directories
CLASSIFIER_MODEL_DIR = MODEL_DIR / "trained_model"
HTML_SELECTOR_MODEL_DIR = MODEL_DIR / "html_selector"
HTML_ONLY_SELECTOR_MODEL_DIR = MODEL_DIR / "html_only_selector"

# Training hyperparameters
TRAIN_EPOCHS = 5
TRAIN_BATCH_SIZE = 8
LEARNING_RATE = 5e-5

# Flask configuration
FLASK_DEBUG = True
FLASK_HOST = "127.0.0.1"
FLASK_PORT = 5000
