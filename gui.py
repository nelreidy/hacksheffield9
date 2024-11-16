import tkinter as tk
from tkinter import ttk
from character import Character
from food import Food

class GUI:
    def __init__(self, root, character):
        self.root = root
        self.character = character
        self.character_canvas = None
        self.stat_labels = {}
        self.food_buttons = []

        self.setup_ui()
        self.update_stats()

    # Function to make the character's head turn green (Radioactive)
    def turn_head_green(self):
        # Clear the head and redraw it with green fill
        self.character_canvas.delete("head")
        self.character_canvas.create_oval(100, 50, 200, 150, fill="green", tags="head")

    # Function to make the character's head turn normal (Alive/neutral)
    def cure(self):
        # Clear the head and redraw it with peachpuff fill
        self.character_canvas.delete("head")
        self.character_canvas.create_oval(100, 50, 200, 150, fill="peachpuff", tags="head")
        
    # Function to make the character's head turn black (Dead)
    def kill(self):
        # Clear the head and redraw it with black fill
        self.character_canvas.delete("head")
        self.character_canvas.create_oval(100, 50, 200, 150, fill="black", tags="head")

    def setup_ui(self):
        self.root.title("Simulation UI")
        self.root.geometry("800x600")

        # Character Canvas
        self.character_frame = tk.Frame(self.root, width=300, height=400, bg="white")
        self.character_frame.grid(row=0, column=0, rowspan=2, padx=10, pady=10)

        self.character_canvas = tk.Canvas(self.character_frame, width=300, height=400, bg="white")
        self.character_canvas.pack()

        # Draw the character (basic placeholder)
        self.character_canvas.create_oval(100, 50, 200, 150, fill="peachpuff", tags="head")  # Head
        self.character_canvas.create_rectangle(120, 150, 180, 300, fill="lightblue")  # Body

        # Stats Section
        self.stats_frame = tk.Frame(self.root, width=200, height=400)
        self.stats_frame.grid(row=0, column=1, padx=10, pady=10, sticky="n")

        tk.Label(self.stats_frame, text="Stats", font=("Arial", 14)).pack()

        stats = {
            "Weight": "XX kg",
            "Height": "XXX cm",
            "Health": "XX",
            "Fitness": "XX",
            "Happiness": "XX",
            "Hunger": "XX",
            "Hair Length": "XX cm"
        }

        for stat, value in stats.items():
            frame = tk.Frame(self.stats_frame)
            frame.pack(anchor="w")
            tk.Label(frame, text=f"{stat}: ", font=("Arial", 12)).pack(side="left")
            self.stat_labels[stat] = tk.Label(frame, text=value, font=("Arial", 12))
            self.stat_labels[stat].pack(side="left")

        # Time Speed Slider
        self.time_frame = tk.Frame(self.stats_frame)
        self.time_frame.pack(anchor="w", pady=10)
        tk.Label(self.time_frame, text="Time Speed:", font=("Arial", 12)).pack(side="left")
        time_slider = ttk.Scale(self.time_frame, from_=0.5, to=4, orient="horizontal", length=150)
        time_slider.set(1)  # Default speed
        time_slider.pack(side="left")

        # Scenarios Section
        self.scenarios_frame = tk.Frame(self.root, width=300, height=200, bg="lightgray")
        self.scenarios_frame.grid(row=1, column=1, padx=10, pady=10, sticky="n")
        tk.Label(self.scenarios_frame, text="Scenarios", font=("Arial", 14)).pack(anchor="w")

        # Interaction Section
        self.interaction_frame = tk.Frame(self.root, width=600, height=200, bg="white")
        self.interaction_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        tk.Label(self.interaction_frame, text="Food Interaction", font=("Arial", 14)).grid(row=0, column=0, columnspan=5)

        # Create list of foods
        food_types = [Food("Apple", "healthy"),
                        Food("Burger", "unhealthy"),
                        Food("Cookie", "neutral"),
                        Food("Magic Cookie", "radioactive"),
                        Food("Cyanide", "deadly"),
                        Food("Mysterious Red Mushrooms", "healthy"),
                        Food("Mysterious Blue Mushrooms", "radioactive"),
                        Food("Mysterious Pink Mushrooms", "deadly"),
                        ]

        # Create food buttons
        for i, food in enumerate(food_types):
            row = 1 if i < 5 else 2  # First 5 buttons in row 1, next 5 in row 2
            col = i % 5  # Column resets after 5 buttons
            button = tk.Button(self.interaction_frame, text=food_types[i].name, width=10, command=lambda f=food: self.feed_character(f))
            button.grid(row=row, column=col, padx=5, pady=5)
            self.food_buttons.append(button)

    def feed_character(self, food: Food):
        # Feed character and update stats
        self.character.eat(food)
    
    def update_stats(self):
        # Update stats on the GUI
        self.stat_labels["Weight"].config(text=f"{self.character.attributes['weight']} kg")
        self.stat_labels["Height"].config(text=f"{self.character.attributes['height']} cm")
        self.stat_labels["Health"].config(text=f"{self.character.attributes['health']}")
        self.stat_labels["Fitness"].config(text=f"{self.character.attributes['fitness']}")
        self.stat_labels["Happiness"].config(text=f"{self.character.attributes['happiness']}")
        self.stat_labels["Hunger"].config(text=f"{self.character.attributes['hunger']}")
        self.stat_labels["Hair Length"].config(text=f"{self.character.attributes['hair_length']} cm")
