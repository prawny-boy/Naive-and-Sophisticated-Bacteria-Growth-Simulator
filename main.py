SECONDS_IN_UNIT = {"d": 86400, "hd": 86400 / 2, "qd": 86400 / 4, "h": 3600, "m": 60, "s": 1,}
MODULE_SETTINGS = [
    {
        "name": "Compare a naive and sophisticated model",
        "output": "population",
        "naive_models": 1,
        "sophisticated_models": 1,
        "special": {"format": False, "list": False},
    },
    {
        "name": "Time for a sophisticated model to reach the target population",
        "output": "time",
        "naive_models": 0,
        "sophisticated_models": 1,
        "special": {"format": False, "list": True},
    },
    {
        "name": "Compare two sophisticated population models",
        "output": "population",
        "naive_models": 0,
        "sophisticated_models": 2,
        "special": {"format": False, "list": False},
    },
    {
        "name": "Generate detailed projections formatted as columns",
        "output": "population",
        "naive_models": 0,
        "sophisticated_models": 2,
        "special": {"format": True, "list": False},
    },
    {
        "name": "Model increases in fission-event frequency",
        "output": "population",
        "sophisticated_models": 1,
        "special": {"format": False, "list": True},
    },
]

class TimeAmount:
    def __init__(self, quantity:float, unit:str):
        self.quantity = quantity
        self.unit = unit
    
    def convert(self, to_unit: str):
        converted = (SECONDS_IN_UNIT[self.unit.lower()] / SECONDS_IN_UNIT[to_unit.lower()]) * self.quantity
        self.quantity = converted
        self.unit = to_unit
        return converted
    
    def get_quantity(self):
        return self.quantity
    
    def get_unit(self):
        return self.unit

class GetData:
    # to store all the inputting functions into a class for easier sorting and calling
    def naive_model():
        pass

    def sophisticated_model():
        pass

    def projection_time():
        pass

    def target_population():
        pass

def calculate_population_size(initial_population: float, growth_rate: TimeAmount, projection_time: TimeAmount, fission_frequency: TimeAmount = TimeAmount(-1, "h"), variable_to_output = "population"):
    initial_population = float(initial_population)
    growth_rate.quantity /= 100
    growth_rate.convert(projection_time.get_unit())

    if variable_to_output == "population":
        if fission_frequency.get_quantity() == -1:
            return round(initial_population * ((1 + growth_rate.get_quantity()) * projection_time.get_quantity()))
        else:
            if fission_frequency.get_quantity() == 1:
                # convert to same unit as projected time
                fission_frequency.convert(projection_time.get_unit())
            f = fission_frequency.get_quantity()
            return round(initial_population * ((1 + growth_rate.get_quantity() / f) ** (f * projection_time.get_quantity())), 2)
        

def input_time_amount(prompt: str, validation_error_message: str = "Invalid. First value must be a number."):
    while True:
        try:
            user_input = input(prompt).split()
            amount = user_input[0]
            unit = user_input[1]
            if unit not in list(SECONDS_IN_UNIT.keys()):
                print(f"Invalid. Incorrect unit. {list(SECONDS_IN_UNIT.keys())}")
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

def run_module(module_number: int):
    # run the module based on the module number and settings
    """
    (1) Compare a naive and sophisticated model
    (2) Time for a sophisticated model to reach the target population
    (3) Compare two sophisticated population models
    (4) Generate detailed projections formatted as columns
    (5) Model increases in fission-event frequency
    """
    pass

if __name__ == "__main__":
    print("Naive Model")
    n_initial_population = input_number_value("Enter the initial population: ")
    n_growth_rate = input_time_amount(f"Enter the growth rate (%) and its time unit (d, hd, qd, h, m, s): ", "Invalid. First value must be a number. (E.g. 7% = 7)")
    print("\nSophisticated Model")
    s_initial_population = input_number_value("Enter the initial population: ")
    s_growth_rate = input_time_amount(f"Enter the growth rate (%) and its time unit (d, hd, qd, h, m, s): ", "Invalid. First value must be a number. (E.g. 7% = 7)")
    fission_frequency = input_time_amount(f"Enter the fission frequency and its unit (d, hd, qd, h, m, s): ")

    print("\nFuture Projection Timeframe")
    projection_time = input_time_amount(f"Enter the projection time and its time unit (d, hd, qd, h, m, s): ")

    n_result = calculate_population_size(n_initial_population, n_growth_rate, projection_time)
    s_result = calculate_population_size(s_initial_population, s_growth_rate, projection_time, fission_frequency)

    print(f"Population after {projection_time.get_quantity()} {projection_time.get_unit()}")
    print(f"Naive population: {n_result}")
    print(f"Sophisticated population: {s_result}")