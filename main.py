from character import Character
from food import Food

def main():
    food_types = [Food("Apple", "healthy"),
                  Food("Burger", "unhealthy"),
                  Food("Cookie", "neutral"),
                  Food("Magic Cookie", "radioactive"),
                  Food("Cyanide", "deadly"),
                  Food("Mysterious Red Mushrooms", "healthy"),
                  Food("Mysterious Blue Mushrooms", "radioactive"),
                  Food("Mysterious Pink Mushrooms", "deadly"),
                  ]
    
    name = input("Enter a name: ")
    character = Character(name)

    while not character.dead:
        print(f"Age: {character.age:.1f}")
        print(f"Attributes: {character.attributes}")
        print(f"Effects: {character.effects}")

        print("\nFood types:")
        for i, food in enumerate(food_types, 1):
            print(f"{i}. {food.name} ({food.type})")

        action = input("\nWhat do you want to do? feed/pass time/quit ")
        if action == "feed":
            food_choice = input(f"\nPick a food between number (1-{len(food_types)}) ")

            try:
                food_index = int(food_choice) - 1
                if 0 <= food_index < len(food_types):
                    selected_food = food_types[food_index]
                    character.eat(selected_food)
                    character.pass_time()
                else:
                    print("Invalid food choice")
            except ValueError:
                print("Invalid food choice")
        elif action == "pass time":
            character.pass_time()
        elif action == "quit":
            print("Quitting")
            break
        else:
            print("Invalid input")
        
        print()
    
    if character.dead:
        print(f"{character.name} died...")

    print(f"{character.name}'s final attributes:")
    for key, val in character.attributes.items():
        print(f"{key}: {val}")

if __name__ == "__main__":
    main()
