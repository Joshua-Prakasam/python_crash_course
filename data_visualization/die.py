from random import randint

class Die:
    """A Class representing a single Die"""

    def __init__(self, num_sides=6):
        """Assumes a six-sided dice"""
        self.num_sides = num_sides

    def roll(self):
        """Return a random value between 1 and num of sides"""

        return randint(1, self.num_sides)
