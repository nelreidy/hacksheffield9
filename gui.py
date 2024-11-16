import tkinter as tk
from tkinter import ttk
from food import Food

# Create the main application window
root = tk.Tk()
root.title("Simulation UI")
root.geometry("800x600")

# Function to make the character's head turn green (Radioactive)
def turn_head_green():
    # Clear the head and redraw it with green fill
    character_canvas.delete("head")
    character_canvas.create_oval(100, 50, 200, 150, fill="green", tags="head")

# Function to make the character's head turn normal (Alive/neutral)
def cure():
    # Clear the head and redraw it with peachpuff fill
    character_canvas.delete("head")
    character_canvas.create_oval(100, 50, 200, 150, fill="peachpuff", tags="head")
    
# Function to make the character's head turn black (Dead)
def kill():
    # Clear the head and redraw it with black fill
    character_canvas.delete("head")
    character_canvas.create_oval(100, 50, 200, 150, fill="black", tags="head")

# Character Canvas
character_frame = tk.Frame(root, width=300, height=400, bg="white")
character_frame.grid(row=0, column=0, rowspan=2, padx=10, pady=10)

character_canvas = tk.Canvas(character_frame, width=300, height=400, bg="white")
character_canvas.pack()

# Draw the character (basic placeholder)
character_canvas.create_oval(100, 50, 200, 150, fill="peachpuff", tags="head")  # Head
character_canvas.create_rectangle(120, 150, 180, 300, fill="lightblue")  # Body

# Stats Section
stats_frame = tk.Frame(root, width=200, height=400)
stats_frame.grid(row=0, column=1, padx=10, pady=10, sticky="n")

tk.Label(stats_frame, text="Stats", font=("Arial", 14)).pack()

stats = {
    "Weight": "XX kg",
    "Height": "XXX cm",
    "Health": "XX",
    "Fitness": "XX",
    "Happiness": "XX",
    "Hunger": "XX"
}

stat_labels = {}
for stat, value in stats.items():
    frame = tk.Frame(stats_frame)
    frame.pack(anchor="w")
    tk.Label(frame, text=f"{stat}: ", font=("Arial", 12)).pack(side="left")
    stat_labels[stat] = tk.Label(frame, text=value, font=("Arial", 12))
    stat_labels[stat].pack(side="left")

# Time Speed Slider
time_frame = tk.Frame(stats_frame)
time_frame.pack(anchor="w", pady=10)
tk.Label(time_frame, text="Time Speed:", font=("Arial", 12)).pack(side="left")
time_slider = ttk.Scale(time_frame, from_=0.5, to=4, orient="horizontal", length=150)
time_slider.set(1)  # Default speed
time_slider.pack(side="left")

# Scenarios Section
scenarios_frame = tk.Frame(root, width=300, height=200, bg="lightgray")
scenarios_frame.grid(row=1, column=1, padx=10, pady=10, sticky="n")
tk.Label(scenarios_frame, text="Scenarios", font=("Arial", 14)).pack(anchor="w")

# Interaction Section
interaction_frame = tk.Frame(root, width=600, height=200, bg="white")
interaction_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

tk.Label(interaction_frame, text="Food Interaction", font=("Arial", 14)).grid(row=0, column=0, columnspan=5)

# Create list of foods
food_types = [Food("Apple", "healthy"),
                  Food("Burger", "unhealthy"),
                  Food("Cookie", "neutral"),
                  Food("Magic Cookie", "radioactive"),
                  Food("Cyanide", "deadly"),
                  Food("Mysterious Red Mushrooms", "healthy"),
                  Food("Mysterious Blue Mushrooms", "radioactive"),
                  Food("Mysterious Pink Mushrooms", "deadly"),
                  Food("food 9", "deadly"),
                  Food("food 10", "deadly"),
                  ]

# Create list of commands to enact effects
command_list = []

# Create food buttons
food_buttons = []
for i in range(10):
    row = 1 if i < 5 else 2  # First 5 buttons in row 1, next 5 in row 2
    col = i % 5  # Column resets after 5 buttons
    button = tk.Button(interaction_frame, text=food_types[i].name, width=10, command=turn_head_green)
    button.grid(row=row, column=col, padx=5, pady=5)
    food_buttons.append(button)

# Start the application
root.mainloop()
