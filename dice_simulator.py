import random

def dice_simulator(sides, num_rolls):
    """
    Simulates rolling a dice with the specified number of sides a specified number of times.
    Returns a list of the roll results.
    """
    rolls = []
    for i in range(num_rolls):
        roll = random.randint(1, sides)
        rolls.append(roll)
    return rolls

# Example usage
sides = 6
num_rolls = 1
rolls = dice_simulator(sides, num_rolls)
print("You rolled:", rolls)
