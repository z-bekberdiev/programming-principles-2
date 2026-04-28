import json
import os
import pathlib

ASSETS_DIR = f"{pathlib.Path(__file__).parent}/assets"
SETTINGS_FILE = os.path.join(ASSETS_DIR, "settings.json")
LEADERBOARD_FILE = os.path.join(ASSETS_DIR, "leaderboard.json")

# Default settings
DEFAULT_SETTINGS = {
    "sound": True,
    "car_color": [50, 200, 50],
    "difficulty": "Normal"
}

def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS
    with open(SETTINGS_FILE, "r") as f:
        return json.load(f)

def save_settings(settings):
    os.makedirs(ASSETS_DIR, exist_ok=True)
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)

def load_leaderboard():
    if not os.path.exists(LEADERBOARD_FILE):
        save_leaderboard([])
        return []
    with open(LEADERBOARD_FILE, "r") as f:
        return json.load(f)

def save_leaderboard(leaderboard):
    os.makedirs(ASSETS_DIR, exist_ok=True)
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(leaderboard, f, indent=4)

def add_score(name, score, distance):
    leaderboard = load_leaderboard()
    leaderboard.append({"name": name, "score": score, "distance": distance})
    leaderboard = sorted(leaderboard, key=lambda x: x["score"], reverse=True)[:10]
    save_leaderboard(leaderboard)