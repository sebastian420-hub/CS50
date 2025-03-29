import sys

def get_keys_and_text():
    if len(sys.argv) > 1:
        try:
            key = int(sys.argv[1])
            text = input("Enter a text: ")
        except ValueError:
            print("Please enter valid keys")
            sys.exit(1)
    else:
        try:
            key = int(input("Key: "))
        except ValueError:
            print("Please enter valid keys")
            sys.exit(1)
        text = input("Enter a text: ")
    return key, text
    

def encrypt_char(char,key,base):
    if char.isalpha():
        return chr((ord(char) + key - base) % 26 + base)
    return char

def encrypt_text(key,text):
    characters = [",", ".", " ", "!", "?", "'", '"', ":", ";", "-", "_", "(", ")", "[", "]", "{", "}", "<", ">", "/", "\\"]
    result = ""
    for i in text:
        if i is not characters:
                result += encrypt_char(i,key,65 if i.isupper() else 97)
    return result

if __name__ == "__main__":
    key, text = get_keys_and_text()
    final_result = encrypt_text(key, text)
    print("CipherText: ", {final_result})