def main():
    checker()

def checker():
    card_number = input("Enter your credit card number: ")
    check_company = [str(x) for x in card_number]
    multiplied = card_number[-2::-2]
    non_multiplied = card_number[-1::-2]
    multiplied = [int(x) * 2 for x in multiplied]

    print(multiplied)

    result = []

    for x in multiplied:
        if x > 9:
            x = [int(y) for y in str(x)]
            result.append(sum(x))
        else:
            result.append(x)

    print(result)

    result = sum(result)
    print(result)
    for x in non_multiplied:
        result += int(x)

    print(result)

    if result % 10 == 0 and check_company[0] == "4":
        print("Valid Visa credit card number")


if __name__ == "__main__":
    main()
