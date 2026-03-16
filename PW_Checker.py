import string
import msvcrt
from getpass import getpass

def get_password(prompt):
    print(prompt, end='', flush=True)
    password = ''
    while True:
        char = msvcrt.getch()
        if char == b'\r':  # Enter key
            print()
            break
        elif char == b'\x08':  # Backspace key
            if password:
                password = password[:-1]
                print('\b \b', end='', flush=True)
        else:
            password += char.decode('utf-8')
            print('*', end='', flush=True)
    return password

def check_password_strength(password):
    score = 0

    if len(password) >= 8:
        score += 1
    if any(char.isupper() for char in password):
        score += 1
    if any(char.islower() for char in password):
        score += 1
    if any(char.isdigit() for char in password):
        score += 1
    if any(char in string.punctuation for char in password):
        score += 1

    return score


while True:
    password = get_password("Enter a password to check (or type 'quit' to stop): ")

    if password.lower() == "quit":
        print("Exiting...")
        break

    strength = check_password_strength(password)

    print("\nStrength Score:", strength, "/ 5")

    if strength <= 2:
        print("Weak password\n")
    elif strength == 3:
        print("Medium strength\n")
    else:
        print("Strong password\n")