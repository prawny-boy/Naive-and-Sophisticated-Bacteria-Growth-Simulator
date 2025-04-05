from termcolor import colored, cprint
import sys

def limited_input(choices: list = ["y", "n"], prompt: str = "Pick an option:", prompt_separator: str = ", ", prompt_colour: str = "yellow", prompt_attrs: list = ["bold"], error: str = "Invalid. Please try again.", error_colour: str = "red", error_attrs: list = []):
    choices = [str(choice) for choice in choices]
    cprint(prompt, prompt_colour, attrs=prompt_attrs)
    cprint("Options:", end=" ", attrs=["bold"])
    print(prompt_separator.join(choices))
    number_choices = [str(i + 1) for i in range(len(choices))]
    while True:
        answer = input(": ").lower()
        if answer in choices:
            return answer
        if answer in number_choices:
            return choices[int(answer) - 1]
        if answer in ["q", "quit"]:
            sys.exit()
        cprint(error, error_colour, attrs=error_attrs)

def listed_input(choices: dict = {"y": "yes", "n": "no"}, prompt: str = "Pick an option:", choice_separator: str = " | ", error: str = "Invalid. Please try again.", return_key: bool = False):
    cprint(prompt, "yellow", attrs=["bold"])
    for key, value in choices.items():
        print(f"{key}{choice_separator}{value}")
    values_list = [str(value).lower() for value in choices.values()]
    number_choices = [str(i + 1) for i in range(len(choices))]
    while True:
        answer = input(": ").lower()
        if answer in choices:
            key_answer = answer
        elif answer in values_list:
            key_answer = list(choices.keys())[values_list.index(answer)]
        elif answer in number_choices:
            key_answer = list(choices.keys())[int(answer) - 1]
        elif answer in ["q", "quit"]:
            cprint("Selected Quit Program", "green")
            sys.exit()
        else:
            cprint(error, "red", attrs=["bold"])
            continue
        cprint(f"Selected {choices[key_answer]}\n", "green")
        return key_answer if return_key else choices[key_answer]

def ranged_input(start: int, end: int, prompt: str = "Choose a number:", error: str = "Invalid. Please try again.", infinite_end: bool = False):
    if infinite_end:
        end = "∞"
    cprint(prompt, "yellow", attrs=["bold"])
    while True:
        answer = input(f"Pick between {start} to {end}: ")
        if answer in ["q", "quit"]:
            cprint("Selected Quit Program", "green")
            sys.exit()
        try:
            answer = int(answer)
        except ValueError:
            cprint(error, "red", attrs=["bold"])
            continue
        if (infinite_end and answer >= start) or (not infinite_end and start <= answer <= end):
            cprint(f"Selected {answer}", "green")
            return answer
        cprint(error, "red", attrs=["bold"])

def print_table(data: list[list], table_length: int, table_title: str = "RESULTS TABLE", titles: list = ["Round", "Choice", "Action", "Outcome"], table_buffer: int = 2):
    longest_string = max(len(str(value)) for row in data + [titles] for value in row)
    cprint(table_title, attrs=["bold"])
    print("")
    for title in titles:
        print(colored(title, attrs=["underline"]), end=" " * (longest_string - len(str(title)) + table_buffer))
    print("")
    for i in range(table_length):
        for row in data:
            value = row[i] if i < len(row) else ""
            print(str(value), end=" " * (longest_string - len(str(value)) + table_buffer))
        print("")
    print("")

def time_amount_input(min:int, max:int, prompt:str = "Enter a time amount: ", infinite_end:bool = False, avaliable_units:dict = {"day": "d", "half-day": "hd", "quarter-day": "qd", "hour": "h", "minute": "m", "second": "s"}) -> list[int, str]:
    if infinite_end:
        max = "∞"
    cprint(prompt, "yellow", attrs=["bold"])
    while True:
        user_input = input(f"Enter a number ({min}-{max}) and an unit: ").split()
        if len(user_input) != 2:
            if user_input[0] in ["q", "quit"]:
                cprint("Selected Quit Program", "green")
                sys.exit()
            elif user_input[0] in ["help", "h"]:
                cprint("Available units:", "yellow")
                for key in avaliable_units.keys():
                    print(f"{key}", end=", " if key != list(avaliable_units.keys())[-1] else "")
                print(".")
            elif user_input[0] in avaliable_units.keys() or user_input[0] in avaliable_units.values():
                unit = user_input[0]
                if user_input[0] in avaliable_units.values():
                    unit = list(avaliable_units.keys())[list(avaliable_units.values()).index(unit)]
                amount = 1
                if (min <= 1 <= max) or (infinite_end and 1 >= min):
                    cprint(f"Selected {amount} {unit}(s)", "green")
                    return amount, unit
                else:
                    print(f"Invalid. Enter a number between {min} and {max}.")
                    continue
            else:
                print("Invalid. Enter in format 'number<space>unit'.")
            continue
        amount = user_input[0]
        if amount.isnumeric():
            amount = int(amount)
            if amount < min or (not infinite_end and amount > max):
                print(f"Invalid. Enter a number between {min} and {max}.")
                continue
        else:
            print("Invalid. First value must be a number.")
            continue
        unit = user_input[1]
        if unit not in list(avaliable_units.keys()):
            if unit in avaliable_units.values():
                unit = list(avaliable_units.keys())[list(avaliable_units.values()).index(unit)]
            else:
                print(f"Invalid. Incorrect unit. Enter 'help' for list of units.")
                continue
        cprint(f"Selected {amount} {unit}(s)", "green")
        return amount, unit