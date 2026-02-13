import random

number_to_be_guess=random.randint(1,100)
attempt =0

while True:
    print("Welcome to number guessing game")
    attempt +=1

    guess=int(input("Enter your number :"))

    if guess !=number_to_be_guess:
        print(f"Wrong guess the expected number is {number_to_be_guess},try again")

    else:
        print(f"{guess} is the expected number ,hurray")

    