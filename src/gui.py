import customtkinter as ctk
from PIL import Image, ImageTk

# Global variables
root = None
main_frame = None
settings_frame = None
logo_ctk_image = None

# Show the requested frame and hide the others
def show_frame(frame):
    main_frame.pack_forget()
    settings_frame.pack_forget()
    frame.pack(expand=True, fill="both", padx=20, pady=20)

# Change the UI theme dynamically.
def change_theme(mode):
    ctk.set_appearance_mode(mode)

# Create the main menu layout
def create_main_menu():
    global main_frame

    main_frame = ctk.CTkFrame(root, fg_color="transparent")
    main_frame.pack(expand=True, fill="both", padx=20, pady=20)

    logo_label = ctk.CTkLabel(main_frame, image=logo_ctk_image, text="")
    logo_label.pack(pady=(20, 10))

    title_label = ctk.CTkLabel(main_frame, text="Ultimate Texas Hold'em", font=("Arial", 28, "bold"))
    title_label.pack(pady=(0, 30))

    start_button = ctk.CTkButton(main_frame, text="Start Game", font=("Arial", 16), corner_radius=10, command=lambda: print("Game Started"))
    start_button.pack(pady=15)

    settings_button = ctk.CTkButton(main_frame, text="Settings", font=("Arial", 16), corner_radius=10, command=lambda: show_frame(settings_frame))
    settings_button.pack(pady=10)

    quit_button = ctk.CTkButton(main_frame, text="Quit", font=("Arial", 16), corner_radius=10, fg_color="red", hover_color="#8B0000", command=root.quit)
    quit_button.pack(pady=15)

# Create the settings page layout
def create_settings_page():
    global settings_frame

    settings_frame = ctk.CTkFrame(root, fg_color="transparent")
    settings_frame.pack(expand=True, fill="both", padx=20, pady=20)

    title_label = ctk.CTkLabel(settings_frame, text="Settings", font=("Arial", 28, "bold"))
    title_label.pack(pady=(20, 30))

    # Theme Selection (Light/Dark Mode)
    theme_label = ctk.CTkLabel(settings_frame, text="Theme:", font=("Arial", 16))
    theme_label.pack()

    theme_option = ctk.CTkOptionMenu(settings_frame, values=["Dark", "Light"], command=change_theme)
    theme_option.pack(pady=10)

    # Back button
    back_button = ctk.CTkButton(settings_frame, text="Back", font=("Arial", 16), corner_radius=10, command=lambda: show_frame(main_frame))
    back_button.pack(pady=30)

# Initialize the GUI application
def start_gui():
    global root, logo_ctk_image

    root = ctk.CTk()
    root.title("Ultimate Texas Hold'em")
    root.geometry("800x600")

    ctk.set_appearance_mode("dark")  # Default to dark mode

    # Load and resize the logo (maintaining aspect ratio)
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
