import unittest
from blackjack import Blackjack, Deck
from collections import namedtuple

class TestSplit(unittest.TestCase):
        
    def setUp(self):
        self.game = Blackjack(["Alfredo"], 1000)  # Create a game with one player
        self.player = self.game.players[0]
        Card = namedtuple('Card', ['suit', 'rank'])
        card1 = Card("♠","A")
        card2 = Card("♥", "A")
        self.player.hands = [[card1, card2]]  # Two aces to begin with
        self.player.bets = [100]  # Assume initial bet of 100

    def test_split(self):
        # Print initial state
        print("Initial hands:", self.player.hands)
        
        # Check if player can split and print the result
        can_split = self.player.can_split()
        print("Can split:", can_split)
        self.assertTrue(self.player, "Player should be able to split a pair of Aces")
        
        # Perform the split
        self.player.split()

        # Print state after splitting
        print("Hands after split:", self.player.hands)
        
        # Assert the number of hands after split
        self.assertEqual(len(self.player.hands), 2, "Player should have two hands after splitting")

        # Check if the bet for each hand is correct
        self.assertEqual(self.player.bets[0], 100, "First hand bet should remain 100 after splitting")
        self.assertEqual(self.player.bets[0], 100, "Second hand bet should be 100 after splitting")

# Start test 
if __name__ == '__main__':
    unittest.main()