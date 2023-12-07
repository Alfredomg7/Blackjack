from deck import Deck
from player import Player
from host import Host

# Constants
WELCOME_MESSAGE = "Welcome to Blackjack!\n"
GAME_OVER_NO_FUNDS_MESSAGE = "All players have insufficient funds to continue. Game over."
NO_ACTIVE_PLAYERS_MESSAGE = "No active players for this round.\n"
SKIP_ROUND_MESSAGE = "{} is skipping this round.\n"
INSUFFICIENT_FUNDS_MESSAGE = "{} cannot play due to insufficient funds.\n"
NEW_DECK_MESSAGE = "New deck is being used"
INVALID_OPTION_MESSAGE = "Invalid option. Please enter 'h' for hit or 's' for stand."
INVALID_BET_MESSAGE = "Invalid bet. Please enter a number between 0 and {}."
INVALID_INPUT_MESSAGE = "Invalid input. Please enter a number."
EXIT_DUE_TO_FUNDS_MESSAGE = "{} has exited the game due to insufficient funds.\n"
PLAYER_BUSTS_MESSAGE = "{} busts! {} wins."
PLAYER_WINS_MESSAGE = "{} wins!"
TIE_MESSAGE = "{} and {} tie!"
PLAYER_BALANCE_MESSAGE = "{}'s balance: ${}\n"
HOST_HAND_MESSAGE = "{}'s hand: {} ?\n"
HIT_ACTION = "h"
STAND_ACTION = "s"
DOUBLE_DOWN_NO_FUNDS_MESSAGE = "Insufficient funds to double down."

class Blackjack:
    def __init__(self, player_names, initial_balance):
        self.players = [Player(name, initial_balance) for name in player_names]
        self.host = Host()
        self.deck = Deck()
        self.active_players = []

    def start_game(self):
        self.print_welcome_message()
        
        while self.any_player_with_funds():
            # Remove players with zero balance before starting a new round
            self.players = [player for player in self.players if player.balance > 0]
            self.reset_for_new_round()
            print("-" * 40)
            
            if self.handle_bets():
                self.deal_initial_cards()
                self.play_round()
                self.update_balances()
                self.print_results()
        
        print(GAME_OVER_NO_FUNDS_MESSAGE)

    def any_player_with_funds(self):
        return any(player.balance > 0 for player in self.players)

    def print_welcome_message(self):
        print(WELCOME_MESSAGE)

    def print_insufficient_funds_message(self):
        print(GAME_OVER_NO_FUNDS_MESSAGE)
    
    def handle_bets(self):
        self.active_players = []  # Reset the list of active players for the new round
        for player in self.players[:]:  # Iterate over a copy of self.players
            if player.balance > 0:
                bet = self.ask_for_bet(player)
                if bet > 0:
                    player.place_bet(bet)
                    self.active_players.append(player)
                else:
                    print(SKIP_ROUND_MESSAGE.format(player.name))
            else:
                print(INSUFFICIENT_FUNDS_MESSAGE.format(player.name))

        if not self.active_players:
            print(NO_ACTIVE_PLAYERS_MESSAGE)
            return  False 
        
        return True
    
    def deal_initial_cards(self):
        for player in self.active_players:
            card_1, card_2 = self.deck.deal()
            player.receive_hand(card_1, card_2)

        # Deal to the host last
        host_card_1, host_card_2 = self.deck.deal()
        self.host.receive_hand(host_card_1, host_card_2)

        # At this point, all active players and the host have been dealt hands for the round
        self.print_initial_hands()
    
    def reset_for_new_round(self):
        for player in self.players:
            player.reset_hand()  
            player.reset_bet()   

        self.host.reset_hand()  
        self.deck.shuffle()

    def play_round(self):
        # Players' turns
        for player in self.active_players:
            # Check and offer double down
            if player.can_double_down():
                if self.offer_double_down(player):
                    continue

            while not self.is_turn_over(player):
                action = self.get_player_action(player)
                if action == HIT_ACTION:
                    new_card = self.hit_card()
                    player.hit(new_card)
                    player.print_hand()
                elif action == STAND_ACTION:
                    break

        self.host_turn()

    def offer_double_down(self, player):
        while True:
            try:
                response = input(f"{player.name}, Do you want to Double Down? (yes/no): ").strip().lower()
                if response not in ["yes", "no"]:
                    raise ValueError("Please answer with 'yes' or 'no'.")

                if response == "yes":
                    if player.can_double_down():
                        player.double_down()
                        print(f"{player.name} has doubled down.")
                        new_card = self.hit_card()
                        print("\n")
                        player.hit(new_card)
                        return True
                    else:
                        print(DOUBLE_DOWN_NO_FUNDS_MESSAGE)
                        return False

                if response == "no":
                    return False

            except ValueError as e:
                print(e)

    def get_player_action(self, player):
        while True:
            action = input(f"{player.name}, do you want to hit ({HIT_ACTION}) or stand ({STAND_ACTION})? ").lower()
            if action in [HIT_ACTION, STAND_ACTION]:
                return action
            print(INVALID_OPTION_MESSAGE)
    
    def host_turn(self):
        while self.host.must_hit():
            new_card = self.deck.hit()
            self.host.hit(new_card)

    def ask_for_bet(self, player):
        if player.balance == 0:
            print(EXIT_DUE_TO_FUNDS_MESSAGE.format(player.name))
            self.players.remove(player)
            return None
    
        while True:
            try:
                bet = int(input(f"{player.name}, how much do you want to bet? (0 to exit): "))
                if 0 <= bet <= player.balance:
                    return bet
                else:
                    print(INVALID_BET_MESSAGE.format(player.balance))
            except ValueError:
                print(INVALID_INPUT_MESSAGE)

    def hit_card(self):
        if self.deck.is_empty():
            print(NEW_DECK_MESSAGE)
            self.deck.reinitialize_deck()
        
        return self.deck.hit()

    def print_initial_hands(self):
        for player in self.players:
            print(f"{player.name}'s hand: ", end="")
            player.print_hand()
        
        print(f"{self.host.name}'s hand: {self.host.hands[0][0][1]}{self.host.hands[0][0][0]} ?")
        print("\n")

    def update_balances(self):
        host_value = self.host.calculate_hand_value()

        for player in self.active_players:
            player_value = player.calculate_hand_value()

            # Player busts
            if player_value > 21:
                pass

            # Host busts
            elif host_value > 21:
                player.balance += player.bets[0] * 2
            
            # Both player and host are under or equal 21
            else:
                # Player wins
                if player_value > host_value:
                    player.balance += player.bets[0] * 2
                # Host wins
                elif player_value < host_value:
                    pass
                # Tie
                elif player_value == host_value:
                    player.balance += player.bets[0] 
            

            # Reset the player's bet for the next round
            player.reset_bet()
    
    def is_turn_over(self, player):
        hand_value = player.calculate_hand_value()
        return hand_value >= 21

    def print_results(self):
        for player in self.players:
            print(f"{player.name}'s hand: ", end="")
            player.print_hand()

        print(HOST_HAND_MESSAGE.format(self.host.name, self.host.hands[0][0][1] + self.host.hands[0][0][0]), end="")
        self.host.print_hand()
        print("\n")

        host_value = self.host.calculate_hand_value()

        for player in self.players:
            player_value = player.calculate_hand_value()
            if player_value > 21:
                print(PLAYER_BUSTS_MESSAGE.format(player.name, self.host.name))
            elif host_value > 21:
                print(PLAYER_WINS_MESSAGE.format(player.name))
            elif player_value > host_value:
                print(PLAYER_WINS_MESSAGE.format(player.name))
            elif player_value < host_value:
                print(PLAYER_BUSTS_MESSAGE.format(player.name, self.host.name))
            else:
                print(TIE_MESSAGE.format(player.name, self.host.name))
            
            print(PLAYER_BALANCE_MESSAGE.format(player.name, player.balance))



        