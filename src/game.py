from src import deck, player

from collections import Counter

GAME_ROUNDS = ["Bets", "Pre-Flop", "Flop", "Turn/River", "Showdown"]
current_round = 0 

player_cards = []
dealer_cards = []
community_cards = []

PAYOUT_TABLE = {
    10: 500,   # Royal Flush
    9: 50,     # Straight Flush
    8: 10,     # Four of a Kind
    7: 3,      # Full House
    6: 2,      # Flush
    5: 1,      # Straight
    4: 0,      # Three of a Kind or less = push on blind
    3: 0,
    2: 0,
    1: 0
}

def resolve_game():
    winner, hand_rank = determine_who_wins()
    print(f"{winner.upper()} wins with {hand_rank_to_string((hand_rank,))}!")

    ante = player.get_ante_chips()
    blind = player.get_blind_chips()
    play = player.get_play_chips()
    payout_multiplier = PAYOUT_TABLE.get(hand_rank, 0)
    print("Payout Multiplier: ")
    print(payout_multiplier)

    if winner == "dealer":
        # Player loses everything
        print("Dealer wins. Player loses all bets.")
        player.clear_all_bets()

    elif winner == "tie":
        # Return bets
        print("It's a tie. Bets returned.")
        player.add_chips(ante + blind + play)
        player.clear_all_bets()

    elif winner == "player":
        print("Player wins!")
        # Ante and Play both pay 1:1
        total_win = ante * 2 + play * 2

        # Blind only pays if rank >= 5 (Straight or better)
        if hand_rank >= 5:
            total_win += blind * PAYOUT_TABLE[hand_rank]
        else:
            total_win += blind  # Blind is pushed (returned)

        player.add_chips(total_win)
        player.clear_all_bets()


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
    global current_round, player_cards, dealer_cards, community_cards
    current_round = 0
    player_cards = []
    dealer_cards = []
    community_cards = []

# Return player hands
def draw_starter_hands():
    global player_cards, dealer_cards
    player_cards = [deck.get_random_card(), deck.get_random_card()]
    dealer_cards = [deck.get_random_card(), deck.get_random_card()]
    return player_cards

def draw_flop_hands():
    global community_cards
    community_cards = [deck.get_random_card() for _ in range(3)]
    return community_cards

def draw_turn_slash_river():
    global community_cards
    community_cards.append(deck.get_random_card())  # Turn
    community_cards.append(deck.get_random_card())  # River
    return community_cards

def get_dealer_cards():
    return dealer_cards

# Determine the winner
def determine_who_wins():
    player_best_hand = best_poker_hand(player_cards + community_cards)
    dealer_best_hand = best_poker_hand(dealer_cards + community_cards)

    if player_best_hand > dealer_best_hand:
        return ("player", player_best_hand[0])
    elif dealer_best_hand > player_best_hand:
        return ("dealer", dealer_best_hand[0])
    else:
        return ("tie", player_best_hand[0])

# Function to rank a hand
def best_poker_hand(cards):
    """
    Takes 7 cards (2 hole cards + 5 community cards) and returns the best hand ranking.
    The ranking is a tuple sorted by strength (higher tuple = better hand).
    """
    ranks = {"2": 0, "3": 1, "4": 2, "5": 3, "6": 4, "7": 5, "8": 6, "9": 7, "10": 8,
             "J": 9, "Q": 10, "K": 11, "A": 12}
    suits = "cdhs"


    formatted_cards = []
    for card in cards:
        parts = card.split("_")
        rank = parts[0] if parts[0] != "ace" and parts[0] != "jack" and parts[0] != "queen" and parts[0] != "king" else parts[0][0].upper()
        suit = parts[-1][0] 
        formatted_cards.append((rank, suit))

  
    rank_values = sorted([ranks[rank] for rank, suit in formatted_cards], reverse=True)

    
    rank_counts = Counter(rank_values)
    rank_sorted = sorted(rank_counts.items(), key=lambda x: (-x[1], -x[0]))  

  
    suit_counts = Counter(suit for rank, suit in formatted_cards)

    # Check for flush (5 of the same suit)
    flush = None
    for suit, count in suit_counts.items():
        if count >= 5:
            flush = sorted([ranks[rank] for rank, s in formatted_cards if s == suit], reverse=True)

    straight = None
    unique_ranks = sorted(set(rank_values), reverse=True)
    for i in range(len(unique_ranks) - 4):
        if unique_ranks[i] - unique_ranks[i + 4] == 4:
            straight = unique_ranks[i:i + 5]
            break

    # Royal Flush
    if flush and set(flush[:5]) == {ranks["10"], ranks["J"], ranks["Q"], ranks["K"], ranks["A"]}:
        return (10,)

    # Straight Flush
    if flush and straight and set(straight).issubset(set(flush)):
        return (9, max(straight))

    # Four of a Kind
    if rank_sorted[0][1] == 4:
        return (8, rank_sorted[0][0], rank_sorted[1][0])

    # Full House
    if rank_sorted[0][1] == 3 and rank_sorted[1][1] >= 2:
        return (7, rank_sorted[0][0], rank_sorted[1][0]) 

 
    if flush:
        return (6, flush[:5])  


    if straight:
        return (5, max(straight))  


    # Three of a Kind
    if rank_sorted[0][1] == 3:
        return (4, rank_sorted[0][0], rank_sorted[1][0], rank_sorted[2][0])  


    # Two Pair
    if rank_sorted[0][1] == 2 and rank_sorted[1][1] == 2:
        return (3, rank_sorted[0][0], rank_sorted[1][0], rank_sorted[2][0])  


    # One Pair
    if rank_sorted[0][1] == 2:
        return (2, rank_sorted[0][0], rank_sorted[1][0], rank_sorted[2][0], rank_sorted[3][0])  


    # High Card
    return (1, rank_sorted[0][0], rank_sorted[1][0], rank_sorted[2][0], rank_sorted[3][0], rank_sorted[4][0])  


def hand_rank_to_string(rank_tuple):
    rank_labels = {
        10: "Royal Flush",
        9: "Straight Flush",
        8: "Four of a Kind",
        7: "Full House",
        6: "Flush",
        5: "Straight",
        4: "Three of a Kind",
        3: "Two Pair",
        2: "One Pair",
        1: "High Card"
    }
    return rank_labels[rank_tuple[0]]

