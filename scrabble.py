letters = {
    "A": 1, "B": 3, "C": 3, "D": 2, "E": 1, "F": 4, "G": 2, "H": 4, "I": 1, "J": 8, "K": 5, "L": 1, "M": 3, "N": 1, "O": 1, "P": 3, "Q": 10, "R": 1, "S": 1, "T": 1, "U": 1, "V": 4, "W": 4, "X": 8, "Y": 4, "Z": 10
}
def main():
    scrabbler()

def scrabbler():
    player1 = input("Enter a word: ")
    player2 = input("Enter a word: ")

    sum1 = 0
    sum2 = 0

    for x in player1:
        if x.upper() in letters:
            sum1 += letters[x.upper()]

    for x in player2:
        if x.upper() in letters:
            sum2 += letters[x.upper()]

    print(f"Player 1: {sum1}")
    print(f"Player 2: {sum2}")

    if sum1 > sum2:
        print("Player 1 wins")

    elif sum2 > sum1:
        print("Player 2 wins")

if __name__ == "__main__":
    main()