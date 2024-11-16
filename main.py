from character import Character
from food import Food

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