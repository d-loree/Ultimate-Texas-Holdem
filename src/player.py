# Handles player logic

import json
import os
from dotenv import load_dotenv

load_dotenv()

PLAYER_FILE = "player.json"
DEFAULT_CHIPS = int(os.getenv("DEFAULT_CHIPS", 10000))

# Load player data from file or create default
def load_player_data():
    try:
        with open(PLAYER_FILE, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}

    if "chips" not in data:
        data["chips"] = DEFAULT_CHIPS
        save_player_data(data)

    return data

# Save player data to file
def save_player_data(data):
    with open(PLAYER_FILE, "w") as file:
        json.dump(data, file)

# Get current chip count
def get_chips():
    return load_player_data()["chips"]

# Set chip count and save
def set_chips(value):
    data = load_player_data()
    data["chips"] = int(value)
    save_player_data(data)

# Reset chips to default value
def reset_chips():
    set_chips(DEFAULT_CHIPS)
