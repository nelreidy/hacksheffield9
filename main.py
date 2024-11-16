import tkinter as tk
from character import Character
from gui import GUI
from food import Food

def main():
    name = input("Enter a name: ")
    character = Character(name)

    # Start the GUI
    root = tk.Tk()
    gui = GUI(root, character)
    character.set_gui(gui)
    root.mainloop()

if __name__ == "__main__":
    main()
