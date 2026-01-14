# [Group Name]:[DAN/EXT 11]
# [Team Members]
# [Jarrah Brain]-[S392191]
# [Mark Campbell]-[S385026]
# [Craig Shaw]-[S396655]
# [Dan Williams]-[S391056]

import os
print("="*40)
print("          Assignment 2, Q1         ")
print("   Created by: Craig, Jarrah, Mark, Dan ")
print("="*40)


# Provides tools to interact with the operating system (like checking if a file exists)
# initially i had great difficulty with the assignment rules, after the initial encryption it was impossible to identify the original starting posistion of the letter
# I attempted to use the inverse of the encrypt rule for decryption, however this resulted in a unsuccessful decrypt
# if a letter overlapped 2 rules it would be unable to be decrypted e.g. "s" would shift backward 6 (if using shift1=2 and shift2=4) to m but on decryption it would use a different rule to find initial placement
# The rules used for each character would need to be stored in order to reverse the encryption during decryption
# Function: encrypt_file
# "def encrypt_file" defines the function
# The parameters are Shift1, Shift2:cipher keys


def encrypt_file(shift1, shift2):
    try:
        # Open the source file in 'read' mode "r"
        with open("raw_text.txt", "r") as f:
            text = f.read()

        encrypted = []  # stores encrypted characters
        rules = []      # stores which rule was used per character

        for char in text:

            # LOWERCASE
            if 'a' <= char <= 'm':
                shift = shift1 * shift2            # rule 0: lowercase a-m
                # Changes letter to number from 0-25 and adds the calculated shift
                # "% 26" is a modulo operator that makes the shift wrap back around to a
                # chr(), ord(), char converts numbers to characters
                new_char = chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
                rules.append('0')

            elif 'n' <= char <= 'z':
                shift = -(shift1 + shift2)         # rule 1: lowercase n-z
                new_char = chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
                rules.append('1')

            # UPPERCASE
            elif 'A' <= char <= 'M':
                shift = -shift1                     # rule 2: uppercase A-M
                new_char = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
                rules.append('2')

            elif 'N' <= char <= 'Z':
                shift = shift2 ** 2                 # rule 3: uppercase N-Z
                new_char = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
                rules.append('3')

            # SPECIAL CHARACTERS
            else:
                new_char = char                      # rule 4: non-letter, no shift
                rules.append('4')

            encrypted.append(new_char)

        # Write encrypted text
        with open("encrypted_text.txt", "w") as f:
            f.write("".join(encrypted))

        # Write rule metadata
        with open("rules.txt", "w") as f:
            f.write("".join(rules))

        print("Successfully encrypted.")
    # Prevent program from crashing without raw_text file
    except FileNotFoundError:
        print("Error: raw_text.txt not found.")

# Function: decrypt_file
# "def decrypt_file" defines the function


def decrypt_file(shift1, shift2):
    try:
        # Open the encrypted file
        with open("encrypted_text.txt", "r") as f:
            encrypted = f.read()

        # Open the rules file
        with open("rules.txt", "r") as f:
            rules = f.read()

        decrypted = []

        # Apply the exact inverse rule for each character
        for char, rule in zip(encrypted, rules):

            if rule == '0':       # lowercase a-m
                shift = -(shift1 * shift2)
                new_char = chr((ord(char) - ord('a') + shift) % 26 + ord('a'))

            elif rule == '1':     # lowercase n-z
                shift = (shift1 + shift2)
                new_char = chr((ord(char) - ord('a') + shift) % 26 + ord('a'))

            elif rule == '2':     # uppercase A-M
                shift = shift1
                new_char = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))

            elif rule == '3':     # uppercase N-Z
                shift = -(shift2 ** 2)
                new_char = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))

            else:                 # special character
                new_char = char

            decrypted.append(new_char)

        # Write decrypted text
        with open("decrypted_text.txt", "w") as f:
            f.write("".join(decrypted))

        print("Successfully decrypted.")

    except FileNotFoundError:
        print("Error: encrypted_text.txt or rules.txt not found.")

# Function: verify_decryption


def verify_decryption():
    # "try"
    try:
        # Open both files at once and assign variables f1,f2 to use later
        with open("raw_text.txt", "r") as f1, open("decrypted_text.txt", "r") as f2:
            # "rstrip()" removes trailing whitespace to prevent false mismatch errors
            raw = f1.read().rstrip()
            decrypted = f2.read().rstrip()

            # Compare the contents and display the result to user (boolean check)
            if raw == decrypted:
                print("Verification SUCCESS: The files are identical.")
                # opens the text files and assign variables
                with open("raw_text.txt", "r") as f3, open("decrypted_text.txt", "r") as f4:
                    # f3 and f4 are file objects only and are required to be "read"
                    # Files are read and assigned variables
                    raw_text = f3.read()
                    decrypted_text = f4.read()
                    print("raw_text:", raw_text)
                    print("decrypted_text:", decrypted_text)
            else:
                print("Verification FAILED: The files do not match.")
    # "except" prevents the program crashes if file was deleted or in the wrong location
    except FileNotFoundError:
        print("Error: Could not find files for verification.")

# Function: Main


def main():
    try:
        # Ask the user for inputs and convert the string input into integers (int)
        # "int()" = integer, input will always return a string but we require a number
        # "input()" Prompts user to input data
        # "s1,s2" Variables where results are stored
        s1 = int(input("Enter value for shift1: "))
        s2 = int(input("Enter value for shift2: "))

        # Run the sequence of functions
        # runs the encrypt function defined above using the variables s1,s2
        encrypt_file(s1, s2)
        decrypt_file(s1, s2)
        verify_decryption()
    # If the user types something that is not an integer it will prevent crash and disply fault
    except ValueError:
        # "print" displays the string
        print("Please enter valid integers for the shifts.")


# ensures the program runs when the file is executed directly
if __name__ == "__main__":
    main()
# input added to keep script open for reading when running external from terminal or output program.
input("\nPress Enter to close...")
