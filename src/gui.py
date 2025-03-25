# Handles GUI elements
import customtkinter as ctk
from PIL import Image, ImageTk
from src import player, game

# Global variables
root = None
main_frame = None
settings_frame = None
game_frame = None
logo_ctk_image = None
chips_var = None
DEFAULT_CHIPS = player.DEFAULT_CHIPS
selected_chip_amount = 1

round_label = None
action_buttons_frame = None

# Betting chip variables
ante_bet_var = None
blind_bet_var = None
play_bet_var = None

# Undo function to return chips from table to player
def undo_bets():
    player.return_chips_from_table()
    chips_var.set(f"Chips: {player.get_chips()}")  # Update chips display
    ante_bet_var.set("0")  # Reset bet labels
    blind_bet_var.set("0")
    play_bet_var.set("0")


# Show the requested frame and hide the others (Also currently updates chips if on main menu)
def show_frame(frame):
    if frame == main_frame:
        chips_var.set(f"Chips: {player.get_chips()}")
    elif frame == settings_frame:
        chips_var.set(str(player.get_chips()))
    elif frame == game_frame:
        chips_var.set(f"{player.get_chips()} chips")

    main_frame.pack_forget()
    settings_frame.pack_forget()
    game_frame.pack_forget()
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
                                 command=lambda: show_frame(game_frame))
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

# Create the game layout
def create_game_screen():
    global game_frame, selected_chip_amount, ante_bet_var, blind_bet_var, play_bet_var, round_label, action_buttons_frame, chip_selector_frame, bet_buttons

    game_frame = ctk.CTkFrame(root, fg_color="transparent")
    game_frame.pack(expand=True, fill="both", padx=20, pady=20)

    title_label = ctk.CTkLabel(game_frame, text="Ultimate Texas Hold'em", font=("Arial", 28, "bold"))
    title_label.pack(pady=(10, 20))

    # Round Label
    round_label = ctk.CTkLabel(game_frame, text=f"Round: {game.get_current_round()}", font=("Arial", 20))
    round_label.pack(pady=(0, 10))

    # Centered game layout
    game_area = ctk.CTkFrame(game_frame, fg_color="transparent")
    game_area.pack()

    game_area.grid_columnconfigure(0, weight=0)  # player/community
    game_area.grid_columnconfigure(1, weight=1)  # spacing
    game_area.grid_columnconfigure(2, weight=0)  # dealer/bet circles

    # Dealer + Community cards row
    community_section = ctk.CTkFrame(game_area, fg_color="#1e1e1e", corner_radius=12)
    community_section.grid(row=0, column=0, padx=(0, 20), pady=10, sticky="w")
    c_label = ctk.CTkLabel(community_section, text="Community Cards", font=("Arial", 16, "bold"))
    c_label.pack(pady=(10, 5))
    community_box = ctk.CTkFrame(community_section, width=300, height=100, fg_color="transparent")
    community_box.pack(padx=20, pady=10)

    dealer_section = ctk.CTkFrame(game_area, fg_color="#1e1e1e", corner_radius=12)
    dealer_section.grid(row=0, column=2, padx=(20, 0), pady=10)
    d_label = ctk.CTkLabel(dealer_section, text="Dealer", font=("Arial", 16, "bold"))
    d_label.pack(pady=(10, 5))
    dealer_box = ctk.CTkFrame(dealer_section, width=160, height=100, fg_color="transparent")
    dealer_box.pack(padx=20, pady=10)

    # Player row
    player_section = ctk.CTkFrame(game_area, fg_color="#1e1e1e", corner_radius=12)
    player_section.grid(row=1, column=0, padx=(0, 20), pady=10, sticky="w")
    p_label = ctk.CTkLabel(player_section, text="Player", font=("Arial", 16, "bold"))
    p_label.pack(pady=(10, 5))
    player_box = ctk.CTkFrame(player_section, width=160, height=100, fg_color="transparent")
    player_box.pack(padx=20, pady=10)

    # Betting values
    ante_bet_var = ctk.StringVar(value="0")
    blind_bet_var = ctk.StringVar(value="0")
    play_bet_var = ctk.StringVar(value="0")

    bet_buttons = {}

    def place_bet(label):
        global selected_chip_amount

        if game.get_current_round() != "Bets":
            print("Betting is only allowed in the Bets round.")
            return

        total_bet = selected_chip_amount * 2
        if player.add_chips_to_table(total_bet):
            new_total = int(ante_bet_var.get()) + selected_chip_amount
            ante_bet_var.set(str(new_total))
            blind_bet_var.set(str(new_total))
            chips_var.set(f"Chips: {player.get_chips()}")
        else:
            print("Not enough chips!")

    # Helper to create a betting chip slot
    def create_bet_circle(parent, label_text, bet_var):
        container = ctk.CTkFrame(parent, fg_color="transparent")
        container.pack(side="left", padx=10)

        is_play_circle = label_text == "Play"
        
        bet_button = ctk.CTkButton(
            container, width=60, height=60, corner_radius=30, 
            fg_color="#2e2e2e",
            text="",
            command=lambda: place_bet(label_text) if not is_play_circle else None,
            hover=False if is_play_circle else True 
        )
        bet_button.pack()

        bet_buttons[label_text] = bet_button

        label = ctk.CTkLabel(container, text=label_text, font=("Arial", 12))
        label.pack(pady=(5, 0))

        bet_label = ctk.CTkLabel(container, textvariable=bet_var, font=("Arial", 12, "bold"))
        bet_label.pack(pady=(5, 0))

    # Row 1: Ante + Blind
    row1 = ctk.CTkFrame(game_area, fg_color="transparent")
    row1.grid(row=1, column=2, pady=(0, 0))
    create_bet_circle(row1, "Ante", ante_bet_var)
    create_bet_circle(row1, "Blind", blind_bet_var)

    # Row 2: Play
    row2 = ctk.CTkFrame(game_area, fg_color="transparent")
    row2.grid(row=2, column=2, pady=(0, 2))
    create_bet_circle(row2, "Play", play_bet_var)

    # Chip amount selector (Shown only in Bets round)
    chip_selector_frame = ctk.CTkFrame(game_frame, fg_color="transparent")
    chip_selector_frame.pack(pady=(0, 10))

    # Undo button
    undo_button = ctk.CTkButton(chip_selector_frame, text="Undo", width=60, font=("Arial", 14),
                                fg_color="red", hover_color="#8B0000", corner_radius=20, command=undo_bets)
    undo_button.pack(side="left", padx=5)


    chip_buttons = []

    # Show chip selector only during Bets round
    def update_chip_selector_visibility():
        if game.get_current_round() == "Bets":
            chip_selector_frame.pack(pady=(0, 10))
        else:
            chip_selector_frame.pack_forget()

    # Enable bet circles only in the Bets round
    def update_bet_circles_state():
        current_round = game.get_current_round()
        is_enabled = (current_round == "Bets")

        for button in bet_buttons.values():
            if is_enabled:
                button.configure(state="normal")
            else:
                button.configure(state="disabled")

    def create_chip_button(amount):
        def on_select():
            global selected_chip_amount
            selected_chip_amount = amount
            update_chip_button_styles()

        button = ctk.CTkButton(chip_selector_frame, text=str(amount), width=60, font=("Arial", 14),
                               corner_radius=20, command=on_select)
        chip_buttons.append((button, amount))
        return button

    for amount in [1, 10, 100, 1000]:
        btn = create_chip_button(amount)
        btn.pack(side="left", padx=5)

    def update_chip_button_styles():
        for btn, amount in chip_buttons:
            if amount == selected_chip_amount:
                btn.configure(fg_color="#3ba336", text_color="white")  # selected
            else:
                btn.configure(fg_color="#2e2e2e", text_color="gray")   # unselected

    update_chip_button_styles()
    update_chip_selector_visibility()
    update_bet_circles_state()

    # Round-based action buttons
    action_buttons_frame = ctk.CTkFrame(game_frame, fg_color="transparent")
    action_buttons_frame.pack(pady=10)

    # Update action buttons and chip visibility based on the round 
    def update_action_buttons():
        for widget in action_buttons_frame.winfo_children():
            widget.destroy()

        update_chip_selector_visibility()
        update_bet_circles_state()

        current_round = game.get_current_round()

        if current_round == "Bets":
            start_button = ctk.CTkButton(action_buttons_frame, text="Deal", command=advance_round)
            start_button.pack(pady=5)

        if current_round == "Pre-Flop":
            bet_button = ctk.CTkButton(action_buttons_frame, text="x3", command=advance_round)
            bet_button.pack(pady=5)
            check_button = ctk.CTkButton(action_buttons_frame, text="x4", command=advance_round)
            check_button.pack(pady=5)
            check_button = ctk.CTkButton(action_buttons_frame, text="Check", command=advance_round)
            check_button.pack(pady=5)

        elif current_round == "Flop":
            bet_button = ctk.CTkButton(action_buttons_frame, text="x2", command=advance_round)
            bet_button.pack(pady=5)
            check_button = ctk.CTkButton(action_buttons_frame, text="Check", command=advance_round)
            check_button.pack(pady=5)

        elif current_round == "Turn/River":
            bet_button = ctk.CTkButton(action_buttons_frame, text="x1", command=advance_round)
            bet_button.pack(pady=5)
            check_button = ctk.CTkButton(action_buttons_frame, text="Fold", command=advance_round)
            check_button.pack(pady=5)

        elif current_round == "Showdown":
            show_button = ctk.CTkButton(action_buttons_frame, text="Play Again", command=reset_game)
            show_button.pack(pady=5)

    def advance_round():
        new_round = game.next_round()
        round_label.configure(text=f"Round: {new_round}")
        update_action_buttons()

    def reset_game():
        game.reset_round()
        round_label.configure(text=f"Round: {game.get_current_round()}")
        update_action_buttons()

    update_action_buttons()

    # Chips display
    chips_label = ctk.CTkLabel(game_frame, textvariable=chips_var, font=("Arial", 20))
    chips_label.pack(pady=(10, 5))

    # Back button
    back_button = ctk.CTkButton(game_frame, text="Back to Menu", font=("Arial", 16), corner_radius=10,
                                command=lambda: show_frame(main_frame))
    back_button.pack(pady=20)

# Initialize the GUI application
def start_gui():
    global root, logo_ctk_image

    root = ctk.CTk()
    root.title("Ultimate Texas Hold'em")
    root.geometry("1000x800")

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
    create_game_screen()

    # Show the main menu right away
    show_frame(main_frame)

    root.mainloop()




