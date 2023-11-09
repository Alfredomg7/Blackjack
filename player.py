class Player:
    def __init__(self, name, initial_balance):
        # Initialize player attributes
        self.name = name
        self.hands = [[]]  # Initialize player hands as a list of lists
        self.balance = initial_balance
        self.bets = [0]  # Initialize player bets as a list

    def print_hand(self):
        # Print each card in the player's hand(s)
        for hand in self.hands:
            for card in hand:
                print(f"{card[1]}{card[0]}", end=" ")
            print("\n")

    def place_bet(self, amount, hand_index=0):
        # Place a bet on a specific hand if the player has enough balance
        if self.balance >= amount:
            self.bets[hand_index] = amount
            self.balance -= amount
            return True
        else:
            return False

    def hit(self, card, hand_index=0):
        # Add a card to the player's hand
        self.hands[hand_index].append(card)

    def receive_hand(self, card_1, card_2):
        # Receive the initial hand of cards
        self.hands[0].append(card_1)
        self.hands[0].append(card_2)
    
    def reset_hand(self):
        self.hands = [[]]

    def reset_bet(self):
        self.bet = [0]

    def split(self):
        # Split a hand into two hands, adding a new hand and duplicating the bet
        new_hand = self.hands[0].pop()
        new_bet = self.bets[0]
        self.hands.append(new_hand)
        self.bets.append(new_bet)

    def double_down(self):
        # Double the bet on the player's hand
        self.bets[0] *= 2
    
    def calculate_hand_value(self, hand_index=0):
        hand_value = 0
        has_ace = False
        for card in self.hands[hand_index]:
            rank = card[1]
            if rank in ["J", "Q", "K"]:
                hand_value += 10
            elif rank == "A":
                has_ace = True
                hand_value += 11
            else:
                hand_value += int(rank)
        
        if hand_value > 21 and has_ace:
            hand_value -= 10
        
        return hand_value

