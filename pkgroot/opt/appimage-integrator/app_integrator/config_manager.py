import json
from pathlib import Path

import subprocess

def get_default_download_dir():
    try:
        result = subprocess.check_output(["xdg-user-dir", "DOWNLOAD"], text=True).strip()
        return result if result else str(Path.home() / "Téléchargements")
    except Exception:
        return str(Path.home() / "Téléchargements")


CONFIG_DIR = Path.home() / ".config" / "appimage-integrator"
CONFIG_FILE = CONFIG_DIR / "config.json"

DEFAULT_CONFIG = {
    "source_dir": get_default_download_dir(),
    "target_dir": str(Path.home() / "Applications")
}

def load_config():
    if not CONFIG_FILE.exists():
        save_config(DEFAULT_CONFIG)
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def save_config(config):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

def get_config_value(key):
    config = load_config()
    return config.get(key, DEFAULT_CONFIG.get(key))

def set_config_value(key, value):
    config = load_config()
    config[key] = value
    save_config(config)
