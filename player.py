class Player:
    def __init__(self, name, initial_balance):
        # Initialize player attributes
        self.name = name
        self.hands = [[]]  # Initialize player hands as a list of lists
        self.balance = initial_balance
        self.bets = [0]  # Initialize player bets as a list

    def print_hand(self):
        # Prints each hand of the player along with its total value
        for index, hand in enumerate(self.hands):
            hand_representation = ' '.join(f"{card.rank}{card.suit}" for card in hand)
            hand_value = self.calculate_hand_value(hand_index=index)
            print(f"Hand {index + 1}: {hand_representation} (Hand Value: {hand_value})")

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

    def split(self, hand_index=0):
        # Perform a split if the hand can be split
        if self.can_split(hand_index):
            new_hand = self.hands[hand_index].pop(0)
            new_bet = self.bets[hand_index]
            self.hands.append(new_hand)
            self.bets.append(new_bet)

    def can_split(self, hand_index=0):
        # Check if the hand has exactly two cards of the same rank
        return (len(self.hands[hand_index]) == 2 and 
                self.hands[hand_index][0].rank == self.hands[hand_index][1].rank)

    def double_down(self, hand_index=0):
        # Double the bet on the player's hand if the balance allows
        if self.can_double_down(hand_index):
            self.balance -= self.bets[hand_index]
            self.bets[hand_index] *= 2
            
    def can_double_down(self, hand_index=0):
        # Check if balance is enought to double down
        return self.balance >= self.bets[hand_index]
            
    def calculate_hand_value(self, hand_index=0):
        hand_value = 0
        aces_count = 0

        for card in self.hands[hand_index]:
            rank = card.rank
            if rank in ["J", "Q", "K"]:
                hand_value += 10
            elif rank == "A":
                aces_count += 1
                hand_value += 11
            else:
                hand_value += int(rank)
        
        # Adjust for Aces if the hand value is over 21
        while hand_value > 21 and aces_count > 0:
            hand_value -= 10
            aces_count -= 1
        
        return hand_value