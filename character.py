# Simulate how different foods impact the character

import random
from constants import *
from food import Food


class Character:
    def __init__(self, name: str):
        self.name = name
        self.dead = False
        self.age = STARTING_AGE
        self.attributes = { # Various attributes
            "health": BASE_HEALTH,
            "fitness": BASE_FITNESS,
            "happiness": BASE_HAPPINESS,
            "height": BASE_HEIGHT,
            "weight": BASE_WEIGHT,
            "hair_length": BASE_HAIR_LENGTH,
            "hunger": BASE_HUNGER,
        }
        self.effects = []  # Stores special effects like "second head"
        self.time_speed = 1 # How fast time passes
        self.head_colour = "peachpuff"
        self.body_colour = "lightblue"
        self.head_number = 1
        self.has_super_strength = False
        self.time_since_effect = 0

        # Achievements
        self.healthy_food_streak = 0
        self.avoided_unhealthy_time = 0
        self.avoided_radioactive_time = 0

    def set_gui(self, gui):
        self.gui = gui

    def _check_attributes(self):
        # Ensure attributes don't go below zero or exceed reasonable limits
        self.attributes["health"] = max(0, min(self.attributes["health"], MAX_HEALTH))
        self.attributes["fitness"] = max(0, min(self.attributes["fitness"], MAX_FITNESS))
        self.attributes["happiness"] = max(0, min(self.attributes["happiness"], MAX_HAPPINESS))
        self.attributes["height"] = max(BASE_HEIGHT, min(self.attributes["height"], MAX_HEIGHT))
        self.attributes["weight"] = max(0, self.attributes["weight"])
        self.attributes["hair_length"] = max(0, self.attributes["hair_length"])
        self.attributes["hunger"] = max(0, min(self.attributes["hunger"], MAX_HUNGER))

        if self.attributes["health"] == 0 and not self.dead:
            self._kill_character()
            print(f"{self.name} has died due to poor health!")
        
        if self.time_speed < MIN_TIME_SPEED:
            self.time_speed = MIN_TIME_SPEED

        if self.time_since_effect > 3:
            self.has_super_strength = False
            self.time_since_effect = 0

    #-----------------------------------------------------------
    # EATING EFFECTS

    def eat(self, food: Food):
        # Apply effects to character attributes based on food being consumed
        if self.dead:
            print(f"{self.name} is dead!")
            return

        print(f"{self.name} is eating {food.name}")

        if food.type == 'healthy':
            if food.name == 'apple' and random.random() < 0.1:
              # poisoned apple
              print(f"uh oh! the apple was poisoned...")
              self._kill_character()
            else:
              self.healthy_food_streak += 1
              self._healthy_effect()
        elif food.type == 'unhealthy':
            self.healthy_food_streak = 0
            self.avoided_unhealthy_time = 0
            self._unhealthy_effect()
        elif food.type == 'deadly':
            self.healthy_food_streak = 0
            self._deadly_effect()
        elif food.type == 'radioactive':
            self.healthy_food_streak = 0
            self.avoided_radioactive_time = 0
            self._radioactive_effect()
        elif food.type == 'neutral':
            self.healthy_food_streak = 0
            self._neutral_effect(food)
        else:
            self.healthy_food_streak = 0
            print(f"{food.name} has an unknown effect on {self.name}.")
        
        self._check_hungry()
        self._check_attributes()
        self.gui.update_body_size()

    def _check_hungry(self):
        # Check if character has overeaten
        if self.attributes["hunger"] > MAX_HUNGER:
            print(f"{self.name} isn't hungry, the extra food made them feel ill!")
            over_hunger = self.attributes["hunger"] - MAX_HUNGER
            if over_hunger <= 10:
                self.attributes["health"] -= random.randint(1, 5)
                self.attributes["fitness"] -= random.randint(1, 3)
                self.attributes["happiness"] -= 5
            else:
                self.attributes["health"] -= random.randint(10, 20)
                self.attributes["fitness"] -= random.randint(5, 10)
                self.attributes["happiness"] -= random.randint(10, 15)

    def _healthy_effect(self):
        print(f"{self.name} feels healthier, fitter, and grows a little!")

        self.attributes["hunger"] += 5
        self.attributes["health"] += 10
        self.attributes["fitness"] += 5
        self.attributes["height"] += 1
        self.attributes["hair_length"] += 2
        self.attributes["happiness"] += 5
        
        #self.gui.cure()
        if random.random() < 0.35: # low chance of curing you if apple eaten
            self.gui.cure()

    def _unhealthy_effect(self):
        print(f"{self.name} feels unfit but happier...")
        self.has_super_strength = True

        self.attributes["hunger"] += 10
        self.attributes["health"] -= 10
        self.attributes["fitness"] -= 5
        self.attributes["happiness"] += 10
        
    def _deadly_effect(self):
        print(f"{self.name} has eaten something deadly... uh oh!")
        self._kill_character()

    def _radioactive_effect(self):
        print(f"{self.name} has eaten radioactivate food and now something strange is occurring...")

        # Apply a random radioactive effect
        random_effects = [
            ("height", random.randint(-5, 15)),
            ("health", random.randint(-20, 20)),
            ("happiness", random.randint(-10, 10)),
            ("hunger", random.randint(-20, 20))
        ]
        for attr, effect in random_effects:
            self.attributes[attr] += effect

        # Unique effect
        if random.random() < 0.35:
            strange_effect = random.choice(RADIOACTIVE_EFFECTS)
            self.effects.append(strange_effect)

            print(f"{self.name} has gained {strange_effect}")

            if strange_effect == "super strength":
                self.attributes["fitness"] += 20
                self.has_super_strength = True
            elif strange_effect == "green head":
                if self.head_number == 2:
                    self.gui.grow_second_green_head()
                else:
                    self.gui.turn_head_green()
            elif strange_effect == "a second head":
                if self.head_colour == "green":
                    self.gui.grow_second_green_head()
                else:
                    self.gui.grow_second_head()
            elif strange_effect == "glowing skin":
                self.gui.glowing_skin()
    

    def _neutral_effect(self, food: Food):
        self.attributes["hunger"] += 20
        print(f"{self.name} ate the {food.name}, but not much happened.")

        self.attributes["hunger"] += random.randint(1, 5)

    #-----------------------------------------------------------
    # AGING/TIME EFFECTS

    def _kill_character(self):
        # Kill the character
        self.attributes["health"] = 0
        self.dead = True
        self.gui.kill()

    def _aging_effect(self):
        # Apply effects based on age of character
        if self.age >= 150:
            self._kill_character()
            print(f"{self.name} has died of old age :(")
        elif self.age >= 80:
            self.attributes["health"] -= 5
            print(f"{self.name} is feeling the effects of old age...")

    def pass_time(self):
        # Pass 1 day, adjusted by time speed
        days = self.time_speed
        self.age += days / 365
        self.attributes["hunger"] -= days * 0.5
        self.attributes["hair_length"] += days * 0.5

        # Update achievements
        self.avoided_radioactive_time += self.time_speed
        self.avoided_unhealthy_time += self.time_speed

        if self.attributes["hunger"] <= 0.0:
            print(f"{self.name} starved to death!")
            self._kill_character()
        elif self.attributes["hunger"] <= STARVING_LEVEL:
            self.attributes["health"] -= 5
            print(f"{self.name} is starving!")
        
        if self.attributes["height"] < MAX_HEIGHT:
            self.attributes["height"] += 0.25
            self.attributes["weight"] += 0.1

        self._aging_effect()
        self._check_attributes()

    def get_age_string(self):
        # Return a string of the age in year + months
        years = int(self.age)
        months = round((self.age - years) * 12)
        return f"{years} years, {months} months"
    