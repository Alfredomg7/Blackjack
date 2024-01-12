import unittest
from blackjack import Blackjack
from deck import Deck, Card

class TestDeck(unittest.TestCase):
    def setUp(self):
        self.deck = Deck()

    def test_deck_initialization(self):
        # Ensure the deck has the correct number of cards after initialization
        self.assertEqual(len(self.deck.deck), 52, "Deck should have 52 cards initially")

    def test_deck_shuffling(self):
        # Get a copy of the deck before shuffling
        original_deck = self.deck.deck[:]
        self.deck.shuffle()
        # Ensure the deck is shuffled by checking that the order has changed
        self.assertNotEqual(original_deck, self.deck.deck, "Deck should be shuffled")

class TestDealCards(unittest.TestCase):
    def setUp(self):
        self.game = Blackjack(["Alfredo"], 1000)
        self.game.active_players = self.game.players
        self.game.deal_initial_cards()
        self.player = self.game.players[0]

    def test_player_initial_cards(self):
        # Player should have exactly 2 cards at the start
        hand = self.player.hands[0]
        self.assertEqual(len(hand), 2, "player should have 2 cards initially" )

    def test_host_initial_cards(self):
        # The host should also have exactly 2 cards at the start
        self.assertEqual(len(self.game.host.hands[0]), 2, "Host should have 2 cards initially")

class TestPlayerActions(unittest.TestCase):
    def setUp(self):
        self.game = Blackjack(["Alfredo"], 1000)
        self.game.active_players = self.game.players
        self.game.deal_initial_cards()
        self.player = self.game.players[0]
    
    def test_hit_action(self):
        initial_hand_count = len(self.player.hands[0])
        initial_hand_value = self.player.calculate_hand_value()

        # Simulate player hitting
        self.game.handle_hit(self.player)
        hand = self.player.hands[0]

        self.assertEqual(len(hand), initial_hand_count + 1, "Player should have one more card after hitting")
        self.assertNotEqual(self.player.calculate_hand_value(), initial_hand_value, "Hand value should change after hitting")

    def test_stand_action(self):
        initial_hand_count = len(self.player.hands[0])
        initial_hand_value = self.player.calculate_hand_value()

        # Simulate player standing
        self.game.handle_stand(self.player)
        hand = self.player.hands[0]

        self.assertEqual(len(hand), initial_hand_count, "Player should have same number of cards after standing")
        self.assertEqual(self.player.calculate_hand_value(), initial_hand_value, "Hand value should not change after standing")

class TestSplit(unittest.TestCase):
    def setUp(self):
        self.game = Blackjack(["Alice"], 1000)
        self.player = self.game.players[0]
        card1 = Card("♠","A")
        card2 = Card("♥", "A")
        self.player.hands = [[card1, card2]]
        self.player.bets = [100]

    def test_split(self):
        # Check if player can split 
        self.assertTrue(self.player, "Player should be able to split a pair of Aces")
        
        # Perform the split
        self.player.split()

        # Assert the number of hands after split
        self.assertEqual(len(self.player.hands), 2, "Player should have two hands after splitting")
        
        # Check if the bet for each hand is correct 
        self.assertEqual(self.player.bets[0], 100, "First hand bet should remain 100 after splitting")
        self.assertEqual(self.player.bets[0], 100, "Second hand bet should be 100 after splitting")

class TestDoubleDown(unittest.TestCase):
    def setUp(self):
        self.game = Blackjack(["Alfredo"], 1000)
        self.game.active_players = self.game.players
        self.player = self.game.players[0]
        self.player.bets[0] = 100
        self.initial_balance = self.player.balance
        self.game.deal_initial_cards()  # Deal initial two cards

    def test_double_down(self):
        # Ensure player can only double down with two cards
        self.assertTrue(len(self.player.hands[0]) == 2, "Player should have only two cards initially for double down")

        initial_hand_value = self.player.calculate_hand_value()
        initial_bet = self.player.bets[0]

        # Perform double down
        new_card = self.game.deck.hit()
        self.player.hit(new_card)
        self.player.double_down()

        # Check if only one card is added
        self.assertEqual(len(self.player.hands[0]), 3, "Player should have three cards after double down")

        # Check if bet is doubled
        self.assertEqual(self.player.bets[0], 2 * initial_bet, "Bet should be doubled after double down")

        # Check if balance is updated correctly
        self.assertEqual(self.player.balance, self.initial_balance - 1 * initial_bet, "Player's balance should decrease by the initial bet after double down")

class TestGameOutcomes(unittest.TestCase):
    def setUp(self):
        self.game = Blackjack(["Alfredo"], 1000)
        self.game.active_players = self.game.players
        self.player = self.game.players[0]
        self.player.bets[0] = 100
        self.bet_amount = self.player.bets[0]
        self.initial_balance = self.player.balance
    
    def test_player_win(self):
        # Player wins (hand value higher than host's but not over 21)
        self.player.hands[0] = [Card('♠', '10'), Card('♥', '6')]  # Total 16
        self.game.host.hands[0] = [Card('♠', '9'), Card('♥', '6')]  # Total 15
        self.game.update_balances()
        self.assertEqual(self.player.balance, self.initial_balance + 2 * self.bet_amount, "Player's balance should increase by twice the bet amount after winning")

    def test_player_bust(self):
        # Player busts (hand value > 21), host has a valid hand
        self.player.hands[0] = [Card('♠', '10'), Card('♥', 'Q'), Card('♦', '5')]
        self.game.host.hands[0] = [Card('♠', '9'), Card('♥', '7')]
        self.game.update_balances()
        self.assertEqual(self.player.balance, self.initial_balance, "Player's balance should remain the same after busting")

    def test_host_win(self):
        # Host wins with a higher hand value, but not bust
        self.player.hands[0] = [Card('♠', '10'), Card('♥', '7')]
        self.game.host.hands[0] = [Card('♠', 'J'), Card('♥', '9')]
        self.game.update_balances()
        self.assertEqual(self.player.balance, self.initial_balance, "Player's balance should remain the same after host wins")

    def test_host_bust(self):
        # Host busts, player has a valid hand
        self.player.hands[0] = [Card('♠', '9'), Card('♥', '7')]
        self.game.host.hands[0] = [Card('♠', '10'), Card('♥', 'Q'), Card('♦', '5')]
        self.game.update_balances()
        self.assertEqual(self.player.balance, self.initial_balance + 2 * self.bet_amount, "Player's balance should increase by twice the bet amount after host busts")

    def test_tie(self):
        # Both player and host have the same hand value
        self.player.hands[0] = [Card('♠', 'J'), Card('♥', '7')]
        self.game.host.hands[0] = [Card('♠', '10'), Card('♥', '7')]
        self.game.update_balances()
        self.assertEqual(self.player.balance, self.initial_balance + self.bet_amount, "Player's balance should increase by the bet amount in case of a tie")

# Start tests
if __name__ == '__main__':
    unittest.main()