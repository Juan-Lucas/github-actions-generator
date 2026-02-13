import json
from pathlib import Path

CONFIG_PATH = Path.home() / ".gha-gen-config.json"

DEFAULTS = {
    "python_version": "3.11",
    "php_version": "8.2",
    "node_version": "18",
    "default_output": ".github/workflows"
}

def load_config():
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, encoding="utf-8") as f:
            return {**DEFAULTS, **json.load(f)}
    return DEFAULTS.copy()

def save_config(data):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
