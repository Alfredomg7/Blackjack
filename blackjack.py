from deck import Deck
from player import Player
from host import Host

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
            if not self.players:
                print("No players with funds left to play. Game over.")
                break
            
            self.reset_for_new_round()
            self.handle_bets_and_dealing()
            self.play_round()

            # Check if there are active players after handling bets
            if not self.active_players:
                print("No active players for this round.\n")
                continue
        
            # Update player balances based on game outcomes
            self.update_balances()
            
            # Print results after balances have been updated
            self.print_results()

    def any_player_with_funds(self):
        return any(player.balance > 0 for player in self.players)

    def print_welcome_message(self):
        print("Welcome to Blackjack!\n")

    def print_insufficient_funds_message(self):
        print("All players have insufficient funds to continue. Game over.")
    
    def handle_bets_and_dealing(self):
        print("-" * 40)

        self.active_players = []  # Reset the list of active players for the new round

        for player in self.players[:]:  # Iterate over a copy of self.players
            if player.balance > 0:
                bet = self.ask_for_bet(player)
                if bet > 0:
                    player.place_bet(bet)
                    card_1, card_2 = self.deck.deal()
                    player.receive_hand(card_1, card_2)
                    self.active_players.append(player)
                else:
                    print(f"{player.name} is skipping this round.\n")
            else:
                print(f"{player.name} cannot play due to insufficient funds.\n")

        if not self.active_players:
            print("No active players for this round.\n")
            return  # Early exit if no players are active for this round

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
            while not self.is_game_over(player):
                action = self.get_player_action(player)
                if action == "h":
                    new_card = self.hit_card()
                    player.hit(new_card)
                    player.print_hand()
                elif action == "s":
                    break

        self.host_turn()

    def get_player_action(self, player):
        while True:
            action = input(f"{player.name}, do you want to hit (h) or stand (s)? ").lower()
            if action in ["h", "s"]:
                return action
            print("Invalid option. Please enter 'h' for hit or 's' for stand.")
    
    def host_turn(self):
        while self.host.must_hit():
            new_card = self.deck.hit()
            self.host.hit(new_card)
            self.host.print_hand()

    def ask_for_bet(self, player):
        if player.balance == 0:
            print(f"{player.name} has exited the game due to insufficient funds.\n")
            self.players.remove(player)
            return None
    
        while True:
            try:
                bet = int(input(f"{player.name}, how much do you want to bet? (0 to exit): "))
                if 0 <= bet <= player.balance:
                    return bet
                else:
                    print(f"Invalid bet. Please enter a number between 0 and {player.balance}.")
            except ValueError:
                print("Invalid input. Please enter a number.")

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
    
    def is_game_over(self, player):
        return player.calculate_hand_value() > 21

    def print_results(self):
        for player in self.players:
            print(f"{player.name}'s hand: ", end="")
            player.print_hand()

        print(f"{self.host.name}'s hand: ", end="")
        self.host.print_hand()
        print("\n")

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
            
            print(f"{player.name}'s balance: ${player.balance}\n")



        