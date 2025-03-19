# Handles GUI elements

import tkinter as tk

def start_gui():
    root = tk.Tk()
    root.title("Ultimate Texas Hold'em")
    root.geometry("800x600")  # Set window size

    label = tk.Label(root, text="Welcome to Ultimate Texas Hold'em!", font=("Arial", 16))
    label.pack(pady=20)

    start_button = tk.Button(root, text="Start Game", font=("Arial", 14), command=lambda: print("Game Started"))
    start_button.pack()

    quit_button = tk.Button(root, text="Quit", font=("Arial", 14), command=root.quit)
    quit_button.pack(pady=10)

    root.mainloop()
