def main():
    cc_checker()

def cc_checker():
    credit_card = input("Enter your credit card number: ")
    check_com = [str(x) for x in credit_card]
    multiplied = credit_card[-2::-2]
    non_multiplied = credit_card[-1::-2]
    multiplied = [int(x) for x in multiplied]
    multiplied = [x * 2 for x in multiplied]

    result = []

    for x in multiplied:
        if x > 9:
            x = [int(y) for y in str(x)]
            result.append(sum(x))
        else:
            result.append(x)

    result = sum(result)

    for x in non_multiplied:
        result += int(x)


    if result % 10 == 0 and check_com[0] == "4":
        print("Valid Visa credit card number")
    elif result % 10 == 0 and check_com[0] == "5":
        print("Valid Mastercard credit card number")
    elif result % 10 == 0 and check_com[0] == "3":
        print("Valid American Express credit card number")
            

    


if __name__ == "__main__":
    main()

