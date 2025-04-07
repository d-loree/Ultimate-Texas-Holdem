# Handles GUI elements
import customtkinter as ctk
from PIL import Image, ImageTk
from src import player, game, deck

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

back_button_game = None

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

def show_result_modal(result_text):
    result_window = ctk.CTkToplevel()
    result_window.title("Game Result")
    result_window.geometry("400x300")

    result_label = ctk.CTkLabel(result_window, text="Game Result", font=("Arial", 22, "bold"))
    result_label.pack(pady=15)

    message_label = ctk.CTkLabel(result_window, text=result_text, font=("Arial", 16), wraplength=350, justify="center")
    message_label.pack(pady=10)

    ok_button = ctk.CTkButton(result_window, text="OK", command=result_window.destroy)
    ok_button.pack(pady=20)

    def set_modal():
        try:
            result_window.grab_set()
        except Exception as e:
            print(f"Failed to set modal grab: {e}")

    result_window.after(100, set_modal)

def update_cards(box, cards):
    for widget in box.winfo_children():
        widget.destroy()

    for card_path in cards:
        if card_path:
            card_image_path = f"assets/cards/{card_path}.png" 
            try:
                img = Image.open(card_image_path).resize((80, 120), Image.Resampling.LANCZOS)
                ctk_img = ctk.CTkImage(light_image=img, size=(80, 120))
                label = ctk.CTkLabel(box, image=ctk_img, text="")
                label.image = ctk_img  
                label.pack(side="left", padx=5)
            except FileNotFoundError:
                print(f"Error: {card_image_path} not found.")


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
    community_box = ctk.CTkFrame(community_section, width=460, height=120, fg_color="transparent")
    community_box.pack_propagate(False)
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
        if player.can_afford(total_bet):
            player.add_ante_chips(selected_chip_amount)
            player.add_blind_chips(selected_chip_amount)
            new_total = int(ante_bet_var.get()) + selected_chip_amount
            ante_bet_var.set(str(new_total))
            blind_bet_var.set(str(new_total))
            chips_var.set(f"Chips: {player.get_chips()}")
        else:
            print("Not enough chips!")
        update_action_buttons()

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
                                fg_color="red", hover_color="#8B0000", corner_radius=20, command=lambda: (undo_bets(), update_action_buttons()))
    undo_button.pack(side="left", padx=5)


    chip_buttons = []

    # Show chip selector only during Bets round
    def update_chip_selector_visibility():
        chip_selector_frame.pack_forget()
        if game.get_current_round() == "Bets":
            chip_selector_frame.pack(before=action_buttons_frame, pady=(0, 10))


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
            start_button = ctk.CTkButton(
                action_buttons_frame,
                text="Deal",
                command=advance_round,
                state="normal" if int(player.get_ante_chips()) > 0 else "disabled",
                fg_color="#3a3a3a" if not int(player.get_ante_chips()) > 0 else None,
                text_color="gray" if not int(player.get_ante_chips()) > 0 else None
            )
            start_button.pack(pady=5)

        if current_round == "Pre-Flop":
            ante = int(ante_bet_var.get())

            x3_btn = ctk.CTkButton(
                action_buttons_frame,
                text="x3",
                command=(lambda: bet_button_pressed(3)) if player.can_afford(ante * 3) else None,
                state="normal" if player.can_afford(ante * 3) else "disabled",
                fg_color="#3a3a3a" if not player.can_afford(ante * 3) else None,
                text_color="gray" if not player.can_afford(ante * 3) else None
            )
            x3_btn.pack(pady=5)

            x4_btn = ctk.CTkButton(
                action_buttons_frame,
                text="x4",
                command=(lambda: bet_button_pressed(4)) if player.can_afford(ante * 4) else None,
                state="normal" if player.can_afford(ante * 4) else "disabled",
                fg_color="#3a3a3a" if not player.can_afford(ante * 4) else None,
                text_color="gray" if not player.can_afford(ante * 4) else None
            )
            x4_btn.pack(pady=5)

            ctk.CTkButton(action_buttons_frame, text="Check", command=advance_round).pack(pady=5)

        elif current_round == "Flop":
            ante = int(ante_bet_var.get())

            x2_btn = ctk.CTkButton(
                action_buttons_frame,
                text="x2",
                command=(lambda: bet_button_pressed(2)) if player.can_afford(ante * 2) else None,
                state="normal" if player.can_afford(ante * 2) else "disabled",
                fg_color="#3a3a3a" if not player.can_afford(ante * 2) else None,
                text_color="gray" if not player.can_afford(ante * 2) else None
            )
            x2_btn.pack(pady=5)

            ctk.CTkButton(action_buttons_frame, text="Check", command=advance_round).pack(pady=5)

        elif current_round == "Turn/River":
            ante = int(ante_bet_var.get())

            x1_btn = ctk.CTkButton(
                action_buttons_frame,
                text="x1",
                command=(lambda: bet_button_pressed(1)) if player.can_afford(ante * 1) else None,
                state="normal" if player.can_afford(ante * 1) else "disabled",
                fg_color="#3a3a3a" if not player.can_afford(ante * 1) else None,
                text_color="gray" if not player.can_afford(ante * 1) else None
            )
            x1_btn.pack(pady=5)

            ctk.CTkButton(action_buttons_frame, text="Fold", command=player_folds).pack(pady=5)


        elif current_round == "Showdown":
            show_button = ctk.CTkButton(action_buttons_frame, text="Play Again", command=reset_game)
            show_button.pack(pady=5)

        if back_button_game:
            if game.get_current_round() in ["Bets", "Showdown"]:
                back_button_game.configure(state="normal")
            else:
                back_button_game.configure(state="disabled")


    def bet_button_pressed(multiplier):
        required_chips = int(ante_bet_var.get()) * multiplier

        if player.can_afford(required_chips):
            player.add_play_chips(required_chips)
            play_bet_var.set(str(required_chips))
            chips_var.set(f"{player.get_chips()} chips")

            # Advance rounds
            if(multiplier == 1):
                advance_round()
            if(multiplier == 2):
                advance_round()
                advance_round()
            if(multiplier == 3 or multiplier == 4):
                advance_round()
                advance_round()
                advance_round()
        else:
            print(f"Cannot afford a x{multiplier} bet. Required: {required_chips}, Available: {player.get_chips()}")
            update_action_buttons()

    def player_folds():
        game.set_folded()
        advance_round()

    # Logic when advancing rounds
    def advance_round():
        if game.get_current_round() == "Bets":
            deck.set_shuffled_deck()
            player_cards = game.draw_starter_hands()
            update_cards(player_box,player_cards)
            print("Bets = Player cards: ", player_cards)
        elif game.get_current_round() == "Pre-Flop":
            community_cards = game.draw_flop_hands()
            update_cards(community_box,community_cards)
            print("Per-Flop = Community cards: ",community_cards)
        elif game.get_current_round() == "Flop":
            community_cards = game.draw_turn_slash_river()
            update_cards(community_box,community_cards)
            print("Flop = Community cards: ",community_cards)
        elif game.get_current_round() == "Turn/River":
            dealer_cards = game.get_dealer_cards()
            update_cards(dealer_box,dealer_cards)
            print("Turn/River = Dealer cards: ", dealer_cards)

            result_text = game.resolve_game()
            show_result_modal(result_text)

            chips_var.set(f"Chips: {player.get_chips()}")
            ante_bet_var.set("0")
            blind_bet_var.set("0")
            play_bet_var.set("0")

        new_round = game.next_round()
        round_label.configure(text=f"Round: {new_round}")
        update_action_buttons()

    def reset_game():
        game.reset_round()

        update_cards(player_box, [])
        update_cards(dealer_box, [])
        update_cards(community_box, [])

        round_label.configure(text=f"Round: {game.get_current_round()}")
        update_action_buttons()

    update_action_buttons()

    # Chips display
    chips_label = ctk.CTkLabel(game_frame, textvariable=chips_var, font=("Arial", 20))
    chips_label.pack(pady=(10, 5))

    # Back button
    global back_button_game
    back_button_game = ctk.CTkButton(game_frame, text="Back to Menu", font=("Arial", 16), corner_radius=10,
                                    command=lambda: show_frame(main_frame))
    back_button_game.pack(pady=20)


# Initialize the GUI application
def start_gui():
    global root, logo_ctk_image

    root = ctk.CTk()
    root.title("Ultimate Texas Hold'em")
    root.geometry("1000x900")

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




