import tkinter as tk
from tkinter import simpledialog
from character import Character
from gui import GUI
from food import Food

def main():
    name = simpledialog.askstring(title="Enter Name",
                                  prompt="Enter name:")
    character = Character(name)

    # Start the GUI
    root = tk.Tk()
    gui = GUI(root, character)
    character.set_gui(gui)
    root.mainloop()

if __name__ == "__main__":
    main()
