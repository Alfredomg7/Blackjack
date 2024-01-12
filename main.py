from blackjack import Blackjack  

def get_player_names(num_players):
    # Get names of players from user input
    player_names = []
    for i in range(num_players):
        name = input(f"Enter name for player {i+1}: ")
        player_names.append(name)
    return player_names

def get_initial_balance():
    # Get initial balance for players
    while True:
        try:
            initial_balance = int(input("Enter initial balance for players: "))
            print("\n")
            if initial_balance < 1:
                print("Initial balance must be a positive integer.")
            else:
                return initial_balance
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

def main():
    try:
        # Get the number of players from user input
        num_players = int(input("Enter the number of players: "))
    
    except:
        print("Invalid input. Please enter a valid integer.")  

    if num_players < 1 or num_players > 6:
            print("Number of players must be between 1 and 6.")
    else:
        # Get player names and initial balance
        player_names = get_player_names(num_players)
        initial_balance = get_initial_balance()
            
        # Create a Blackjack game instance and start the game
        blackjack = Blackjack(player_names,initial_balance)
        blackjack.start_game()
    

if __name__ == "__main__":
    main()