# Simulate how different foods impact the character

import random
from food import Food

class Character:
    def __init__(self, name):
        self.name = name
        self.attributes = {
            "health": 50,          # Base health level
            "fitness": 50,         # Physical fitness level
            "happiness": 50,       # General happiness
            "height": 150,         # Height in centimeters
            "hair_length": 10,     # Hair length in centimeters
        }
        self.effects = []  # Stores special effects like "second head"
        self.dead = False

    def eat(self, food):
        print(f"{self.name} is eating {food.name} ({food.type})")
        if food.type == 'healthy':
            self.attributes["health"] += 10
            self.attributes["fitness"] += 5
            self.attributes["height"] += 1
            self.attributes["hair_length"] += 2
            print(f"{self.name} feels healthier, fitter, and grows a little taller!")
        elif food.type == 'unhealthy':
            self.attributes["health"] -= 10
            self.attributes["fitness"] -= 5
            self.attributes["happiness"] -= 10
            print(f"{self.name} feels unfit and sad after eating unhealthy food.")
        elif food.type == 'deadly':
            self.attributes["health"] = 0
            self.dead = True
            print(f"{self.name} has eaten something deadly and... it's not good.")
        elif food.type == 'radioactive':
            strange_effect = random.choice(["second head", "glowing skin", "super strength"])
            self.effects.append(strange_effect)
            self.attributes["health"] -= 5
            print(f"{self.name} has eaten radioactive food and now has a strange effect: {strange_effect}!")
        elif food.type == 'neutral':
            print(f"{self.name} eats the {food.name}, but nothing much happens.")
        else:
            print(f"{food.name} has an unknown effect on {self.name}.")
        
        self._check_attributes()

    def _check_attributes(self):
        # Ensure attributes don't go below zero or exceed reasonable limits
        self.attributes["health"] = max(0, min(self.attributes["health"], 100))
        self.attributes["fitness"] = max(0, min(self.attributes["fitness"], 100))
        self.attributes["happiness"] = max(0, min(self.attributes["happiness"], 100))
        self.attributes["height"] = max(100, min(self.attributes["height"], 250))  # Character height range
        self.attributes["hair_length"] = max(0, min(self.attributes["hair_length"], 100))

# Example Usage
if __name__ == "__main__":
    apple = Food("Apple", "healthy")
    burger = Food("Burger", "unhealthy")
    uranium = Food("Uranium", "radioactive")
    cookie = Food("Cookie", "neutral")
    poison = Food("Poison", "deadly")

    character = Character("Alex")
    character.eat(apple)
    character.eat(burger)
    character.eat(uranium)
    character.eat(cookie)
    character.eat(poison)

    print(f"\n{character.name}'s final attributes: {character.attributes}")
    print(f"Special effects: {character.effects}")
    if character.dead: 
        print(f"{character.name} is dead.")
