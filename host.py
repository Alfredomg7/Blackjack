from player import Player

class Host(Player):
    def __init__(self):
        # Initialize the Host class, inheriting from the Player class
        super().__init__(name="Host", initial_balance=0)
    
    def must_hit(self):
        # Determine if the host must hit based on the hand value
        return self.calculate_hand_value() < 17
