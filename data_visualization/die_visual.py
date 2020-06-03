import pygal

from die import Die

# Create two D6 dice.
die_1 = Die()
die_2 = Die()

times = 5000
results = [die_1.roll() * die_2.roll() for roll_num in range(times)]

min_result = 1
max_result = die_1.num_sides * die_2.num_sides
# Analyze the results.
frequencies = [results.count(value) for value in range(min_result, max_result + 1)]

# Visualize the results.
hist = pygal.Bar()

hist.title = f"Results of rolling a D{die_1.num_sides} and a D{die_2.num_sides} {times:,} times."
hist.x_labels = [str(value) for value in range(min_result, max_result + 1)]
hist.x_title = "Result"
hist.y_title = "Frequency of Result"

hist.add(f"D{die_1.num_sides} + D{die_2.num_sides}", frequencies)
hist.render_to_file('die_visual.svg')
