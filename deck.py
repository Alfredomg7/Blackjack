import random

class Deck:

    # Define the suits and face cards for a standard deck
    suits = ["♣","♦","♥","♠"]
    face_cards = ["A","J","Q","K"]
    
    def __init__(self):
        # Create a deck of cards using list comprehensions
        self.deck = [(suit, str(rank)) for suit in self.suits for rank in range(2, 11)] + [(suit, face) for suit in self.suits for face in self.face_cards]
    
    def print_deck(self):
        # Print each card in the deck
        for card in self.deck:
            print(f"{card[1]}{card[0]}", end=" ")
        print("\n\n")
    
    def shuffle(self):
        # Shuffle the deck using the random.shuffle() function
        random.shuffle(self.deck)

    def hit(self):
        # Remove and return a card from the top of the deck
        return self.deck.pop()
    
    def deal(self):
        # Deal two cards (as a tuple) from the top of the deck
        card_1 = self.deck.pop()
        card_2 = self.deck.pop()
        return card_1, card_2
    
    def is_empty(self):
        # Check if deck list is empty
        return len(self.deck) == 0
