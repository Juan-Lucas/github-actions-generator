import json
from pathlib import Path

STATS_PATH = Path.home() / ".gha-gen-stats.json"

def load_stats():
    if STATS_PATH.exists():
        with open(STATS_PATH, encoding="utf-8") as f:
            return json.load(f)
    return {"total": 0, "templates": {}}

def save_stats(stats):
    with open(STATS_PATH, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2)

def increment_template(template):
    stats = load_stats()
    stats["total"] += 1
    stats["templates"][template] = stats["templates"].get(template, 0) + 1
    save_stats(stats)
