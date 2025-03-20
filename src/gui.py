# Handles GUI elements
import customtkinter as ctk
from PIL import Image, ImageTk
from src import player

# Global variables
root = None
main_frame = None
settings_frame = None
logo_ctk_image = None
chips_var = None
DEFAULT_CHIPS = player.DEFAULT_CHIPS

# Show the requested frame and hide the others (Also currently updates chips if on main menu)
def show_frame(frame):
    if frame == main_frame:
        chips_var.set(f"Chips: {player.get_chips()}")
    elif frame == settings_frame:
        chips_var.set(str(player.get_chips()))

    main_frame.pack_forget()
    settings_frame.pack_forget()
    frame.pack(expand=True, fill="both", padx=20, pady=20)

# Toggle dark/light mode
def change_theme(mode):
    ctk.set_appearance_mode(mode)

# Save chips value from entry field
def save_config_gui():
    player.set_chips(chips_var.get())

# Reset chips to default and update input field
def reset_chips_gui():
    player.reset_chips()
    chips_var.set(str(player.get_chips()))

# Create the main menu layout
def create_main_menu():
    global main_frame, chips_var

    main_frame = ctk.CTkFrame(root, fg_color="transparent")
    main_frame.pack(expand=True, fill="both", padx=20, pady=20)

    logo_label = ctk.CTkLabel(main_frame, image=logo_ctk_image, text="")
    logo_label.pack(pady=(20, 10))

    title_label = ctk.CTkLabel(main_frame, text="Ultimate Texas Hold'em", font=("Arial", 28, "bold"))
    title_label.pack(pady=(0, 20))

    # Single variable for both display & input
    chips_var = ctk.StringVar(value=f"Chips: {player.get_chips()}")
    chips_label = ctk.CTkLabel(main_frame, textvariable=chips_var, font=("Arial", 18))
    chips_label.pack(pady=(0, 30))

    start_button = ctk.CTkButton(main_frame, text="Start Game", font=("Arial", 16), corner_radius=10,
                                 command=lambda: print(f"Game Started with {player.get_chips()} chips"))
    start_button.pack(pady=15)

    settings_button = ctk.CTkButton(main_frame, text="Settings", font=("Arial", 16), corner_radius=10,
                                    command=lambda: show_frame(settings_frame))
    settings_button.pack(pady=10)

    quit_button = ctk.CTkButton(main_frame, text="Quit", font=("Arial", 16), corner_radius=10,
                                fg_color="red", hover_color="#8B0000", command=root.quit)
    quit_button.pack(pady=15)

# Create the settings page layout
def create_settings_page():
    global settings_frame, chips_var

    settings_frame = ctk.CTkFrame(root, fg_color="transparent")
    settings_frame.pack(expand=True, fill="both", padx=20, pady=20)

    title_label = ctk.CTkLabel(settings_frame, text="Settings", font=("Arial", 28, "bold"))
    title_label.pack(pady=(20, 30))

    # Theme Selection (Light/Dark Mode)
    theme_label = ctk.CTkLabel(settings_frame, text="Theme:", font=("Arial", 16))
    theme_label.pack()

    theme_option = ctk.CTkOptionMenu(settings_frame, values=["Dark", "Light"], command=change_theme)
    theme_option.pack(pady=10)

    # Chips input
    chips_label = ctk.CTkLabel(settings_frame, text="Chips:", font=("Arial", 16))
    chips_label.pack()

    chips_var.set(str(player.get_chips()))
    chips_entry = ctk.CTkEntry(settings_frame, textvariable=chips_var, font=("Arial", 16))
    chips_entry.pack(pady=10)

    # Save chips and Reset buttons
    save_button = ctk.CTkButton(settings_frame, text="Save", font=("Arial", 16), corner_radius=10,
                                command=save_config_gui)
    save_button.pack(pady=10)

    reset_button = ctk.CTkButton(settings_frame, text=f"Reset to {DEFAULT_CHIPS}", font=("Arial", 16), corner_radius=10,
                                 command=reset_chips_gui)
    reset_button.pack(pady=10)

    # Back button
    back_button = ctk.CTkButton(settings_frame, text="Back", font=("Arial", 16), corner_radius=10,
                                command=lambda: show_frame(main_frame))
    back_button.pack(pady=30)

# Initialize the GUI application
def start_gui():
    global root, logo_ctk_image

    root = ctk.CTk()
    root.title("Ultimate Texas Hold'em")
    root.geometry("800x600")

    ctk.set_appearance_mode("dark")  # Default to dark mode

    # Load logo
    logo_path = "assets/logo.png"
    original_width, original_height = 384, 191
    new_width = 300
    new_height = int((new_width / original_width) * original_height)

    logo_image = Image.open(logo_path).resize((new_width, new_height), Image.Resampling.LANCZOS)
    logo_ctk_image = ctk.CTkImage(light_image=logo_image, size=(new_width, new_height))

    create_main_menu()
    create_settings_page()

    # Show the main menu right away
    show_frame(main_frame)

    root.mainloop()
