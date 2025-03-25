# Handles game state and round tracking

GAME_ROUNDS = ["Bets", "Pre-Flop", "Flop", "Turn/River", "Showdown"]
current_round = 0 

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
