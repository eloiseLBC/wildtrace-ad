import json
from pathlib import Path

MOODS_FILE = Path("data/moods.json")

def load_moods():
    if not MOODS_FILE.exists():
        return []
    return json.loads(MOODS_FILE.read_text())

def add_mood(label: str, emoji: str):
    moods = load_moods()
    mood_id = label.lower().replace(" ", "_")

    if any(m["id"] == mood_id for m in moods):
        return  # déjà présent

    moods.append({
        "id": mood_id,
        "label": label,
        "emoji": emoji
    })

    MOODS_FILE.write_text(json.dumps(moods, indent=2, ensure_ascii=False))
