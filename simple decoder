import string

alphabet = string.ascii_uppercase

# Simple Rotors
rotor1 = "BDFHJLCPRTXVZNYEIWGAKMUSQO"
rotor2 = "AJDKSIRUXBLHWTMCQGZNPYFVOE"
rotor3 = "EKMFLGDQVZNTOWYHXUSPAIBRCJ"

# Reflector
reflector = {
    "A":"Y","Y":"A","B":"R","R":"B","C":"U","U":"C","D":"H","H":"D",
    "E":"Q","Q":"E","F":"S","S":"F","G":"L","L":"G","I":"P","P":"I",
    "J":"X","X":"J","K":"N","N":"K","M":"O","O":"M","T":"Z","Z":"T",
    "V":"W","W":"V"
}

# Rotater
def rotate(rotor):
    return rotor[1:] + rotor[0]

# Encoder
def encode_letter(letter, r1, r2, r3):
    idx = alphabet.index(letter)

    letter = r1[idx]
    idx = alphabet.index(letter)
    letter = r2[idx]
    idx = alphabet.index(letter)
    letter = r3[idx]

    letter = reflector[letter]

    idx = r3.index(letter)
    letter = alphabet[idx]
    idx = r2.index(letter)
    letter = alphabet[idx]
    idx = r1.index(letter)
    letter = alphabet[idx]

    return letter

def enigma(message):
    global rotor1, rotor2, rotor3
    output = ""

    for char in message.upper():
        if char not in alphabet:
            output += char
            continue

        encoded = encode_letter(char, rotor1, rotor2, rotor3)
        output += encoded
        rotor1 = rotate(rotor1)

        if output.count("") % 26 == 0:
            rotor2 = rotate(rotor2)
        if output.count("") % (26*26) == 0:
            rotor3 = rotate(rotor3)

    return output

msg = input("Message: ")
print("Encrypted/Decrypted:", enigma(msg))
