import random

# Function to get the computer's choice
def get_computer_choice():
    choices = ['rock', 'paper', 'scissors']
    return random.choice(choices)

# Function to get the player's choice
def get_player_choice():
    choice = input("Choose rock, paper, or scissors: ").lower()
    while choice not in ['rock', 'paper', 'scissors']:
        choice = input("Invalid choice. Choose rock, paper, or scissors: ").lower()
    return choice

# Function to play a single round
def play_round():
    computer_choice = get_computer_choice()
    player_choice = get_player_choice()
    print(f"Computer chooses {computer_choice}")
    if computer_choice == player_choice:
        print("It's a tie!")
    elif (computer_choice == 'rock' and player_choice == 'scissors') or \
         (computer_choice == 'paper' and player_choice == 'rock') or \
         (computer_choice == 'scissors' and player_choice == 'paper'):
        print("Computer wins!")
    else:
        print("Player wins!")

# Main game loop
while True:
    play_round()
    play_again = input("Play again? (y/n) ").lower()
    while play_again not in ['y', 'n']:
        play_again = input("Invalid input. Play again? (y/n) ").lower()
    if play_again == 'n':
        break
