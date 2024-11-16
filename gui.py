import tkinter as tk
from tkinter import ttk
import random
from character import Character
from constants import REFRESH_RATE, MIN_TIME_SPEED, MAX_TIME_SPEED
from food import Food

class GUI:
    def __init__(self, root, character):
        self.root = root
        self.character = character
        self.character_canvas = None
        self.stat_labels = {}
        self.food_buttons = []

        self.head_left = 0 
        self.head_right = 0 
        self.head_top = 0 
        self.head_bottom = 0 
        self.head_width = 0
        self.head_height = 0
        self.head_color = "peachpuff"

        self.setup_ui()
        self.update_stats()

    # Function to make the character's head turn green (Radioactive)
    def turn_head_green(self):
        # Clear the head and redraw it with green fill
        self.character.head_colour = "green"

    # Function to make the character's head turn normal (Alive/neutral/cured)
    def cure(self):
        # Clear the head and redraw it with peachpuff fill
        self.character_canvas.delete("head")

        # Use the head width and height attributes to determine the size of the head
        head_width = self.head_right - self.head_left
        head_height = self.head_bottom - self.head_top

        # Calculate the center of the body and position the head accordingly
        body_left = 120  # Assuming body_left is the starting point of the body
        body_right = body_left + (self.character.attributes["weight"] * 4)
        body_top = 150
        body_bottom = body_top + (self.character.attributes["height"] * 2)

        # Calculate the center for the head
        head_center_x = (body_left + body_right) / 2
        head_top = body_top - head_height
        head_left = head_center_x - (head_width / 2)
        head_right = head_center_x + (head_width / 1) 
        head_bottom = head_top + head_height

        # Redraw the head centered at the correct position
        self.character_canvas.create_oval(head_left, head_top, head_right, head_bottom, fill="peachpuff", tags="head")

        # Reset head color and number to default (single head)
        print("cure")
        self.character.head_colour = "peachpuff"
        self.character.body_colour = "lightblue"

        self.character.head_number = 1

        # Update the head position attributes for future use
        self.head_left = head_left
        self.head_right = head_right
        self.head_top = head_top
        self.head_bottom = head_bottom

        
    # Function to make the character's head turn black (Dead)
    def kill(self):
        # Clear the head and redraw it with black fill
        self.character_canvas.delete("head")

        self.character_canvas.create_oval(100, 50, 200, 150, fill="black", tags="head")

    # Function to make the character grow a 2nd head
    def grow_second_head(self):
        # Clear existing heads
        self.character_canvas.delete("head")

        # Dimensions for the first head (left side)
        first_head_left = self.head_left
        first_head_right = self.head_right
        first_head_top = self.head_top
        first_head_bottom = self.head_bottom

        # Dimensions for the second head (placed to the right of the first head)
        head_width = first_head_right - first_head_left
        second_head_left = first_head_right + 10  # Add spacing of 10 pixels
        second_head_right = second_head_left + head_width
        second_head_top = first_head_top
        second_head_bottom = first_head_bottom

        # Draw the first head
        self.character_canvas.create_oval(
            self.head_left - self.head_width/2, self.head_top,  self.head_right-self.head_width/2, self.head_bottom,
            fill="green", tags="head"
        )

        self.head_left = self.head_left - self.head_width
        self.head_right = self.head_right - self.head_width

        self.character_canvas.create_oval(
            self.head_left+self.head_width/2, self.head_top,  self.head_right+self.head_width/2, self.head_bottom,
            fill="peachpuff", tags="head2"
        )

        # Update the character's head count
        self.character.head_number = 2

    # Function to make the character grow a 2nd green head
    def grow_second_green_head(self):
        # Clear the head and redraw 2 with green fill
        self.head_color = "green"
        self.grow_second_head()


    # Function to make skin glow
    def glowing_skin(self):
        self.character.body_colour = "gold"

    
    # Bigger arms = stronger
    def strong_arms(self):
        self.character_canvas.delete("arm")
        self.character_canvas.create_rectangle(30, 155, 120, 200, fill="peachpuff", tags="arm")
        self.character_canvas.create_rectangle(180, 155, 270, 200, fill="peachpuff", tags="arm")
        self.character.has_super_strength = True

    # After some time, arms go back to normal (small)
    def normal_arms(self):
        self.character_canvas.delete("arm") 
        self.character_canvas.create_rectangle(60, 155, 120, 180, fill="peachpuff", tags="arm")  # Left arm
        self.character_canvas.create_rectangle(180, 155, 240, 180, fill="peachpuff", tags="arm") # Right arm


    def setup_ui(self):
        self.root.title("Simulation UI")
        self.root.geometry("1000x510")

        # Character Canvas
        self.character_frame = tk.Frame(self.root, width=300, height=400, bg="white")
        self.character_frame.grid(row=0, column=0, rowspan=2, padx=10, pady=10)

        self.character_canvas = tk.Canvas(self.character_frame, width=300, height=400, bg="white")
        self.character_canvas.pack()

        # Draw the character (basic placeholder)
        self.character_canvas.create_oval(100, 80, 150, 150, fill="peachpuff", tags="head")  # Head
        self.character_canvas.create_rectangle(120, 150, 180, 300, fill="lightblue", tags="body")  # Body
        self.character_canvas.create_rectangle(60, 155, 120, 180, fill="peachpuff", tags="arm")  # Left arm
        self.character_canvas.create_rectangle(180, 155, 240, 180, fill="peachpuff", tags="arm") # Right arm


        # Stats Section
        self.stats_frame = tk.Frame(self.root, width=200, height=400)
        self.stats_frame.grid(row=0, column=1, padx=10, pady=10, sticky="n")

        tk.Label(self.stats_frame, text=f"{self.character.name}'s Stats", font=("Arial", 14)).pack()

        stats = {
            "Age": "XX years XX months",
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
        tk.Label(self.time_frame, text="Simulation Speed:", font=("Arial", 12)).pack(side="left")
        self.time_slider = ttk.Scale(self.time_frame, from_=MIN_TIME_SPEED, to=MAX_TIME_SPEED, orient="horizontal", length=150)
        self.time_slider.set(1)  # Default speed
        self.time_slider.pack(side="left")

        # Bind slider to update character's time_speed
        self.time_slider.bind("<Motion>", self.update_time_speed)

        # Scenarios Section
        self.scenarios_frame = tk.Frame(self.root, width=300, height=200, bg="lightgray")
        self.scenarios_frame.grid(row=0, column=2, padx=10, pady=10, sticky="n")
        tk.Label(self.scenarios_frame, text="Scenarios", font=("Arial", 14)).pack(anchor="w")

        # Interaction Section
        self.interaction_frame = tk.Frame(self.root, width=600, height=200, bg="white")
        self.interaction_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        tk.Label(self.interaction_frame, text="Food Interaction", font=("Arial", 14)).grid(row=0, column=0, columnspan=5)

        # Create list of foods
        self.food_types = [  Food("Apple", "healthy"),
                        Food("Burger", "unhealthy"),
                        Food("Cookie", "neutral"),
                        Food("Magic Cookie", "radioactive"),
                        Food("Cyanide", "deadly"),
                        Food("Red Mushrooms", "healthy"),
                        Food("Blue Mushrooms", "radioactive"),
                        Food("Pink Mushrooms", "deadly"),
                        Food("Pizza", "unhealthy"),
                        Food("Salad", "unhealthy"),
                        Food("Spinach", "radioactive"),
                        Food("Ice Cream", "unhealthy"),
                        Food("Fruit Salad", "healthy"),
                        Food("Pufferfish", "deadly"),
                        Food("Wine", "neutral"),
                        Food("Sandwich", "healthy"),
                        Food("Cucumber", "healthy"),
                        ]

        # Create food buttons
        self.create_food_buttons()
        
        # Start time loop
        self.update_time()

    def create_food_buttons(self):
        # Clear existing buttons
        for button in self.food_buttons:
            button.destroy()
        self.food_buttons.clear()

        # Randomly pick up to 3 foods to create buttons for
        random_foods = random.sample(self.food_types, min(3, len(self.food_types)))
        for i, food in enumerate(random_foods):
            row = 1
            col = i
            button = tk.Button(self.interaction_frame, text=food.name, width=25, command=lambda f=food: self.feed_character(f))
            button.grid(row=1, column=i, padx=5, pady=5)
            self.food_buttons.append(button)

    def feed_character(self, food: Food):
        # Feed character and update stats
        self.character.eat(food)
        self.update_stats()
    
    def update_stats(self):
        # Update stats on the GUI
        self.stat_labels["Age"].config(text=f"{self.character.get_age_string()}")
        self.stat_labels["Weight"].config(text=f"{self.character.attributes['weight']} kg")
        self.stat_labels["Height"].config(text=f"{self.character.attributes['height']} cm")
        self.stat_labels["Health"].config(text=f"{self.character.attributes['health']}")
        self.stat_labels["Fitness"].config(text=f"{self.character.attributes['fitness']}")
        self.stat_labels["Happiness"].config(text=f"{self.character.attributes['happiness']}")
        self.stat_labels["Hunger"].config(text=f"{self.character.attributes['hunger']}")
        self.stat_labels["Hair Length"].config(text=f"{self.character.attributes['hair_length']} cm")

    def update_time_speed(self, event):
        # Update time_speed based on slider value
        self.character.time_speed = self.time_slider.get()

    def update_time(self):
        # Simulate time passing
        self.character.pass_time()
        self.update_stats()
        self.update_body_size()

        if self.character.has_super_strength:
            self.character.time_since_effect+=1
        if random.random() < 0.1: # random chance of resetting available foods
            self.create_food_buttons()
        if not self.character.dead:
            self.root.after(REFRESH_RATE, self.update_time) # Call every 1 second

 
    def update_body_size(self):
        # Update body on GUI based on height and weight
        body_top = 150
        body_left = 120
        body_right = body_left + (self.character.attributes["weight"] * 4)
        body_bottom = body_top + (self.character.attributes["height"] * 2)
        self.character_canvas.delete("body")

        self.character_canvas.create_rectangle(body_left, body_top, body_right, body_bottom, fill=self.character.body_colour, tags="body")

        head_width = self.character.attributes["weight"] * 5  # Head width scales with weight
        head_height = self.character.attributes["height"] * 1.5  # Head height scales with height

        # Position the head(s) above the body, keeping them centered
        head_center_x = (body_left + body_right) / 2
        head_top = body_top - head_height*0.8
        head_left = head_center_x - (head_width / 1.7)
        head_right = head_center_x + (head_width / 10)
        head_bottom = body_top

        

        print(body_left - body_right)

        self.head_right = head_right
        self.head_left = head_left
        self.head_top = head_top
        self.head_bottom = head_bottom
        self.head_width = head_width
        self.head_height = head_height

        add = 7 + (body_right - body_left)*0.3


        # Clear existing heads
        self.character_canvas.delete("head")
        self.character_canvas.delete("head2")

        if self.character.head_number == 1:
            # Draw a single head
            self.character_canvas.create_oval(
                head_left, head_top, head_right+add, head_bottom, fill=self.character.head_colour, tags="head"
            )
        elif self.character.head_number == 2:
            # Draw two heads
            spacing = 0.5  # Space between the two heads
            first_head_left = head_left - (head_width / 2)
            first_head_right = first_head_left + head_width
            second_head_left = head_right 
            second_head_right = second_head_left + head_width

            # Draw first head
            self.character_canvas.create_oval(
                first_head_left, head_top, first_head_right, head_bottom, fill=self.character.head_colour, tags="head"
            )

            # Draw second head
            self.character_canvas.create_oval(
                second_head_left, head_top, second_head_right, head_bottom, fill=self.character.head_colour, tags="head2"
            )
