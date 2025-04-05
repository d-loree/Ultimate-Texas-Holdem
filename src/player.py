# Handles player logic

import json
import os
from dotenv import load_dotenv

load_dotenv()

PLAYER_FILE = "src/player.json"
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

    for field in ["ante_chips", "blind_chips", "play_chips"]:
        if field not in data:
            data[field] = 0

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

# Add chips to current amount
def add_chips(amount):
    current = get_chips()
    set_chips(current + int(amount))

# Remove chips from current amount - wont go below 0
def remove_chips(amount):
    current = get_chips()
    new_total = max(0, current - int(amount))
    set_chips(new_total)

def can_afford(amount):
    return get_chips() >= int(amount)

# Add specific type of chips to table
def add_ante_chips(amount):
    return _add_to_table("ante_chips", amount)

def add_blind_chips(amount):
    return _add_to_table("blind_chips", amount)

def add_play_chips(amount):
    return _add_to_table("play_chips", amount)

def _add_to_table(chip_type, amount):
    if can_afford(amount):
        data = load_player_data()
        data["chips"] -= amount
        data[chip_type] += amount
        save_player_data(data)
        return True
    return False

# Return all chips from the table back to the player
def return_chips_from_table():
    data = load_player_data()
    total_return = data["ante_chips"] + data["blind_chips"] + data["play_chips"]
    data["chips"] += total_return
    data["ante_chips"] = 0
    data["blind_chips"] = 0
    data["play_chips"] = 0
    save_player_data(data)

# Get specific chip values
def get_ante_chips():
    return load_player_data()["ante_chips"]

def get_blind_chips():
    return load_player_data()["blind_chips"]

def get_play_chips():
    return load_player_data()["play_chips"]
