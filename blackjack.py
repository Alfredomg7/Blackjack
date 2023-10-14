from deck import Deck
from player import Player
from host import Host

class Blackjack:
    def __init__(self, player_names, initial_balance):
        self.players = [Player(name, initial_balance) for name in player_names]
        self.host = Host()
        self.deck = Deck()

    def start_game(self):
        print("Welcome to Blackjack!")
        
        while self.players:
            self.reset_for_new_round()
            self.deck.shuffle()

            # Ask for best and deal initial cards
            remaining_players = []
            for player in self.players:
                bet = self.ask_for_bet(player)
                if bet > 0:
                    player.place_bet(bet)
                    card_1, card_2 = self.deck.deal()
                    player.receive_hand(card_1,card_2)
                    remaining_players.append(player)
                else:
                    print(f"{player.name} has exited the game.")
            
            self.players = remaining_players

            if not self.players:
                print("All players have exited the game.")
                break

            card_1, card_2 = self.deck.deal()
            self.host.receive_hand(card_1, card_2)
            self.print_initial_hands()

            # Players' turns
            for player in self.players:
                while not self.is_game_over(player):
                    action = input(f"{player.name}, do you want to hit or stand? ").lower()
                    if action == "hit":
                        new_card = self.hit_card()
                        player.hit(new_card)
                        self.print_player_hand(player)
                    elif action == "stand":
                        break

            # Host's turn
            while self.host.must_hit():
                new_card = self.hit_card()
                self.host.hit(new_card)
        
            # Update player balances based on game outcomes
            self.update_balances()
            
            # Print results after balances have been updated
            self.print_results()

    def ask_for_bet(self, player):
        while True:
            bet = input(f"{player.name}, how much do you want to bet? (0 to exit): ")
            if bet.isdigit() and 0 <= int(bet) <= player.balance:
                return int(bet)
            else:
                print(f"Invalid bet. Please enter a number between 0 and {player.balance}.")

    def hit_card(self):
        if self.deck.is_empty():
            print("New deck is being used")
            self.deck = Deck()
            self.deck.shuffle()
        
        return self.deck.hit()

    def print_initial_hands(self):
        for player in self.players:
            print(f"{player.name}'s hand: ", end="")
            player.print_hand()
        
        print(f"{self.host.name}'s hand: {self.host.hands[0][0][1]}{self.host.hands[0][0][0]} ?")
        print("\n")

    def print_player_hand(self, player):
        print(f"{player.name}'s hand: ", end="")
        player.print_hand()
        print("\n")

    def update_balances(self):
        host_value = self.host.calculate_hand_value()

        for player in self.players:
            player_value = player.calculate_hand_value()

            if host_value > 21 or player_value > host_value:
                player.balance += 2 * player.bets[0]  # Player earns twice its bet
            elif player_value == host_value:
                player.balance += player.bets[0] # Player recover its bet

    def reset_for_new_round(self):
        for player in self.players:
            player.hands = [[]]
            player.bets = [0]
        self.host.hands = [[]]
    
    def is_game_over(self, player):
        return player.calculate_hand_value() >= 21 or self.host.calculate_hand_value() >= 21

    def print_results(self):
        for player in self.players:
            print(f"{player.name}'s hand: ", end="")
            player.print_hand()

        print(f"{self.host.name}'s hand: ", end="")
        self.host.print_hand()

        host_value = self.host.calculate_hand_value()

        for player in self.players:
            player_value = player.calculate_hand_value()
            if player_value > 21:
                print(f"{player.name} busts! {self.host.name} wins.")
            elif host_value > 21:
                print(f"{self.host.name} busts! {player.name} wins.")
            elif player_value > host_value:
                print(f"{player.name} wins!")
            elif player_value < host_value:
                print(f"{self.host.name} wins!")
            else:
                print(f"{player.name} and {self.host.name} tie!")



        