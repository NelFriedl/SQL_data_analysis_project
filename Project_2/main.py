"""
projekt_2.py: druhý projekt do Engeto Online Python Akademie

author: Nela Friedlová
email: nela.friedl@gmail.com
"""

import random
import numpy as np
import time

def random_number_generation(length=4) -> list[int]:
    """
    Generates a list of unique digits of specified length 
    with the first non-zero digit.
    
    """
    digits = [random.randint(1, 9)]
    while len(digits) < length:
        digit = random.randint(0, 9)
        if digit not in digits:
                digits.append(digit)
    return digits

def find_duplication(numbers: list) -> bool:
    """Checks for duplicate digits."""
    return len(numbers) != len(set(numbers))

def input_verification() -> list[int] | None:
    """Prompts the player to enter a number and validates it."""
    user_number = input(">>> ")
    if not user_number.isdigit():
        print("This is not a number!")
    elif len(user_number) != 4:
        print("The number must have exactly 4 digits!")
    elif user_number[0] == '0':
        print("The number must not start with zero!")
    elif find_duplication(list(user_number)):
        print("The number must not contain duplications!")
    else:
        return [int(digit) for digit in user_number]
    return None

def cow_value(your_number: list, random_number: list) -> int:
    """Returns the number of the correct values 
    but in the wrong position (cows)."""
    return len(set(your_number) & set(random_number)) - bull_value(your_number, random_number)

def bull_value(your_number: list[int], random_number:list[int]) -> int:
    """Returns the number of correct values 
    in the correct position (bulls)."""
    return int(np.sum(np.array(your_number) == np.array(random_number)))

def format_livestock(value: int, word: str, plural_suffix="s") -> str:
    """Formats the given value with the word in the correct singular/plural form."""
    word_form = word if value ==1 else word + plural_suffix
    return f'{value} {word_form}'

def print_separator(char: str = "-", length: int = 50):
    print(char * length)

def main():
    pc_number = random_number_generation()
    guesses = 0
    print("Hi, there!")
    print_separator()
    print("I've generated a random 4 digit number for you.")
    print("Let's play a Bulls and cows game.")
    print_separator()
    print("Enter a number:")
    print_separator()

    user_number = list()
    start = time.time()
    while user_number != pc_number:
        user_number = input_verification()
        
        guesses += 1
        if user_number is None:
            continue
        cows = cow_value(user_number, pc_number)
        bulls = bull_value(user_number, pc_number)
        print(f"{format_livestock(bulls, 'bull')}, {format_livestock(cows, 'cow')}")
        print_separator()
    stop = time.time()
    print(f'''
Congratulations! You've guessed the right number in 
{(stop - start):.03f} seconds within {guesses} attempts!
''')

if __name__ == "__main__":
    main()