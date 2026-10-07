import json
from pathlib import Path

ENVIRONMENT_FILE = Path("data/environments.json")

def load_environments():
    if not ENVIRONMENT_FILE.exists():
        return []
    return json.loads(ENVIRONMENT_FILE.read_text())

def add_environment(label: str, emoji: str):
    environments = load_environments()
    environment_id = label.lower().replace(" ", "_")

    if any(m["id"] == environment_id for e in environments):
        return  # déjà présent

    environments.append({
        "id": mood_id,
        "label": label,
        "emoji": emoji
    })

    ENVIRONMENT_FILE.write_text(json.dumps(moods, indent=2, ensure_ascii=False))
