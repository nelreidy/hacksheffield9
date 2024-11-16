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

        self.setup_ui()
        self.update_stats()

    # Function to make the character's head turn green (Radioactive)
    def turn_head_green(self):
        # Clear the head and redraw it with green fill
        self.character_canvas.delete("head")
        self.character_canvas.create_oval(100, 50, 200, 150, fill="green", tags="head")
        self.character.head_colour = "green"

    # Function to make the character's head turn normal (Alive/neutral/cured)
    def cure(self):
        # Clear the head and redraw it with peachpuff fill
        self.character_canvas.delete("head")
        self.character_canvas.delete("body")
        self.character_canvas.create_oval(100, 50, 200, 150, fill="peachpuff", tags="head")
        self.character_canvas.create_rectangle(120, 150, 180, 300, fill="lightblue", tags="body")
        
        # reset head colour and number 
        self.character.head_colour = ""
        self.character.head_number = 1
        
    # Function to replace the character with a coffin (Dead)
    def kill(self):
        # Remove character
        self.character_canvas.delete("all")

        # Draw coffin
        coffin_x1, coffin_y1 = 100, 50
        coffin_x2, coffin_y2 = 200, 300
        self.character_canvas.create_rectangle(coffin_x1, coffin_y1, coffin_x2, coffin_y2, fill="saddle brown", tags="coffin")
        self.character_canvas.create_polygon(
            (coffin_x1, coffin_y1, coffin_x1 - 20, coffin_y1 + 50, coffin_x1, coffin_y2, coffin_x2, coffin_y2,
            coffin_x2 + 20, coffin_y1 + 50, coffin_x2, coffin_y1), fill="saddle brown", tags="coffin"
        )

        rip_x = (coffin_x1 + coffin_x2) / 2
        rip_y = coffin_y1 + 40
        self.character_canvas.create_text(rip_x, rip_y, text="RIP", font=("Arial", 20, "bold"), fill="black")

    # Function to make the character grow a 2nd head
    def grow_second_head(self):
        # Clear the head and redraw 2 
        self.character_canvas.delete("head")
        height = 55
        self.character_canvas.create_oval(152, height+6, 252, height + 106, fill="peachpuff", tags="head")
        self.character_canvas.create_oval(48, height, 148, height + 100, fill="peachpuff", tags="head")
        self.character.head_number = 2

    # Function to make the character grow a 2nd green head
    def grow_second_green_head(self):
        # Clear the head and redraw 2 with green fill
        self.character_canvas.delete("head")
        height = 55
        self.character_canvas.create_oval(152, height+6, 252, height + 106, fill="green", tags="head")
        self.character_canvas.create_oval(48, height, 148, height + 100, fill="green", tags="head")

    # Function to make skin glow
    def glowing_skin(self):
        # Clear the body and redraw with gold fill
        self.character_canvas.delete("body")
        self.character_canvas.create_rectangle(120, 150, 180, 300, fill="gold", tags="body")
    
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
        self.character_canvas.create_oval(100, 50, 200, 150, fill="peachpuff", tags="head")  # Head
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
        
        # Achievements Section
        self.achievements_frame = tk.Frame(self.root, width=300, height=400)
        self.achievements_frame.grid(row=0, column=2, padx=10, pady=10, rowspan=2, sticky="n")
        tk.Label(self.achievements_frame, text="Achievements", font=("Arial", 14)).pack(anchor="w")
        
        self.achievements = {
            "Keep alive for 1 year": False,
            "Keep alive for 2 years": False,
            "Keep alive for 5 years": False,
            "Keep alive for 10 years": False,
            "Feed 5 healthy foods in a row": False,
            "Avoid unhealthy food for 1 year": False,
            "Avoid radioactive food for 1 year": False,
        }

        self.achievement_labels = {}
        for achievement, status in self.achievements.items():
            label = tk.Label(self.achievements_frame, text=achievement, font=("Arial", 12), bg="lightgray")
            label.pack(anchor="w", pady=5)
            self.achievement_labels[achievement] = label

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
                        Food("Salad", "healthy"),
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
        # Method is called repeatedly
        self.character.pass_time()
        self.update_stats()
        self.check_achievements()
        if self.character.has_super_strength:
            self.character.time_since_effect+=1
        if random.random() < 0.1: # random chance of resetting available foods
            self.create_food_buttons()
        if not self.character.dead:
            self.root.after(REFRESH_RATE, self.update_time) # Call every 1 second

    def update_achievement_status(self, achievement_name):
        # Update achievement to completed
        self.achievements[achievement_name] = True
        self.achievement_labels[achievement_name].config(bg="gold")
    
    def check_achievements(self):
        # Alive achievements
        if self.character.age >= 1 and not self.achievements["Keep alive for 1 year"]:
            self.update_achievement_status("Keep alive for 1 year")
        if self.character.age >= 2 and not self.achievements["Keep alive for 2 years"]:
            self.update_achievement_status("Keep alive for 2 years")
        if self.character.age >= 5 and not self.achievements["Keep alive for 5 years"]:
            self.update_achievement_status("Keep alive for 5 years")
        if self.character.age >= 10 and not self.achievements["Keep alive for 10 years"]:
            self.update_achievement_status("Keep alive for 10 years")
        
        # 5 healthy foods in a row
        if self.character.healthy_food_streak >= 5 and not self.achievements["Feed 5 healthy foods in a row"]:
            self.update_achievement_status("Feed 5 healthy foods in a row")

        # Avoided unhealthy food for 1 year
        if self.character.avoided_unhealthy_time >= 365 and not self.achievements["Avoid unhealthy food for 1 year"]:
            self.update_achievement_status("Avoid unhealthy food for 1 year")

        # Avoided radioactive food for 1 year
        if self.character.avoided_radioactive_time >= 365 and not self.achievements["Avoid radioactive food for 1 year"]:
            self.update_achievement_status("Avoid radioactive food for 1 year")
