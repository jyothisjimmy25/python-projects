import random

# List of words for the game
words = ["python", "program", "computer", "data", "science", "algorithm"]

# Choose a random word from the list
word = random.choice(words)

# Create a list of underscores for the word
hidden_word = ["_"] * len(word)

# List of guessed letters
guessed_letters = []

# Number of guesses allowed
num_guesses = 6

# Game loop
while num_guesses > 0:
    # Display the hidden word
    print(" ".join(hidden_word))
    
    # Ask the player to guess a letter
    guess = input("Guess a letter: ").lower()
    
    # Check if the letter has already been guessed
    if guess in guessed_letters:
        print("You already guessed that letter!")
    else:
        # Add the letter to the list of guessed letters
        guessed_letters.append(guess)
        
        # Check if the letter is in the word
        if guess in word:
            print("Correct!")
            
            # Replace the underscores with the guessed letter
            for i in range(len(word)):
                if word[i] == guess:
                    hidden_word[i] = guess
                    
            # Check if the word has been completely guessed
            if "_" not in hidden_word:
                print("Congratulations, you guessed the word!")
                break
        else:
            print("Incorrect!")
            num_guesses -= 1
            
            # Check if the player has used up all their guesses
            if num_guesses == 0:
                print("Game over! The word was:", word)
            else:
                print(f"You have {num_guesses} guesses left.")
