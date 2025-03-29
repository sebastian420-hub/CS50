import sys

def get_keys_and_text():
    if len(sys.argv) > 1:
        try:
            key_one, key_two, key_three = map(int, sys.argv[1:4])
            text = input("Enter a text: ")
        except ValueError:
            print("Please enter valid keys")
            sys.exit(1)
    else:
        try:
            key_one = int(input("Key 1: "))
            key_two = int(input("Key 2: "))
            key_three = int(input("Key 3: "))
        except ValueError:
            print("Please enter valid keys")
            sys.exit(1)
        text = input("Enter a text: ")
    return key_one, key_two, key_three, text

def encrypt_char(char,key,base):
    if char.isalpha():
        return chr((ord(char) + key - base) % 26 + base)
    return char

def encrypt_text(key_one, key_two, key_three, text):
    # characters =" ,.!?':;-_()[]{}<>/\\"
    result = text
    for key in (key_one, key_two, key_three):
        result = "".join(encrypt_char(char,key,65 if char.isupper() else 97) for char in result)
    return result

def main():
    key_one, key_two, key_three, text = get_keys_and_text()
    final_result = encrypt_text(key_one, key_two, key_three, text)
    print("Encrypted text: ", {final_result})

if __name__ == "__main__":
    main()