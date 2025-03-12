import random

# Function to simulate the Prisoner's Dilemma game
def prisoners_dilemma(player_choice):
    # AI Opponent randomly chooses between Cooperate or Betray
    opponent_choice = random.choice(["Cooperate", "Betray"])
    
    # Outcome logic
    if player_choice == "Cooperate" and opponent_choice == "Cooperate":
        result = "Both sides cooperated – Mutual benefit (2 years each)."
    elif player_choice == "Cooperate" and opponent_choice == "Betray":
        result = "You cooperated, but opponent betrayed – You suffer (5 years), they go free."
    elif player_choice == "Betray" and opponent_choice == "Cooperate":
        result = "You betrayed, but opponent cooperated – You go free, they suffer (5 years)."
    else:
        result = "Both betrayed – Both suffer (3 years each)."
    
    return player_choice, opponent_choice, result

# Game loop
while True:
    print("\n🔵 Prisoner's Dilemma Game 🔵")
    print("Choose your action:")
    print("1. Cooperate")
    print("2. Betray")
    
    choice = input("Enter 1 or 2: ").strip()
    
    if choice == "1":
        player_move = "Cooperate"
    elif choice == "2":
        player_move = "Betray"
    else:
        print("Invalid choice. Try again.")
        continue  # Restart loop if input is invalid
    
    # Get game results
    player, opponent, outcome = prisoners_dilemma(player_move)
    
    # Display results
    print(f"\n🟢 You chose: {player}")
    print(f"🔴 Opponent chose: {opponent}")
    print(f"🏆 Outcome: {outcome}")

    # Ask if player wants to play again
    replay = input("\nPlay again? (yes/no): ").strip().lower()
    if replay != "yes":
        break

print("\nGame Over. Thanks for playing!")