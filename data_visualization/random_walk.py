from random import choice


class RandomWalk:
    """A Class to generate Random Walk."""

    def __init__(self, num_points=5000):
        """Initialize attributes of a walk"""

        self.num_points = num_points

        """All Walks start at (0, 0)"""
        self.x_values = [0]
        self.y_values = [0]

    @staticmethod
    def get_step():
        direction_list = [1, -1]
        distance_list = [0, 1, 2, 3, 4]
        direction = choice(direction_list)
        distance = choice(distance_list)
        return direction * distance

    def fill_walk(self):
        """Calculate all the points in the random walk."""

        # Keep taking steps until the walk reaches the desired length.
        while len(self.x_values) < self.num_points:

            # Decide which direction to go and how far to go in to that direction.

            x_step = self.get_step()
            y_step = self.get_step()

            if x_step + y_step == 0:
                continue

            # Calculate the next x and y values
            next_x = self.x_values[-1] + x_step
            next_y = self.y_values[-1] + y_step

            self.x_values.append(next_x)
            self.y_values.append(next_y)
