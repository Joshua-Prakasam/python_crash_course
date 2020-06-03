import matplotlib.pyplot as plt

x_values = list(range(1, 5001))
y_values = [x**3 for x in x_values]

plt.scatter(x_values, y_values, c=y_values, cmap=plt.cm.Greens, edgecolor='none')

# Setting Title
plt.title("Cube Numbers", fontsize=24)

# Setting Labels
plt.xlabel("Value", fontsize=14)
plt.ylabel("Cube of Value", fontsize=14)

plt.tick_params(axis='both', labelsize=14)

# Set the range for each axis.
print(y_values[-2500])
plt.axis([0, x_values[-1] + 500, 0, y_values[-1] + y_values[2500]])

plt.show()
