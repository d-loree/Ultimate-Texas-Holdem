def place_bet(player, amount, bet_type):
    if player.can_afford(amount):
        player.remove_chips(amount)
        player.bets[bet_type] += amount
        return True
    return False
