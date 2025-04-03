# Handles GUI elements
import customtkinter as ctk
from PIL import Image, ImageTk
from src import player
from src import deck
# Global variables
root = None
main_frame = None
settings_frame = None
game_frame = None
logo_ctk_image = None
chips_var = None
DEFAULT_CHIPS = player.DEFAULT_CHIPS

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


#deal cards
def deal_player(player_box):
    for widget in player_box.winfo_children():
        widget.destroy()  # Clear previous cards

    card_1_path, card_2_path = deck.deal_player_cards()

    for card_path in [card_1_path, card_2_path]:
        if card_path:
            img = Image.open(card_path).resize((80, 120), Image.Resampling.LANCZOS)
            ctk_img = ctk.CTkImage(light_image=img, size=(80, 120))
            label = ctk.CTkLabel(player_box, image=ctk_img, text="")
            label.image = ctk_img  # Keep reference to avoid garbage collection
            label.pack(side="left", padx=5)


community_cards = [] 
def deal_communityThree(community_box):
    # Clear previous cards
    for widget in community_box.winfo_children():
        widget.destroy()
    # Deal the first three community cards
    card_1_path, card_2_path, card_3_path = deck.deal_communityThree_cards()

    global community_cards
    community_cards = [card_1_path, card_2_path, card_3_path]
    # Deal the first three cards
    for card_path in [card_1_path, card_2_path, card_3_path]:
        if card_path:
            img = Image.open(card_path).resize((80, 120), Image.Resampling.LANCZOS)
            ctk_img = ctk.CTkImage(light_image=img, size=(80, 120))
            label = ctk.CTkLabel(community_box, image=ctk_img, text="")
            label.image = ctk_img  # Keep reference to avoid garbage collection
            label.pack(side="left", padx=5)
    
    card_back_path = "assets/cards/card_back.png"  
    for _ in range(2):  
        img = Image.open(card_back_path).resize((80, 120), Image.Resampling.LANCZOS)
        ctk_img = ctk.CTkImage(light_image=img, size=(80, 120))
        label = ctk.CTkLabel(community_box, image=ctk_img, text="")
        label.image = ctk_img  
        label.pack(side="left", padx=5)  

def deal_communityTwo(community_box):
    # Clear previous cards
    for widget in community_box.winfo_children():
        widget.destroy()

    global community_cards
    for card_path in community_cards:
        if card_path:
            img = Image.open(card_path).resize((80, 120), Image.Resampling.LANCZOS)
            ctk_img = ctk.CTkImage(light_image=img, size=(80, 120))
            label = ctk.CTkLabel(community_box, image=ctk_img, text="")
            label.image = ctk_img  # Keep reference to avoid garbage collection
            label.pack(side="left", padx=5)


    card_4_path, card_5_path = deck.deal_communityTwo_cards()
    for card_path in [card_4_path, card_5_path]:
        if card_path:
            img = Image.open(card_path).resize((80, 120), Image.Resampling.LANCZOS)
            ctk_img = ctk.CTkImage(light_image=img, size=(80, 120))
            label = ctk.CTkLabel(community_box, image=ctk_img, text="")
            label.image = ctk_img  # Keep reference to avoid garbage collection
            label.pack(side="left", padx=5)


# Create the game layout
def create_game_screen():
    global game_frame

    game_frame = ctk.CTkFrame(root, fg_color="transparent")
    game_frame.pack(expand=True, fill="both", padx=20, pady=20)

    title_label = ctk.CTkLabel(game_frame, text="Ultimate Texas Hold'em", font=("Arial", 28, "bold"))
    title_label.pack(pady=(10, 20))


    #deal button's
    deal_player_button = ctk.CTkButton(game_frame, text="Deal Player Cards", font=("Arial", 16, "bold"), command=lambda: deal_player(player_box))
    deal_player_button.pack(pady=20)

    deal_communityThree_button= ctk.CTkButton(game_frame, text="Deal Community 3 Cards", font=("Arial", 16, "bold"), command=lambda: deal_communityThree(community_box))
    deal_communityThree_button.pack(pady=20)
    deal_communityTwo_button= ctk.CTkButton(game_frame, text="Deal Community Last Two Cards", font=("Arial", 16, "bold"), command=lambda: deal_communityTwo(community_box))
    deal_communityTwo_button.pack(pady=20)

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

    


    # ----- Betting Circles Layout -----
    # Helper to create a circular chip slot
    def create_bet_circle(parent, label_text, bet_var):
        container = ctk.CTkFrame(parent, fg_color="transparent")
        container.pack(side="left", padx=10)

        circle = ctk.CTkFrame(container, width=60, height=60, corner_radius=30, fg_color="#2e2e2e")
        circle.pack()

        label = ctk.CTkLabel(container, text=label_text, font=("Arial", 12))
        label.pack(pady=(5, 0))

        # Bet value label that shows the bet placed
        bet_label = ctk.CTkLabel(container, textvariable=bet_var, font=("Arial", 12, "bold"))
        bet_label.pack(pady=(5, 0))

    # Row 1: Ante + Blind (goes into same grid spot chips used to be in)
    row1 = ctk.CTkFrame(game_area, fg_color="transparent")
    row1.grid(row=1, column=2, pady=(0, 0))
    ante_bet_var = ctk.StringVar(value="0") 
    blind_bet_var = ctk.StringVar(value="0")  
    create_bet_circle(row1, "Ante", ante_bet_var)
    create_bet_circle(row1, "Blind", blind_bet_var)

    # Row 2: Play
    row2 = ctk.CTkFrame(game_area, fg_color="transparent")
    row2.grid(row=2, column=2, pady=(0, 2))
    play_bet_var = ctk.StringVar(value="0")  
    create_bet_circle(row2, "Play", play_bet_var)

    # Function to update the label with selected chip amount and update the bets
    def update_chip_label(amount):
        chip_display_label.configure(text=f"Selected {amount} chip bet size. Place your bet as you please.")
        ante_bet_var.set(str(amount)) 
        blind_bet_var.set(str(amount))  
        play_bet_var.set(str(amount))  

    # Chip amount selector buttons
    chip_selector_frame = ctk.CTkFrame(game_frame, fg_color="transparent")
    chip_selector_frame.pack(pady=(0, 10))

    def create_chip_button(amount):
        button = ctk.CTkButton(chip_selector_frame, text=str(amount), width=60, font=("Arial", 14), corner_radius=20, 
                                command=lambda: update_chip_label(amount))
        return button

    # Add the label to display the chip selection message
    chip_display_label = ctk.CTkLabel(game_frame, text="", font=("Arial", 18))
    chip_display_label.pack(pady=(10, 20))

    # Add buttons for chip amounts
    for amount in [1, 10, 100, 1000, 10000]:
        btn = create_chip_button(amount)
        btn.pack(side="left", padx=5)


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




