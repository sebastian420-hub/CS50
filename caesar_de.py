import sys

if len(sys.argv) > 1:
    key_one = int(sys.argv[1])
    key_two = int(sys.argv[2])
    key_three = int(sys.argv[3])
    text = input("Enter a cipertext: ")

else:
    key_one = int(input("Key 1: "))
    key_two = int(input("Key 2: "))
    key_three = int(input("Key 3: "))
    text = input("Enter a cipertext: ")

characters = [",", ".", " ", "!", "?", "'", '"', ":", ";", "-", "_", "(", ")", "[", "]", "{", "}", "<", ">", "/", "\\"]
upper_case = [chr(i) for i in range(65, 91)]
lower_case = [chr(i) for i in range(97, 123)]


def main():
    final_result = decrypt_text(key_one, key_two, key_three, text)
    print("Decrypted text: ", final_result)


def decrypt_text(key_one, key_two, key_three, text):
    result_one = ""
    result_two = ""
    result_three = ""

    for i in text:
        if i != characters:
            if i in upper_case:
                result_one += chr((ord(i) - key_one - 65) % 26 + 65)
            elif i in lower_case:
                result_one += chr((ord(i) - key_one - 97) % 26 + 97)
            else:
                result_one += i

    for i in result_one:
        if i != characters:
            if i in upper_case:
                result_two += chr((ord(i) - key_two - 65) % 26 + 65)
            elif i in lower_case:
                result_two += chr((ord(i) - key_two - 97) % 26 + 97)
            else:
                result_two += i

    for i in result_two:
        if i != characters:
            if i in upper_case:
                result_three += chr((ord(i) - key_three - 65) % 26 + 65)
            elif i in lower_case:
                result_three += chr((ord(i) - key_three - 97) % 26 + 97)
            else:
                result_three += i

    return result_three


if __name__ == "__main__":
    main()