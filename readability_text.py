def main():
    text = input("Enter a text: ")
    result = compute_readability(text)
    print("Grade level: ", round(result))


def count_letters(text):
    count = 0
    for i in text:
        if i != "." and i != "," and i != " ":
            count += 1
    return count

def count_words(text):
    count = 0
    for i in text:
        if i == " ":
            count += 1
    return count

def count_sentences(text):
    count = 0
    for i in text:
        if i == "." or i == "?" or i == "!":
            count += 1
    return count

def compute_readability(text):
    letters = count_letters(text)
    words = count_words(text)
    sentences = count_sentences(text)

    print(f"Letters: {letters}")
    print(f"Words: {words}")
    print(f"Sentences: {sentences}")

    i = letters / words * 100
    j = sentences / words * 100

    index = 0.0588 * i - 0.296 * j - 15.8

    return index

if __name__ == "__main__":
    main()
