SECONDS_IN_UNIT = {"d": 86400, "hd": 86400 / 2, "qd": 86400 / 4, "h": 3600, "m": 60, "s": 1,}
MODULE_SETTINGS = [
    {
        "name": "Compare a naive and sophisticated model",
        "output": "population",
        "condition": "none",
        "naive_models": 1,
        "sophisticated_models": 1,
    },
    {
        "name": "Time for a sophisticated model to reach the target population",
        "output": "list",
        "condition": "population",
        "naive_models": 0,
        "sophisticated_models": 1,
    },
    {
        "name": "Compare population models",
        "output": "population",
        "condition": "none",
        "naive_models": 0,
        "sophisticated_models": 2,
    },
    {
        "name": "Generate detailed projections formatted as columns",
        "output": "columns",
        "condition": "varied",
        "naive_models": 0,
        "sophisticated_models": 1,
    },
    {
        "name": "Model increases in fission-event frequency",
        "output": "population",
        "condition": "fission",
        "naive_models": 0,
        "sophisticated_models": 1,
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

# Functions
def naive_model_input(number = ""):
    print(f"\nNaive Model {number}")
    initial_population = input_number_value("Enter the initial population: ")
    growth_rate = input_time_amount(f"Enter the growth rate (%) and its time unit (d, hd, qd, h, m, s): ", "Invalid. First value must be a number. (E.g. 7% = 7)")
    return (initial_population, growth_rate)

def sophisticated_model_input(number = ""):
    print(f"\nSophisticated Model {number}")
    initial_population = input_number_value("Enter the initial population: ")
    growth_rate = input_time_amount(f"Enter the growth rate (%) and its time unit (d, hd, qd, h, m, s): ", "Invalid. First value must be a number. (E.g. 7% = 7)")
    fission_frequency = input_time_amount(f"Enter the fission frequency and its unit (d, hd, qd, h, m, s): ")
    return (initial_population, growth_rate, fission_frequency)

def projection_time_input():
    print("\nProjection Timeframe")
    projection_time = input_time_amount(f"Enter the projection time and its time unit (d, hd, qd, h, m, s): ")
    return projection_time

def target_population_input(extra = ""):
    return input_number_value(f"Enter the target population {extra}: ")

def calculate_population_size(initial_population: float, growth_rate: TimeAmount, projection_time: TimeAmount, fission_frequency: TimeAmount) -> float:
    initial_population = float(initial_population)
    growth_rate.convert(projection_time.get_unit())

    if fission_frequency == None:
        return round(initial_population * ((1 + growth_rate.get_quantity()) * projection_time.get_quantity()))
    else:
        growth_rate.convert(fission_frequency.get_unit())
        projection_time.convert(fission_frequency.get_unit())
        return initial_population * ((1 + growth_rate.get_quantity() / growth_rate.get_quantity() / 100) ** (fission_frequency.get_quantity() * projection_time.get_quantity()))
        
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

def summary(data:list[tuple[str, int, TimeAmount, TimeAmount]], settings, projection_time, target_population):
    # write a summary of what the user inputted
    naive_model_count = 0
    sophisticated_model_count = 0
    for model in data:
        model_type = model[0]
        if model_type == "naive":
            model_number = naive_model_count
            naive_model_count += 1
        else:
            model_number = sophisticated_model_count
            sophisticated_model_count += 1
        model_population = model[1]
        model_growth_rate = model[2].get_quantity()
        model_growth_unit = model[2].get_unit()
        fission_frequency = model[3] if len(model) > 3 else None

        print(f"{model_type.title()} Model {model_number}: I = {model_population}, g = {model_growth_rate}% per {model_growth_unit}", end=", ")

        print(f"Fission Event Frequency: {fission_frequency.get_quantity()} {fission_frequency.get_unit()}") if model_type == "sophisticated" else print("")

        if projection_time != None:
            print(f"Projected Timeframe: {projection_time}")
        if target_population != None:
            print(f"Target Population: {target_population}")

def calculate_models(list_of_models:list[tuple[str, int, TimeAmount, TimeAmount, TimeAmount]]):
    results = {}
    result = 0
    sophisticated_model_count = 1
    naive_model_count = 1
    opening_population = []
    added_population = []
    final_population = []
    for model in list_of_models:
        model_type, initial_population, growth_rate, fission_frequency, projection_time = model[:5]

        if model_type == "naive":
            result = calculate_population_size(initial_population, growth_rate, projection_time, fission_frequency)
            results[f"Naive Model {naive_model_count}"] = result
            naive_model_count += 1
        elif model_type == "sophisticated":
            result = calculate_population_size(initial_population, growth_rate, projection_time, fission_frequency)
            results[f"Sophisticated Model {sophisticated_model_count}"] = result
            sophisticated_model_count += 1

        opening_population.append(initial_population)
        added_population.append(result - initial_population)
        final_population.append(result)

def compile_data(list_of_models):
    pass

def run_module(module_number: int):
    # run the module based on the module number and settings
    """
    (1) Compare a naive and sophisticated model
    (2) Time for a sophisticated model to reach the target population
    (3) Compare two sophisticated population models
    (4) Generate detailed projections formatted as columns
    (5) Model increases in fission-event frequency
    """
    settings = MODULE_SETTINGS[module_number - 1]
    print(f"\nModule {module_number}: {settings['name']}")

    # Get data for models
    data = []
    for i in range(settings["naive_models"]):
        data.append(tuple(["naive"]) + naive_model_input(i + 1) + tuple([None]))
    for i in range(settings["sophisticated_models"]):
        data.append(tuple(["sophisticated"]) + sophisticated_model_input(i + 1))

    # Get projection time or target population
    # set these variables to begin calculation
    target_population = None
    projection_time = None
    stop_by_population = False
    split_projection_time = False

    if settings["condition"] == "population":
        target_population = target_population_input()
        stop_by_population = split_projection_time = True
    elif settings["condition"] == "varied":
        target_population = target_population_input("(Enter 0 for stopping after a projected time)")
        if target_population == 0:
            projection_time = projection_time_input()
            split_projection_time = True
        else:
            stop_by_population = split_projection_time = True
    else:
        projection_time = projection_time_input()

    # summarise data inputted
    summary(data, settings, projection_time, target_population)

    stop_by_projection_time = False
    if split_projection_time:
        if not stop_by_population:
            target_projection_time = projection_time
            stop_by_projection_time = True
        projection_time = TimeAmount(0, data[0][3].get_unit())

    data = compile_data(data)
    
    results, opening_population, added_population, final_population = calculate_models(data)

    # Results
    print("\nResults")
    if settings["output"] == "columns":
        # format the output as columns
        columns = zip(opening_population, added_population, final_population)
        for column in columns:
            print(column)
    elif settings["output"] == "list":
        print_list = []
        for model, result in results.items(): 
            print_list.append(result)
        if stop_by_population:
            print(f"Forward Projection: {print_list}")
            print(f"\nTime Taken: {projection_time.get_quantity()} {projection_time.get_unit()}")
        else:
            print(f"Models (In order of input): {print_list}")
    else:
        # print the results based on the output type
        for model, result in results.items():
            print(f"{model}: {result}")

if __name__ == "__main__":
    run_module(4)