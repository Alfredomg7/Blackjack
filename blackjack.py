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
        self.deck.shuffle()

        # Deal initial cards
        for player in self.players:
            player.receive_hand(self.deck.deal()[0],self.deck.deal()[1])

        self.host.receive_hand(self.deck.deal()[0],self.deck.deal()[1])

        self.print_initial_hands()

        # Players' turns
        for player in self.players:
            while not self.is_game_over(player):
                action = input(f"{player.name}, do you want to hit or stand? ").lower()
                if action == "hit":
                    new_card = self.deck.hit()
                    player.hit(new_card)
                    self.print_player_hand(player)
                elif action == "stand":
                    break

        # Host's turn
        while self.host.must_hit():
            new_card = self.deck.hit()
            self.host.hit(new_card)
        
        self.print_results()

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



        