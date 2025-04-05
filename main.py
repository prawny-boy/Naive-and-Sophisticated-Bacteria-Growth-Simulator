from print_functions import *

SECONDS_IN_UNIT = {"day": 86400, "half-day": 86400 / 2, "quarter-day": 86400 / 4, "hour": 3600, "minute": 60, "seconds": 1}
MODULE_SETTINGS = [
    {
        "name": "Compare a naive and sophisticated model",
        "output": "final",
        "condition": "projected",
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
        "output": "final",
        "condition": "projected",
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
        "output": "final",
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
def calculate_population_size(model_type: str, initial_population: float, growth_rate: TimeAmount, fission_frequency: TimeAmount, projection_time: TimeAmount) -> float:
    initial_population = float(initial_population)
    projection_time.convert(growth_rate.get_unit())
    growth_rate.quantity /= 100

    if model_type == "naive":
        return initial_population + (growth_rate.get_quantity() * initial_population * projection_time.get_quantity())

    if model_type == "sophisticated":
        fission_frequency.convert(growth_rate.get_unit())
        rate_over_fission = growth_rate.get_quantity() * fission_frequency.get_quantity()
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
    return {
        "name": "Custom Settings",
        "output": output,
        "condition": condition,
        "naive_models": naive_models,
        "sophisticated_models": sophisticated_models,
    }

def summary(models_data, projection_time:TimeAmount, target_population:TimeAmount):
    # write a summary of what the user inputted
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

        if projection_time != None:
            print(f"Projected Timeframe: {projection_time.get_quantity()} {projection_time.get_unit()}(s)")
        if target_population != None:
            print(f"Target Population: {target_population}")

def calculate_models(calculate_data:list[list[list]]):
    results:dict[str, list] = {}
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
        
        opening_population.append([])
        added_population.append([])
        final_population.append([])

        for calculation in calculate_data[i]:
            initial_population = calculation[1]
            model_result = calculate_population_size(*calculation[:5])
            results[model_name].append(model_result) # add the result to the dictionary of results

            opening_population[i].append(initial_population)
            added_population[i].append(model_result - initial_population)
            final_population[i].append(model_result)
    
    return results, opening_population, added_population, final_population

def compile_data(models_data: list[list[str, int, TimeAmount, TimeAmount]], projection_time:TimeAmount|None, target_population:int|None, output_as:str):
    # 2 ways, stop after a target population or stop after a projected time
    # the last way is just to print out the final one
    calculation_data:list[list[list[str, int, TimeAmount, TimeAmount]]] = []
    time_needed = None
    if target_population:
        time_needed = 1 # IMPORTANT Calculate the projection time needed to exceed the target population

    if output_as == "final":
        for i in range(len(models_data)):
            calculation_data.append([]) # add a new model to the list
            if projection_time: # if not 0 or None
                calculation_data[i].append(models_data[i] + [projection_time]) # add a calculation for that model to the list
            elif target_population:
                calculation_data[i].append(models_data[i] + [time_needed]) 
    
    if output_as == "list" or output_as == "columns":
        for i in range(len(models_data)):
            projection_time_count = 0
            calculation_data.append([]) # add a new model to the list
            if projection_time:
                for _ in range(int(projection_time.get_quantity())):
                    projection_time_count += 1
                    calculation_data[i].append(models_data[i] + [projection_time_count]) # add a calculation to the new model
            elif target_population:
                for _ in range(time_needed):
                    projection_time_count += 1
                    calculation_data[i].append(models_data[i] + [projection_time_count])
    
    return calculation_data, time_needed

def print_results(results:dict[str, list], opening_population:list[list], added_population:list[list], final_population:list[list], time_needed:TimeAmount, output_as:str, condition:str):
    print_title("Results")
    if output_as == "columns":
        # format the output as columns
        columns = zip(opening_population, added_population, final_population)
        for column in columns:
            print(column)
    elif output_as == "list":
        print_list = []
        for model, result in results.items(): 
            print_list.append(result)
        if condition == "population":
            print(f"Forward Projection: {print_list}")
            print(f"\nTime taken to reach population: {time_needed.get_quantity()} {time_needed.get_unit()}")
        else:
            print(f"Models (In order of input): {print_list}")
    elif output_as == "final":
        # print the results based on the output type
        for model, result in results.items():
            print(f"{model}: {result}")

def run_inputs(settings:dict[str, str|int|list[str]]):
    # GET USER INPUT
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

    if settings["condition"] == "population":
        print_title("Target Population")
        target_population = ranged_input(1, None, "Enter the target population: ", infinite_end=True)
    elif settings["condition"] == "varied":
        print_title("Target Population")
        target_population = ranged_input(0, None, f"Enter the target population (Enter 0 for stopping at a projected time): ", infinite_end=True)
        if target_population == 0:
            print_title("Projection Timeframe")
            projection_time = TimeAmount(*time_amount_input(
                min = 1,
                max = None,
                prompt = "Enter the projection time: ",
                infinite_end=True,
            ))
    elif settings["condition"] == "projected":
        print_title("Projection Timeframe")
        projection_time = TimeAmount(*time_amount_input(
            min = 1,
            max = None,
            prompt = "Enter the projection time: ",
            infinite_end=True,
        ))
    
    return models_data, projection_time, target_population

def run_module(module_number: int):
    # run the module based on the module number and settings
    """
    (1) Compare a naive and sophisticated model
    (2) Time for a sophisticated model to reach the target population
    (3) Compare two sophisticated population models
    (4) Generate detailed projections formatted as columns
    (5) Model increases in fission-event frequency
    """
    print_header(f"Module {module_number}: {settings['name']}")
    if module_number == 0:
        settings = input_custom_settings()
        print(f"Settings selected: {settings}")
    else:
        settings = MODULE_SETTINGS[module_number - 1]
    
    models_data, projection_time, target_population = run_inputs(settings)

    # summarise data inputted
    summary(models_data, projection_time, target_population)
    
    # CALCULATIONS
    calculation_data, time_needed = compile_data(models_data, projection_time, target_population, settings["output"])
    results, opening_population, added_population, final_population = calculate_models(calculation_data)

    # PRINT RESULTS
    print_results(results, opening_population, added_population, final_population, time_needed, settings["output"], settings["condition"])

if __name__ == "__main__":
    run_module(0)