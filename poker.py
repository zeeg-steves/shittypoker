class Player:
    def __init__(self, name):
        self.name = name

class BotPlayer(Player):
    def __init__(self, name):
        super().__init__(name)

def get_player_name():
    name = input("Enter your name: ")
    return name

def get_bot_count():
    while True:
        try:
            bot_count = int(input("Enter the number of bot players: "))
            if bot_count < 1:
                print("Please enter a valid number of bot players (1 or more).")
            else:
                return bot_count
        except ValueError:
            print("Invalid input. Please enter a valid number.")

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
    def __eq__(self, other):
        if isinstance(other, Card):
            return self.rank == other.rank and self.suit == other.suit
        return False

class Deck:
    def __init__(self):
        self.ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.suits = ['♠', '♥', '♦', '♣']
        self.cards = [Card(rank, suit) for rank in self.ranks for suit in self.suits]
    
    def shuffle(self):
        import random
        random.shuffle(self.cards)

def deal_hole_cards(deck, player, bot_players):
    player.hole_cards = [deck.cards.pop(), deck.cards.pop()]
    for bot in bot_players:
        bot.hole_cards = [deck.cards.pop(), deck.cards.pop()]

def deal_flop(deck):
    burned_card = deck.cards.pop(0)  # Burn the first card
    flop_cards = [deck.cards.pop() for _ in range(3)]
    return flop_cards

def deal_turn(deck):
    burned_card = deck.cards.pop(0)  # Burn another card
    turn_card = deck.cards.pop()
    return turn_card

def deal_river(deck):
    burned_card = deck.cards.pop(0)  # Burn another card
    river_card = deck.cards.pop()
    return river_card

def display_hands(player, bots, community_cards):
    for bot in bots:
        bot.hand = bot.hole_cards + community_cards
    player.hand = player.hole_cards + community_cards

    print("\nPlayers' hands:")
    print(f"{player.name}'s hand: {' '.join([card.rank + card.suit for card in player.hand])}")
    for bot in bots:
        print(f"{bot.name}'s hand: {' '.join([card.rank + card.suit for card in bot.hand])}")

from collections import Counter

def evaluate_hand(hand):
    HIGH_CARD = 0
    ONE_PAIR = 1
    TWO_PAIR = 2
    THREE_OF_A_KIND = 3
    STRAIGHT = 4
    FLUSH = 5
    FULL_HOUSE = 6
    FOUR_OF_A_KIND = 7
    STRAIGHT_FLUSH = 8
    
    VALUES = "23456789TJQKA"
    SUITS = "♥♠♣♦"
    
    values = [card[0] if card[0] != '10' else 'T' for card in hand]
    suits = [card[1] for card in hand]
    
    value_counts = Counter(values)
    suit_counts = Counter(suits)
    
    is_flush = len(suit_counts) == 1
    values_sorted_indices = sorted([VALUES.index(value) for value in values])
    is_straight = values_sorted_indices in (
        [0, 1, 2, 3, 4], list(range(min(values_sorted_indices), max(values_sorted_indices) + 1))
    )
    
    if is_straight and is_flush:
        return STRAIGHT_FLUSH, values_sorted_indices
    elif value_counts.most_common(1)[0][1] == 4:
        return FOUR_OF_A_KIND, values_sorted_indices
    elif value_counts.most_common(1)[0][1] == 3 and value_counts.most_common(2)[1][1] == 2:
        return FULL_HOUSE, values_sorted_indices
    elif is_flush:
        return FLUSH, values_sorted_indices
    elif is_straight:
        return STRAIGHT, values_sorted_indices
    elif value_counts.most_common(1)[0][1] == 3:
        return THREE_OF_A_KIND, values_sorted_indices
    elif value_counts.most_common(1)[0][1] == 2 and value_counts.most_common(2)[1][1] == 2:
        return TWO_PAIR, values_sorted_indices
    elif value_counts.most_common(1)[0][1] == 2:
        return ONE_PAIR, values_sorted_indices
    else:
        return HIGH_CARD, values_sorted_indices

from itertools import combinations

# Function 1: get all possible 5-card combinations from player.hand
def getcombinationsfromahand(playerhand):
    playerhandcomb = list(combinations(playerhand, 5))
    return playerhandcomb

# Function 3: get best hand out of a list of x 5-card tuples
def getbesthand(handlist):
    strongest_rank = None
    strongest_values = None
    strongest_hands = []
    converted_handlist = [ [(card.rank, card.suit) for card in hand] for hand in handlist]

        
    for hand in converted_handlist:
        rank, values = evaluate_hand(hand)

        if strongest_rank is None or rank > strongest_rank or (rank == strongest_rank and values > strongest_values):
            strongest_rank = rank
            strongest_values = values
            strongest_hands = [hand]
        elif rank == strongest_rank and values == strongest_values:
            strongest_hands.append(hand)
    
    best_hand_cards_list = []
    for hand in strongest_hands:
        best_hand_cards = [Card(rank, suit) for rank, suit in hand]
        best_hand_cards_list.append(tuple(best_hand_cards))
    return best_hand_cards_list

# Function 2: combine all players' besthand into a list of tuples
def combineallplayersbesthands(players):
    allplayerbesthands = []
    for player in players:
        player.besthand = getbesthand(getcombinationsfromahand(player.hand))[0]
        allplayerbesthands.append(player.besthand)
    return allplayerbesthands
    
import sys
        
def setup_game():
    player_name = get_player_name()
    bot_count = get_bot_count()

    player = Player(player_name)
    bots = [BotPlayer(f"Bot {i+1}") for i in range(bot_count)]

    print(f"Hello, {player_name}! You are playing against {bot_count} bot(s).")

    return player, bots

def main():
    print("Welcome to the Poker Game!")

    while True:
        while True:
            player, bots = setup_game()

            deck = Deck()
            deck.shuffle()

            deal_hole_cards(deck, player, bots)

            print(f"\nYour hole cards: {player.hole_cards[0].rank}{player.hole_cards[0].suit}, {player.hole_cards[1].rank}{player.hole_cards[1].suit}")

            #continue_play = input("\nDo you want to continue? (y/n): ")
            #if continue_play.lower() != 'y':
            #    break

            flop_cards = deal_flop(deck)
            print(f"Flop cards: {', '.join([card.rank + card.suit for card in flop_cards])}")

            #continue_play = input("\nDo you want to continue? (y/n): ")
            #if continue_play.lower() != 'y':
            #    break

            turn_card = deal_turn(deck)
            flop_and_turn = flop_cards + [turn_card]
            print(f"Turn card: {turn_card.rank + turn_card.suit}")
            print(f"Community cards: {', '.join([card.rank + card.suit for card in flop_and_turn])}")

            #continue_play = input("\nDo you want to continue? (y/n): ")
            #if continue_play.lower() != 'y':
            #    break

            river_card = deal_river(deck)
            community_cards = flop_and_turn + [river_card]
            print(f"River card: {river_card.rank + river_card.suit}")
            print(f"Community cards: {', '.join([card.rank + card.suit for card in community_cards])}")

            #continue_play = input("\nDo you want to continue? (y/n): ")
            #if continue_play.lower() != 'y':
            #    break

            display_hands(player, bots, community_cards)
            
            allplayers = [player] + bots
            
            final_result = getbesthand(combineallplayersbesthands(allplayers))

            print("All players' best hands:")
            for idx, player in enumerate(allplayers):
                print(f"{player.name}: {', '.join([card.rank + card.suit for card in player.besthand])}")
            print(f"Final result: {', '.join([card.rank + card.suit for card in final_result[0]])}")

            winning_players = []
            for result in final_result:
                for player in allplayers:
                    if sorted(player.besthand, key=lambda card: (card.rank, card.suit)) == sorted(result, key=lambda card: (card.rank, card.suit)):
                        winning_players.append(player)

            winners = ', '.join([player.name for player in winning_players])
            print(f"{winners} win(s) with the hand: {', '.join([card.rank + card.suit for card in final_result[0]])}")

            new_game = input("\nDo you want to start a new game? (y/n): ")
            if new_game.lower() != 'y':
                print("\nExiting the game. Thanks for playing!")
                sys.exit()

        print("\nStarting a new game...\n")

if __name__ == "__main__":
    main()