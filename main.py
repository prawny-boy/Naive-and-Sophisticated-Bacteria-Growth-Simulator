"""
(1) Compare a naive and sophisticated model
(2) Time for a sophisticated model to reach the target population
(3) Compare two sophisticated population models
(4) Generate detailed projections formatted as columns
(5) Model increases in fission-event frequency
"""
seconds_in_unit = {"d": 86400, "hd": 86400 / 2, "qd": 86400 / 4, "h": 3600, "m": 60, "s": 1,}

class TimeAmount:
    def __init__(self, quantity:float, unit:str):
        self.quantity = quantity
        self.unit = unit
    
    def convert(self, to_unit: str, percentage:bool = False):
        if percentage:
            self.quantity /= 100
        converted = (seconds_in_unit[self.unit.lower()] / seconds_in_unit[to_unit.lower()]) * self.quantity
        self.quantity = converted
        self.unit = to_unit
        return converted
    
    def get_quantity(self):
        return self.quantity
    
    def get_unit(self):
        return self.unit

def calculate_population_size(initial_population: float, growth_rate: TimeAmount, projection_time: TimeAmount, variable_to_output = "population", output_unit = "h", fission_rate: TimeAmount = -1):
    growth_rate.convert(output_unit, True)
    # print(growth_rate.get_quantity())
    projection_time.convert(output_unit)
    # print(projection_time.get_quantity())
    initial_population = float(initial_population)
    if variable_to_output == "population":
        if fission_rate == -1:
            return round(initial_population * (1 + (growth_rate.get_quantity()) * projection_time.get_quantity()))
        else:
            # A = P(1 + r/n)^(nt)
            fission_rate.convert(output_unit)
            return round(initial_population * (1 + growth_rate.get_quantity() / fission_rate.get_quantity()) ** (fission_rate.get_quantity() * projection_time.get_quantity()))
    
def calculate_population_target():
    pass

def compare_sophisticated_models():
    pass

def input_time_amount(prompt: str, validation_error_message: str = "Invalid. First value must be a number."):
    while True:
        try:
            user_input = input(prompt).split()
            amount = user_input[0]
            unit = user_input[1]
            if unit not in seconds_in_unit:
                print(f"Invalid. Incorrect unit. {list(seconds_in_unit.keys())}")
                continue
            amount = float(amount)
            return TimeAmount(amount, unit)
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
    growth_rate = input_time_amount(f"Enter the growth rate (%) and its time unit {list(seconds_in_unit.keys())}: ", "Invalid. First value must be a number. (E.g. 7% = 7)")

    projection_time = input_time_amount(f"Enter the projection time and its time unit {list(seconds_in_unit.keys())}: ")

    result = calculate_population_size(initial_population, growth_rate, projection_time)
    print(f"Population after {projection_time.get_quantity()} {projection_time.get_unit()}: {result}")
