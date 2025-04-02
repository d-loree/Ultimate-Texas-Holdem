# Handles deck functions

import os
import random

CARD_DIR = "assets/cards"

def get_random_card():
    """Returns the file path of a random card image from the assets/cards directory."""
    if not os.path.exists(CARD_DIR):
        print(f"Error: Card directory '{CARD_DIR}' not found!")
        return None

    card_files = [f for f in os.listdir(CARD_DIR) if f.endswith(".png") and f != "card_back.png"]
    
    if not card_files:
        print("Error: No card images found in the directory!")
        return None

    return os.path.join(CARD_DIR, random.choice(card_files))



def deal_player_cards():
    card_1 = get_random_card()
    card_2 = get_random_card()
    player_cards = card_1, card_2
    return card_1, card_2


def deal_communityThree_cards():
    card_1 = get_random_card()
    card_2 = get_random_card()
    card_3 = get_random_card()
    return card_1, card_2, card_3


def deal_communityTwo_cards():
    card_4 = get_random_card()
    card_5 = get_random_card()
    return card_4, card_5
