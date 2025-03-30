"""
(1) Compare a naive and sophisticated model
(2) Time for a sophisticated model to reach the target population
(3) Compare two sophisticated population models
(4) Generate detailed projections formatted as columns
(5) Model increases in fission-event frequency
"""
seconds_in_unit = {"day": 86400, "half_day": 86400 / 2, "quarter_day": 86400 / 4, "hour": 3600, "minute": 60, "second": 1,}

def convert_time(from_unit: str, from_amount: int, to_unit: str):
    return (seconds_in_unit[from_unit.lower()] / seconds_in_unit[to_unit.lower()]) * from_amount

def calculate_population_size(initial_population: float, growth_rate: list[float, str], projection_time: list[float, str], fission_rate: list[float, str] = -1):
    growth_rate_value, growth_rate_unit = growth_rate
    projection_time_value, projection_time_unit = projection_time
    growth_rate_value = convert_time(growth_rate_unit, growth_rate_value, projection_time_unit)
    initial_population = float(initial_population)
    if fission_rate == -1:
        return round(initial_population * (1 + (growth_rate_value / 100) * projection_time_value))
    else:
        # A = P(1 + r/n)^(nt)
        fission_rate_value, fission_rate_unit = fission_rate
        fission_rate_value = convert_time(fission_rate_unit, fission_rate_value, projection_time_unit)
        return round(initial_population * (1 + growth_rate_value / fission_rate_value) ** (fission_rate_value * projection_time_value))
    
def calculate_population_target():
    pass

def compare_sophisticated_models():
    pass

def input_time_with_format(prompt: str, validation_error_message: str = "Invalid. First value must be a number."):
    while True:
        try:
            user_input = input(prompt).split()
            amount = user_input[0]
            unit = user_input[1]
            if unit not in seconds_in_unit:
                print(f"Invalid. Incorrect unit. {list(seconds_in_unit.keys())}")
                continue
            amount = float(amount)
            return [amount, unit]
        except IndexError:
            print("Invalid. Enter in format 'number<space>unit'.")
        except ValueError:
            print(validation_error_message)

def input_number_value(prompt: str):
    while True:
        try:
            return int(input(prompt))
        except:
            print("Invalid. Enter a number.")

if __name__ == "__main__":
    initial_population = input_number_value("Enter the initial population: ")
    growth_rate = input_time_with_format(f"Enter the growth rate (%) and its time unit {list(seconds_in_unit.keys())}: ", "Invalid. First value must be a number. (E.g. 7% = 7)")

    projection_time = input_time_with_format(f"Enter the projection time and its time unit {list(seconds_in_unit.keys())}: ")

    result = calculate_population_size(initial_population, growth_rate, projection_time)
    print(f"Population after {projection_time[0]} {projection_time[1]}: {result}")
