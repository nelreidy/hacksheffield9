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

    def eat(self, food: Food):
        # Apply effects to character attributes based on food being consumed
        if self.dead:
            print(f"{self.name} is dead!")
            return

        print(f"{self.name} is eating {food.name} ({food.type})")

        if food.type == 'healthy':
            self._healthy_effect()
        elif food.type == 'unhealthy':
            self._unhealthy_effect()
        elif food.type == 'deadly':
            self._deadly_effect()
        elif food.type == 'radioactive':
            self._radioactive_effect()
        elif food.type == 'neutral':
            self._neutral_effect(food)
        else:
            print(f"{food.name} has an unknown effect on {self.name}.")
        
        self._check_attributes()

    def _healthy_effect(self):
        print(f"{self.name} feels healthier, fitter, and grows a little!")

        self.attributes["hunger"] += 20
        self.attributes["health"] += 10
        self.attributes["fitness"] += 5
        self.attributes["height"] += 1
        self.attributes["hair_length"] += 2
        self.attributes["happiness"] += 5

    def _unhealthy_effect(self):
        print(f"{self.name} feels unfit but happier...")

        self.attributes["hunger"] += 10
        self.attributes["health"] -= 10
        self.attributes["fitness"] -= 5
        self.attributes["happiness"] += 10

    def _deadly_effect(self):
        print(f"{self.name} has eaten something deadly... uh oh!")

        self.attributes["health"] = 0
        self.dead = True

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

    def _neutral_effect(self, food: Food):
        print(f"{self.name} ate the {food.name}, but not much happened.")

    def _check_attributes(self):
        # Ensure attributes don't go below zero or exceed reasonable limits
        self.attributes["health"] = max(0, min(self.attributes["health"], MAX_HEALTH))
        self.attributes["fitness"] = max(0, min(self.attributes["fitness"], MAX_FITNESS))
        self.attributes["happiness"] = max(0, min(self.attributes["happiness"], MAX_HAPPINESS))
        self.attributes["height"] = max(BASE_HEIGHT, self.attributes["height"], MAX_HEIGHT)
        self.attributes["weight"] = max(0, self.attributes["weight"])
        self.attributes["hair_length"] = max(0, self.attributes["hair_length"])
        self.attributes["hunger"] = max(0, min(self.attributes["hunger"], MAX_HUNGER))

        if self.attributes["health"] == 0 and not self.dead:
            self.dead = True
            print(f"{self.name} has died due to poor health!")
