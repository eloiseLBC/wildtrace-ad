import json
from pathlib import Path

ZONE_FILE = Path("data/zone_infos.json")

def load_zones():
    if not ZONE_FILE.exists():
        return []
    return json.loads(ZONE_FILE.read_text())

def get_timezone_option(zone_id: str) -> str | None:
    zones = load_zones()
    for zone in zones:
        if zone["id"] == zone_id:
            return zone.get("timezone_option")
    return None