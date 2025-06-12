from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any


BASE_DIR = Path(__file__).resolve().parents[1]


def ajouter_interaction(type: str, contenu: Dict[str, Any], fichier: str = "data/historique.jsonl") -> None:
    """Ajoute une interaction dans le fichier JSONL."""
    entry = {"type": type, "timestamp": datetime.utcnow().isoformat(), "contenu": contenu}
    path = BASE_DIR / fichier
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        json.dump(entry, f, ensure_ascii=False)
        f.write("\n")


def charger_historique(fichier: str = "data/historique.jsonl") -> List[Dict[str, Any]]:
    """Charge toutes les interactions du fichier JSONL."""
    path = BASE_DIR / fichier
    if not path.is_file():
        return []
    interactions = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                interactions.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return interactions
