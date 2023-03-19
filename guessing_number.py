import random

# Generate a random number between 1 and 100
secret_number = random.randint(1, 100)

# Initialize the number of guesses
num_guesses = 0

# Start the game
print("I'm thinking of a number between 1 and 100. Can you guess what it is?")

# Loop until the player guesses the number
while True:
    # Ask the player to guess the number
    guess = int(input("Enter your guess: "))
    
    # Increase the number of guesses
    num_guesses += 1
    
    # Provide feedback on whether the guess is too high or too low
    if guess < secret_number:
        print("Too low! Try again.")
    elif guess > secret_number:
        print("Too high! Try again.")
    else:
        # The player has guessed the number
        print(f"Congratulations, you guessed the number in {num_guesses} guesses!")
        break
