import random

score = 0
possible = ["rock", "paper", "scissors"]

def rps_ai(num_ai):
    if num_ai == 1:
        return "Rock"
    elif num_ai == 2:
        return "Paper"
    else:
        return "Scissors"

while True:
    p_guess = input("What is your guess for rock, paper, scissors? (or 'quit' to exit)\n").lower()
   
    if p_guess == 'quit':
        print(f"Final Score: {score}")
        break
       
    if p_guess not in possible:
        print("Invalid choice. Please try again.")
        continue

    num_ai = random.randint(1, 3)
    ai_choice = rps_ai(num_ai)
   
    print(f"\nYou: {p_guess.capitalize()}")
    print(f"AI: {ai_choice}")

    if p_guess == "rock":
        p = 1
    elif p_guess == "paper":
        p = 2
    else:
        p = 3

    if p == num_ai:
        print("Tie!")
    elif (p == 1 and num_ai == 3) or (p == 2 and num_ai == 1) or (p == 3 and num_ai == 2):
        score += 1
        print("Win!")
    else:
        print("Loss")
       
    print(f"Current Score: {score}\n")
