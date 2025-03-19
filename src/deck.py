# Handles deck functions

import os
import random

CARD_DIR = "assets/cards"

def get_random_card():
    """Returns the file path of a random card image from the assets/cards directory."""
    if not os.path.exists(CARD_DIR):
        print(f"Error: Card directory '{CARD_DIR}' not found!")
        return None

    card_files = [f for f in os.listdir(CARD_DIR) if f.endswith(".png")]
    
    if not card_files:
        print("Error: No card images found in the directory!")
        return None

    return os.path.join(CARD_DIR, random.choice(card_files))
