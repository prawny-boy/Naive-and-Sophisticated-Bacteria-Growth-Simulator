from print_functions import *

SECONDS_IN_UNIT = {"day": 86400, "half-day": 86400 / 2, "quarter-day": 86400 / 4, "hour": 3600, "minute": 60, "second": 1}
SIMULATION_SETTINGS = [
    {
        "name": "Compare a naive and sophisticated model",
        "output": "final",
        "condition": "projected",
        "naive_models": 1,
        "sophisticated_models": 1,
        "graph": False,
    },
    {
        "name": "Time for a sophisticated model to reach the target population",
        "output": "list",
        "condition": "population",
        "naive_models": 0,
        "sophisticated_models": 1,
        "graph": False,
    },
    {
        "name": "Compare population models",
        "output": "list",
        "condition": "projected",
        "naive_models": 0,
        "sophisticated_models": 2,
        "graph": False,
    },
    {
        "name": "Generate detailed projections formatted as columns",
        "output": "columns",
        "condition": "varied",
        "naive_models": 0,
        "sophisticated_models": 1,
        "graph": False,
    },
    {
        "name": "Model increases in fission-event frequency",
        "output": "final",
        "condition": "fission",
        "naive_models": 0,
        "sophisticated_models": 1,
        "graph": False,
    },
    # Presets start here
    {
        "name": "Graph the comparsion of a naive and sophisticated model",
        "output": "list",
        "condition": "projected",
        "naive_models": 1,
        "sophisticated_models": 1,
        "graph": True,
    },
    {
        "name": "Graph the comparison of two sophisticated models",
        "output": "list",
        "condition": "projected",
        "naive_models": 0,
        "sophisticated_models": 2,
        "graph": True,
    },
    {
        "name": "Compare two naive models",
        "output": "final",
        "condition": "projected",
        "naive_models": 2,
        "sophisticated_models": 0,
        "graph": False,
    },
    {
        "name": "Graph the population growth of a naive model",
        "output": "list",
        "condition": "projected",
        "naive_models": 1,
        "sophisticated_models": 0,
        "graph": True,
    },
    {
        "name": "Graph the population growth of a sophisticated model",
        "output": "list",
        "condition": "projected",
        "naive_models": 0,
        "sophisticated_models": 1,
        "graph": True,
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
def calculate_population_size(model_type: str, initial_population: float, growth_rate: TimeAmount, fission_frequency: TimeAmount, projection_time: TimeAmount) -> float:
    initial_population = float(initial_population)
    projection_time.convert(growth_rate.get_unit())
    rate = TimeAmount(growth_rate.get_quantity(), growth_rate.get_unit())
    rate.quantity /= 100

    if model_type == "naive":
        return initial_population + (rate.get_quantity() * initial_population * projection_time.get_quantity())

    if model_type == "sophisticated":
        fission_frequency.convert(rate.get_unit())
        rate_over_fission = rate.get_quantity() * fission_frequency.get_quantity()
        total_fission_events = projection_time.get_quantity() / fission_frequency.get_quantity()
        return initial_population * ((1 + rate_over_fission) ** total_fission_events)

def input_custom_settings():
    print_title("Input Custom Settings")
    naive_models = ranged_input(0, 10, "Enter the number of naive models: ")
    sophisticated_models = ranged_input(0, 10, "Enter the number of sophisticated models: ")
    output = listed_input(
        choices = {"final": "Final Population Size", 
                   "list": "List of Populations over Time", 
                   "columns": "Columns of Populations over Time (start, added, end)"},
        prompt = "Select the output type:",
        return_key=True,
    )
    condition = listed_input(
        choices = {"population": "Target Population", 
                   "varied": "Varied Population",   
                   "projected": "Projected Time"},
        prompt = "Select the condition type:",
        return_key=True,
    )
    print_title("Selected Settings")
    print(f"Output: {output.capitalize()}, Condition: {condition.capitalize()}")
    print(f"Naive Models: {naive_models}, Sophisticated Models: {sophisticated_models}")
    return {
        "name": "Custom Settings",
        "output": output,
        "condition": condition,
        "naive_models": naive_models,
        "sophisticated_models": sophisticated_models,
    }

def summary(models_data, projection_time:TimeAmount, target_population:TimeAmount, condition:str):
    print_title("Summary")
    naive_model_count = 0
    sophisticated_model_count = 0
    for model in models_data:
        model_type = model[0]
        if model_type == "naive":
            model_number = naive_model_count
            naive_model_count += 1
        else:
            model_number = sophisticated_model_count
            sophisticated_model_count += 1
        model_population:int = model[1]
        model_growth_rate:int = model[2].get_quantity()
        model_growth_unit:str = model[2].get_unit()
        fission_frequency:TimeAmount = model[3] if len(model) > 3 else None

        print(f"{model_type.title()} Model {model_number}: I = {model_population}, g = {model_growth_rate}% per {model_growth_unit}", end="")

        print(f", Fission Event Frequency: {fission_frequency.get_quantity()} {fission_frequency.get_unit()}(s)") if model_type == "sophisticated" else print("")

        if condition == "projected":
            print(f"Projected Timeframe: {projection_time.get_quantity()} {projection_time.get_unit()}(s)")
        if condition == "population":
            print(f"Target Population: {target_population}")

def calculate_models(calculate_data:list[list[list]]):
    results:dict[str, list] = {}
    model_configuration:dict[str, list[int|TimeAmount]] = {}
    model_result = 0
    sophisticated_model_count = 1
    naive_model_count = 1
    opening_population:list[list] = []
    added_population:list[list] = []
    final_population:list[list] = []
    for i in range(len(calculate_data)):
        if calculate_data[i][0][0] == "naive": # getting first model type
            model_name = f"Naive Model {naive_model_count}"
            naive_model_count += 1
        elif calculate_data[i][0][0] == "sophisticated":
            model_name = f"Sophisticated Model {sophisticated_model_count}"
            sophisticated_model_count += 1
        results[model_name] = [] # add a new model to the dictionary of results
        model_configuration[model_name] = calculate_data[i][-1] # add a new model to the model configurations
        
        opening_population.append([])
        added_population.append([])
        final_population.append([])

        last_population = 0
        for calculation in calculate_data[i]:
            if last_population == 0:
                last_population = calculation[1]
            model_result = calculate_population_size(*calculation[:5])
            results[model_name].append(model_result) # add the result to the dictionary of results

            opening_population[i].append(round(last_population, 2))
            added_population[i].append(round(model_result - last_population, 2))
            final_population[i].append(round(model_result, 2))

            last_population = model_result
    
    return results, opening_population, added_population, final_population, model_configuration

def compile_data(models_data: list[list[str|int|TimeAmount]], projection_time:TimeAmount|None, projected_time_unit:str, target_population:int|None, condition:str, output_as:str):
    calculation_data:list[list[list[str, int, TimeAmount, TimeAmount]]] = []
    time_needed = None
    if condition == "population":
        time_needed = TimeAmount(1, projected_time_unit) # IMPORTANT Calculate the projection time needed to exceed the target population
        target_population # use this

    if output_as == "final":
        for i in range(len(models_data)):
            calculation_data.append([]) # add a new model to the list
            if condition == "projected": # if not 0 or None
                calculation_data[i].append(models_data[i] + [projection_time]) # add a calculation for that model to the list
            elif condition == "population":
                calculation_data[i].append(models_data[i] + [time_needed])
    
    if output_as == "list" or output_as == "columns":
        for i in range(len(models_data)):
            projection_time_count = 0
            calculation_data.append([]) # add a new model to the list
            if condition == "projected":
                for _ in range(int(projection_time.get_quantity())):
                    projection_time_count += 1
                    calculation_data[i].append(models_data[i] + [TimeAmount(projection_time_count, projection_time.get_unit())]) # add a calculation to the new model
            elif condition == "population":
                for _ in range(time_needed.get_quantity()):
                    projection_time_count += 1
                    calculation_data[i].append(models_data[i] + [TimeAmount(projection_time_count, time_needed.get_unit())])
    
    return calculation_data, time_needed

def print_results(results:dict[str, list], opening_population:list[list], added_population:list[list], final_population:list[list], model_configuration:dict[str, list[int|TimeAmount]], time_needed:TimeAmount, output_as:str, condition:str):
    print_title("Results")
    if output_as == "columns":
        for i in range(len(results.keys())):
            time_amount_of_condition = model_configuration[list(results.keys())[i]][-1]
            print_table(
                data=[[n for n in range(len(opening_population[i]) + 1)], ([1000] + opening_population[i]), (["-"] + added_population[i]), (["-"] + final_population[i])],
                table_length=len(opening_population[i]) + 1,
                table_title=list(results.keys())[i],
                titles=[f"Time (in {time_amount_of_condition.get_unit()}s)", "Opening", "Added", "Final"],
            )
            if condition == "population":
                print(f"Time taken to reach population: {time_needed.get_quantity()} {time_needed.get_unit()}(s)\n")
            elif condition == "projected":
                print(f"Final Population after {time_amount_of_condition.get_quantity()} {time_amount_of_condition.get_unit()}(s): {final_population[i][-1]}\n")
    
    elif output_as == "list":
        for model, result in results.items():
            if condition == "population":
                print(f"Forward Projection for {model}: {result}")
                print(f"Time taken to reach population: {time_needed.get_quantity()} {time_needed.get_unit()}(s)\n")
            elif condition == "projected":
                print(f"Over Time for {model}: {result}")
                print(f"Final Population after {time_amount_of_condition.get_quantity()} {time_amount_of_condition.get_unit()}(s): {result[-1]}\n")
    
    elif output_as == "final":
        for model, result in results.items():
            print(f"{model}: {result[-1]}\n")

def run_inputs(settings:dict[str, str|int|list[str]]):
    models_data = []
    for i in range(settings["naive_models"]):
        print_title(f"Naive Model {i + 1}")
        initial_population = ranged_input(1, None, "Enter the initial population: ", infinite_end=True)
        growth_rate = TimeAmount(*time_amount_input(
            min = 1,
            max = 100,
            prompt = "Enter the growth rate % (7% = 7): ",
        ))
        models_data.append(["naive"] + [initial_population, growth_rate] + [None])
    for i in range(settings["sophisticated_models"]):
        print_title(f"Sophisticated Model {i + 1}")
        initial_population = ranged_input(1, None, "Enter the initial population: ", infinite_end=True)
        growth_rate = TimeAmount(*time_amount_input(
            min = 1,
            max = 100,
            prompt = "Enter the growth rate % (7% = 7): ",
        ))
        fission_frequency = TimeAmount(*time_amount_input(
            min = 1,
            max = None,
            prompt = "Enter the fission frequency: ",
            infinite_end=True,
        ))
        models_data.append(["sophisticated"] + [initial_population, growth_rate, fission_frequency])

    # Get projection time or target population
    target_population = None
    projection_time = None
    condition = None

    if settings["condition"] == "population":
        print_title("Target Population")
        target_population = ranged_input(1, None, "Enter the target population: ", infinite_end=True)
        condition = "population"
    elif settings["condition"] == "varied":
        print_title("Target Population")
        target_population = ranged_input(0, None, f"Enter the target population (Enter 0 for stopping at a projected time): ", infinite_end=True)
        if target_population == 0:
            condition = "projected"
            print_title("Projection Timeframe")
            projection_time = TimeAmount(*time_amount_input(
                min = 1,
                max = None,
                prompt = "Enter the projection time: ",
                infinite_end=True,
            ))
        else: condition = "population"
    elif settings["condition"] == "projected":
        print_title("Projection Timeframe")
        projection_time = TimeAmount(*time_amount_input(
            min = 1,
            max = None,
            prompt = "Enter the projection time: ",
            infinite_end=True,
        ))
        condition = "projected"
    
    # special conditions
    if condition == "population":
        if settings["naive_models"] > 0:
            projection_time_unit = input("Enter a projected time unit for naive models:")
        else:
            projection_time_unit = fission_frequency.get_unit()
    else:
        projection_time_unit = None
    
    return models_data, projection_time, target_population, condition, projection_time_unit

def run_module(module_number: int):
    # run the module based on the module number and settings
    if module_number == 0:
        settings = input_custom_settings()
    else:
        settings = SIMULATION_SETTINGS[module_number - 1]
    print_header(f"Simulation {module_number}: {settings['name']}")
    
    models_data, projection_time, target_population, condition, projection_time_unit = run_inputs(settings)

    # SUMMARY
    summary(models_data, projection_time, target_population, condition)
    
    # CALCULATIONS
    calculation_data, time_needed = compile_data(models_data, projection_time, projection_time_unit, target_population, condition, settings["output"])
    results, opening_population, added_population, final_population, model_configuration = calculate_models(calculation_data)

    # PRINT RESULTS
    print_results(results, opening_population, added_population, final_population, model_configuration, time_needed, settings["output"], condition)

if __name__ == "__main__":
    print("-------------------------------------------------------------------")
    cprint("Population Modelling Bacteria Simulator", attrs=["bold", "underline"])
    cprint("By Sean Chan", attrs=["bold"])
    cprint("Disclaimer: This was made for a school project. Do not take seriously.")
    print("-------------------------------------------------------------------")
    command = None
    while True:
        command:str = listed_input(
            choices = {
                "1": "Compare a naive and sophisticated model", 
                "2": "Time for a sophisticated model to reach the target population", 
                "3": "Compare two sophisticated population models", 
                "4": "Generate detailed projections formatted as columns", 
                "5": "Model increases in fission-event frequency (Unfinished)",
                "0": "Custom Simulation Settings (Sandbox)",
                "p": "Run Presets for Simulations",
                "h": "Help"
            },
            prompt = "Main Menu",
            return_key=True,
        )
        if command.isnumeric():
            run_module(int(command))
        if command == "p":
            print_title("Presets")
            preset = listed_input(
                choices = {
                    "1": "Graph the comparsion of a naive and sophisticated model", 
                    "2": "Graph the comparison of two sophisticated models",
                    "3": "Compare two naive models", 
                    "4": "Graph the population growth of a naive model",
                    "5": "Graph the population growth of a sophisticated model",
                    "b": "Back"
                },
                prompt = "Select a preset:",
                return_key=True,
            )
            if preset == "b":
                continue
            run_module(int(preset) + 5)
        elif command == "h":
            print_title("Help")
            print("""This is a population modelling simulator for bacteria. \nIt simulates the growth of bacteria using naive (linear) and sophisticated (exponential) models.
The naive model is a linear model that calculates the population size based on the growth rate and the projection time.
The sophisticated model is an exponential model that calculates the population size based on: 
        growth rate, fission frequency, and projection time.

This simulator allows you to compare the two models and see how they differ in many ways.
You can input different values for the initial population, growth rate, fission frequency, and projection time.
You can also input a target population and see how long it takes for the sophisticated model to reach that population.

This is a school project and should not be taken seriously.
""")
