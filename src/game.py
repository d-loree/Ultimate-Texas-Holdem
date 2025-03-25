# Handles game state and round tracking
from src import deck

GAME_ROUNDS = ["Bets", "Pre-Flop", "Flop", "Turn/River", "Showdown"]
current_round = 0 

player_cards = []
dealer_cards = []
community_cards = []

# Get the current round name
def get_current_round():
    return GAME_ROUNDS[current_round]

# Move to the next round
def next_round():
    global current_round
    if current_round < len(GAME_ROUNDS) - 1:
        current_round += 1
    return get_current_round()

# Reset the game round
def reset_round():
    global current_round
    current_round = 0

# Return player hands
def draw_starter_hands():
    for i in range(1, 5):
        if i % 2 == 0:
            dealer_cards.append(deck.get_random_card())
        else:
            player_cards.append(deck.get_random_card())
    return player_cards

def draw_flop_hands():
    for i in range(1, 4):
        community_cards.append(deck.get_random_card())
    return community_cards
        
def draw_turn_slash_river():
    for i in range(1, 3):
        community_cards.append(deck.get_random_card())
    return community_cards
        
def get_dealer_cards():
    return dealer_cards




def determine_who_wins():
    pass