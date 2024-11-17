import _tkinter
import tkinter as tk
from tkinter import ttk
import random
from character import Character
from constants import REFRESH_RATE, MIN_TIME_SPEED, MAX_TIME_SPEED, DATING_AGE
from food import Food

class GUI:
    def __init__(self, root, character):
        self.root = root
        self.character = character
        self.character_canvas = None
        self.stat_labels = {}
        self.food_buttons = []
        self.all_buttons = []

        self.head_left = 0 
        self.head_right = 0 
        self.head_top = 0 
        self.head_bottom = 0 
        self.head_width = 0
        self.head_height = 0
        self.arm_height = 15

        self.setup_ui()
        self.update_stats()

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
        
        self.character.head_colour = "peachpuff"
        self.character.body_colour = "lightblue"

        self.character.head_number = 1

        # Update the head position attributes for future use
        self.head_left = head_left
        self.head_right = head_right
        self.head_top = head_top
        self.head_bottom = head_bottom
        
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

        # Disable inputs
        for button in self.all_buttons:
            try:
                button.config(state=tk.DISABLED)
            except _tkinter.TclError:
                # Button may have already been destroyed
                pass
        self.cut_hair_button.config(state=tk.DISABLED)
        self.exercise_button.config(state=tk.DISABLED)
        self.date_button.config(state=tk.DISABLED)
        self.time_slider.config(state=tk.DISABLED)

    # Bigger arms = stronger
    def strong_arms(self):
        # Delete existing arms
        self.character_canvas.delete("arm")

        # Scaling factor for arms based on character's size (weight and height)
        arm_scale = self.character.attributes["weight"] * 0.3  # You can adjust this multiplier for better scaling
        arm_length = 45 + arm_scale  # Length of the arms will increase with the character's size
        arm_width = 20 + (self.character.attributes["height"] * 0.05)  # Arm width also scales with height

        # Adjust arm positions based on the scaling
        self.character_canvas.create_rectangle(30, 155, 120, 155 + arm_length, fill="peachpuff", tags="arm")  # Left arm
        self.character_canvas.create_rectangle(180, 155, 270, 155 + arm_length, fill="peachpuff", tags="arm")  # Right arm

        self.character.has_super_strength = True

    def normal_arms(self):
        # Delete existing arms
        self.character_canvas.delete("arm")

        # Scaling factor for arms based on character's size (weight and height)
        arm_scale = self.character.attributes["weight"] * 0.2  # Adjust scaling based on weight
        arm_length = 30 + arm_scale  # Default arm length, with a scaling factor
        arm_width = 15 + (self.character.attributes["height"] * 0.03)  # Arm width based on height

        # Adjust arm positions based on the scaling
        self.character_canvas.create_rectangle(60, 155, 120, 155 + arm_length, fill="peachpuff", tags="arm")  # Left arm
        self.character_canvas.create_rectangle(180, 155, 240, 155 + arm_length, fill="peachpuff", tags="arm")  # Right arm


    def setup_ui(self):
        self.root.title("Grown your own Human")
        self.root.geometry("1200x560")

        # Logging frame
        self.log_frame = tk.Frame(self.root, width=600, height=100, bg="white" )
        self.log_frame.grid(row=1, column=1, columnspan=2, padx=10, pady=10 )

        self.log_text = tk.Text(self.log_frame, width=70, height=5, wrap=tk.WORD, bg="white")
        self.log_text.pack(pady=5)

        # Character Canvas
        self.character_frame = tk.Frame(self.root, width=300, height=400, bg="white")
        self.character_frame.grid(row=0, column=0, rowspan=2, padx=10, pady=10)

        self.character_canvas = tk.Canvas(self.character_frame, width=300, height=400, bg="white")
        self.character_canvas.pack()

        # Draw the character (basic placeholder)
        self.character_canvas.create_oval(100, 80, 150, 150, fill="peachpuff", tags="head")  # Head
        self.character_canvas.create_rectangle(120, 150, 180, 300, fill="lightblue", tags="body")  # Body
        self.character_canvas.create_rectangle(100, 155, 120, 160, fill="peachpuff", tags="arm")  # Left arm
        self.character_canvas.create_rectangle(130, 155, 150, 160, fill="peachpuff", tags="arm") # Right arm
        
        self.arm_height = 15

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
        tk.Label(self.achievements_frame, text="Achievements", font=("Arial", 14)).grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 10))
        
        self.achievements = {
            "Keep alive for 1 year": False,
            "Keep alive for 5 years": False,
            "Keep alive for 10 years": False,
            "Keep alive for 25 years": False,
            "Feed 5 healthy foods in a row": False,
            "Avoid unhealthy food for 1 year": False,
            "Avoid radioactive food for 1 year": False,
            "Go on 20 dates": False,
            "Go on 5 successful dates in a row": False,
            "Rapunzel": False,
        }

        self.achievement_labels = {}
        max_per_col = 7
        for i, (achievement, status) in enumerate(self.achievements.items()):
            col = i // max_per_col
            row = i % max_per_col + 1

            # Create label
            label = tk.Label(self.achievements_frame, text=achievement, font=("Arial", 12), bg="lightgray")
            label.grid(row=row, column=col, sticky="w", padx=5, pady=5)
            self.achievement_labels[achievement] = label

        # Interaction Section
        self.interaction_frame = tk.Frame(self.root, width=600, height=200, bg="white")
        self.interaction_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
        tk.Label(self.interaction_frame, text="Interaction", font=("Arial", 14)).grid(row=0, column=0, columnspan=5)

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
                        Food("Aging Potion", "magic"),
                        ]

        # Create food buttons
        self.create_food_buttons()

        # Create action buttons
        self.cut_hair_button = tk.Button(self.interaction_frame, text="Cut Hair", width=25, command=self.cut_hair)
        self.cut_hair_button.grid(row=3, column=0, padx=5, pady=10)

        self.exercise_button = tk.Button(self.interaction_frame, text="Exercise", width=25, command=self.exercise)
        self.exercise_button.grid(row=3, column=1, padx=5, pady=10)  

        self.date_button = tk.Button(self.interaction_frame, text="Date", width=25, command=self.go_on_date, state=tk.DISABLED)
        self.date_button.grid(row=3, column=2, padx=5, pady=10)  

        # Start time loop
        self.update_time()

    def update_log(self, new_text):
        self.log_text.config(state=tk.NORMAL)  # Enable editing
        self.log_text.delete(1.0, tk.END)  # Clear the existing text
        self.log_text.insert(tk.END, new_text)  # Insert the new text
        self.log_text.config(state=tk.DISABLED)  # Disable editing again

    def create_food_buttons(self):
        # Clear existing buttons
        for button in self.food_buttons:
            button.destroy()
        self.all_buttons = []
        self.food_buttons.clear()

        # Randomly pick up to 3 foods to create buttons for
        random_foods = random.sample(self.food_types, min(3, len(self.food_types)))
        for i, food in enumerate(random_foods):
            row = 1
            col = i
            button = tk.Button(self.interaction_frame, text=food.name, width=25, command=lambda f=food: self.feed_character(f))
            button.grid(row=2, column=i, padx=5, pady=5, sticky="n")
            self.food_buttons.append(button)
            self.all_buttons.append(button)

    def feed_character(self, food: Food):
        # Feed character and update stats
        self.character.eat(food)
        self.update_stats()
        self.check_achievements()
    
    def cut_hair(self):
        # Cut hair and update stats
        new_len = max(0, self.character.attributes['hair_length'] - 10)
        self.character.attributes['hair_length'] = new_len
        self.update_stats()

    def exercise(self):
        # Exercise and update stats
        self.character.attributes['hunger'] -= random.randint(5, 8)
        self.character.attributes['fitness'] += random.randint(5, 8)
        self.character.attributes['health'] += random.randint(3, 5)
        self.character.attributes['happiness'] += random.randint(3, 5)

    def update_stats(self):
        # Update stats on the GUI
        self.stat_labels["Age"].config(text=f"{self.character.get_age_string()}")
        self.stat_labels["Weight"].config(text=f"{self.character.attributes['weight']:.2f} kg")
        self.stat_labels["Height"].config(text=f"{self.character.attributes['height']:.2f} cm")
        self.stat_labels["Health"].config(text=f"{self.character.attributes['health']}")
        self.stat_labels["Fitness"].config(text=f"{self.character.attributes['fitness']}")
        self.stat_labels["Happiness"].config(text=f"{self.character.attributes['happiness']}")
        self.stat_labels["Hunger"].config(text=f"{self.character.attributes['hunger']:.2f}")
        self.stat_labels["Hair Length"].config(text=f"{self.character.attributes['hair_length']:.2f} cm")

    def check_dating_age(self):
        # Check if character is old enough to date
        if self.character.age >= DATING_AGE:
            self.date_button.config(state=tk.NORMAL)
        
    def go_on_date(self):
        # Go on a date
        self.character.go_on_date()
        self.update_stats()

    def update_time_speed(self, event):
        # Update time_speed based on slider value
        self.character.time_speed = self.time_slider.get()

    def update_time(self):
        # Simulate time passing
        # Method is called repeatedly
        if self.character.dead:
            return

        self.check_dating_age()
        self.character.pass_time()
        self.update_stats()
        self.update_body_size()
        self.check_achievements()
        if self.character.has_super_strength:
            self.character.time_since_effect+=1
        if random.random() < min(0.1 * self.character.time_speed, 1): # random chance of resetting available foods
            self.create_food_buttons()
        if not self.character.dead:
            self.root.after(REFRESH_RATE, self.update_time) # Call every 1 second

    def update_body_size(self):
        # Update body on GUI based on height and weight
        if (self.character.dead):
            return
        
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
            head_bottom += 20
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

        arm_scale = self.character.attributes["weight"] * 0.3  # Scaling factor for arms based on weight
        arm_length = (body_top - body_bottom)*0.2
        arm_width = 20 + (self.character.attributes["height"] * 0.05)  # Arm width scaling

        strength_scale = 15

        if (self.character.has_super_strength)  :
            arm_length = (body_top - body_bottom)*0.5
            strength_scale = 25

        width_scale = body_right - body_left

        # Draw arms based on scaled values
        self.character_canvas.delete("arm")
        self.character_canvas.delete("arm2")
        self.character_canvas.create_rectangle(body_left - width_scale, head_bottom +strength_scale, body_left, head_bottom +strength_scale+ arm_length, fill="peachpuff", tags="arm")  # Left arm
        self.character_canvas.create_rectangle(body_right + width_scale, head_bottom +strength_scale, body_right, head_bottom +strength_scale + arm_length, fill="peachpuff", tags="arm2")  # R

    def update_achievement_status(self, achievement_name):
        # Update achievement to completed
        self.achievements[achievement_name] = True
        self.achievement_labels[achievement_name].config(bg="gold")
    
    def check_achievements(self):
        # Alive achievements
        if self.character.age >= 1 and not self.achievements["Keep alive for 1 year"]:
            self.update_achievement_status("Keep alive for 1 year")
        if self.character.age >= 5 and not self.achievements["Keep alive for 5 years"]:
            self.update_achievement_status("Keep alive for 5 years")
        if self.character.age >= 10 and not self.achievements["Keep alive for 10 years"]:
            self.update_achievement_status("Keep alive for 10 years")
        if self.character.age >= 25 and not self.achievements["Keep alive for 25 years"]:
            self.update_achievement_status("Keep alive for 25 years")
        
        # 5 healthy foods in a row
        if self.character.healthy_food_streak >= 5 and not self.achievements["Feed 5 healthy foods in a row"]:
            self.update_achievement_status("Feed 5 healthy foods in a row")

        # Avoided unhealthy food for 1 year
        if self.character.avoided_unhealthy_time >= 365 and not self.achievements["Avoid unhealthy food for 1 year"]:
            self.update_achievement_status("Avoid unhealthy food for 1 year")

        # Avoided radioactive food for 1 year
        if self.character.avoided_radioactive_time >= 365 and not self.achievements["Avoid radioactive food for 1 year"]:
            self.update_achievement_status("Avoid radioactive food for 1 year")
        
        # Rapunzel (long hair)
        if self.character.attributes["hair_length"] >= 500 and not self.achievements["Rapunzel"]:
            self.update_achievement_status("Rapunzel")
        
        # Dating achievements
        if self.character.successful_dates_streak >= 5 and not self.achievements["Go on 5 successful dates in a row"]:
            self.update_achievement_status("Go on 5 successful dates in a row")
        if self.character.total_dates >= 20 and not self.achievements["Go on 20 dates"]:
            self.update_achievement_status("Go on 20 dates")
