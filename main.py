import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# JSON file path
json_path = "experience.json"

# Open and read the json file
with open(json_path, 'r') as file:
    experience_data = json.load(file)


def fit_polynomial_to_category(category):
    category_items = list(category.keys())
    years = [float(category[item]) for item in category_items]
    x_values = list(range(len(category_items)))
    degree = min(2, len(x_values) - 1)
    coefficients = np.polyfit(x_values, years, degree)
    return np.poly1d(coefficients)


def animate_category(category, polynomial, frames=100):
    items = list(category.keys())
    years = [float(category[item]) for item in items]
    x_data = np.array(range(len(items)))
    y_data = np.array(years)

    fig, ax = plt.subplots()
    ax.scatter(x_data, y_data, color='red', label='Data Points')
    line, = ax.plot([], [], color='blue', label='Fitted Polynomial')
    ax.set_xlim(min(x_data)-1, max(x_data)+1)
    ax.set_ylim(min(y_data)-1, max(y_data)+1)
    ax.set_xticks(x_data)
    ax.set_xticklabels(items, rotation=45)
    ax.set_title("Polynomial Fit for Category")
    ax.set_xlabel("Items")
    ax.set_ylabel("Years")
    ax.legend()
    ax.grid(True)

    def init():
        line.set_data([], [])
        return line,

    def update(frame):
        # Convert frame to integer
        frame = int(frame)
        x_values = np.linspace(0, len(items) - 1, frame)
        y_values = polynomial(x_values)
        line.set_data(x_values, y_values)
        return line,

    ani = FuncAnimation(fig, update, frames=np.linspace(1, frames, frames), init_func=init, blit=True)

    # To display the animation in a Jupyter notebook, use:
    # from IPython.display import HTML
    # HTML(ani.to_jshtml())

    # To save the animation as a video or GIF, use:
    # ani.save('polynomial_animation_{}.mp4'.format(category), writer='ffmpeg')
    # or
    # ani.save('polynomial_animation_{}.gif'.format(category), writer='imagemagick')

    plt.show()


# Applying the animation to each category
for cat, items in experience_data.items():
    poly = fit_polynomial_to_category(items)
    animate_category(items, poly)
