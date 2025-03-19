# Handles GUI elements

import tkinter as tk
from tkinter import PhotoImage
from src.deck import get_random_card

def start_gui():
    """Initialize the main UI window."""
    root = tk.Tk()
    root.title("Ultimate Texas Hold'em")
    root.geometry("800x600")

    label = tk.Label(root, text="Welcome to Ultimate Texas Hold'em!", font=("Arial", 16))
    label.pack(pady=20)

    # Label to display card image
    card_label = tk.Label(root)
    card_label.pack(pady=20)

    def show_card():
        card_path = get_random_card()
        if card_path:
            card_img = PhotoImage(file=card_path)
            card_label.config(image=card_img)
            card_label.image = card_img  # Keep a reference to prevent garbage collection

    start_button = tk.Button(root, text="Start Game", font=("Arial", 14), command=show_card)
    start_button.pack()

    quit_button = tk.Button(root, text="Quit", font=("Arial", 14), command=root.quit)
    quit_button.pack(pady=10)

    root.mainloop()
