import random
from collections import namedtuple

# Define a namedtuple for card representation
Card = namedtuple('Card', ['suit', 'rank'])

class Deck:
    # Define the suits and face cards for a standard deck
    SUITS = ["♣", "♦", "♥", "♠"]
    FACE_CARDS = ["A", "J", "Q", "K"]
    RANKS = list(map(str, range(2, 11))) + FACE_CARDS  # Ranks now include number and face cards
    MIN_RANK = 2  # Minimum rank value for cards
    MAX_RANK = 11  # Maximum rank value for cards, assuming Ace counts as 11 initially
    
    def __init__(self):
        # Create and shuffle a new deck of cards
        self.reinitialize_deck()
    
    def __repr__(self):
        # Return a string representation of the deck
        return ' '.join(f"{card.suit}{card.rank}" for card in self.deck) + "\n\n"
    
    def shuffle(self):
        # Shuffle the deck using the random.shuffle() function
        random.shuffle(self.deck)

    def hit(self):
        # Remove and return a card from the top of the deck
        return self.deck.pop()
    
    def deal(self):
        # Ensure there are at least 2 cards to deal
        while self.is_empty():
            print("New Deck is being used")
            self.reinitialize_deck()

        # Deal two cards (as a tuple) from the top of the deck
        card_1 = self.deck.pop()
        card_2 = self.deck.pop()
        return card_1, card_2

    def is_empty(self):
        # Check if deck list is empty
        return len(self.deck) < 2
    
    def reinitialize_deck(self):
        # Reinitialize the deck to a full deck of 52 cards and shuffle
        self.deck = [Card(suit, rank) for suit in Deck.SUITS for rank in Deck.RANKS]
        self.shuffle()


if __name__ == "__main__":
    deck = Deck()
    print(deck)