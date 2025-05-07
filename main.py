from print_functions import * # Imports my functions for user error and inputting/printing things
from math import log, ceil, e # Imports neccessary math functions, log and ceil, and the constant e
import matplotlib.pyplot as plt # Imports matplotlib for graphing

SECONDS_IN_UNIT = {"year": 31536000, "half-year": 31536000 / 2, "quarter-year": 31536000 / 4, "month": 2592000, "week": 604800, "day": 86400, "half-day": 86400 / 2, "quarter-day": 86400 / 4, "2-hour": 3600 * 2, "hour": 3600, "minute": 60, "second": 1} # Defines the number of seconds in each unit
UNITS_ABBREVIATION = {"year": "y", "half-year": "hy", "quarter-year": "qy", "month": "m", "week": "w", "day": "d", "half-day": "hd", "quarter-day": "qd", "2-hour": "2h", "hour": "h", "minute": "min", "second": "s"} # Defines some abbreviations for units
SIMULATION_SETTINGS = [ # Settings for all the modules that can be run
    {
        "name": "Compare a naive and sophisticated model", # this is the name of the module
        "output": "final", # this is the output type of the module. Final is final population only
        "condition": "projected", # this is the condition of the module. Projected is by projected time
        "naive_models": 1, # this is the number of naive models to run
        "sophisticated_models": 1, # this is the number of sophisticated models to run
        "forced": {},
    },
    {
        "name": "Time for a sophisticated model to reach the target population",
        "output": "list", # list is list of all the populations over time
        "condition": "population", # population is target population
        "naive_models": 0,
        "sophisticated_models": 1,
        "forced": {},
    },
    {
        "name": "Compare population models",
        "output": "compare", # compare is list of all the populations over time side by side for each model
        "condition": "projected",
        "naive_models": 0,
        "sophisticated_models": 2,
        "forced": {},
    },
    {
        "name": "Generate detailed projections formatted as columns",
        "output": "columns", # columns is the list of all the populations over time as columns (start, added, end)
        "condition": "varied", # varied allows the user to choose between population and projected
        "naive_models": 0,
        "sophisticated_models": 1,
        "forced": {},
    },
    {
        "name": "Model increases in fission-event frequency",
        "output": "final",
        "condition": "projected",
        "naive_models": 0,
        "sophisticated_models": 5,
        "forced": {"initial_population": "same", "growth_rate": [100, "day"], "projection_time": [1, "day"], "fission_frequency": ["quarter-day", "2-hour", "hour", "minute", "second"]}, # forced are variables that are set for all modules no matter what
    }
]

# Settings
rounding_amount = 2 # How many decimal places to round to (this can be changed in settings)
inital_population_limits = [1, 1000000000] # The limits for the initial population
growth_rate_limits = [1, 100] # The limits for the growth rate
fission_frequency_limits = [1, 1000000000] # The limits for the fission frequency
projection_time_limits = [0, 10000000000] # The limits for the projection time
target_population_limits = [0, 1000000000] # The limits for the target population

class TimeAmount: # Class for time amounts, which are a float and a str (unit)
    def __init__(self, quantity:float, unit:str): # Constructor
        self.quantity = quantity # sets quantity
        self.unit = unit # sets unit
    
    def __str__(self): # this runs if the class is converted to a string
        if self.quantity == 1:
            return f"{self.quantity} {self.unit}"
        else:
            return f"{self.quantity} {self.unit}s"
    
    def __round__(self, n): # this runs if the class is rounded
        self.quantity = round(self.quantity, n)
        return self
    
    def convert(self, to_unit: str): # converts the timeamount to the new unit
        converted = (SECONDS_IN_UNIT[self.unit.lower()] / SECONDS_IN_UNIT[to_unit.lower()]) * self.quantity # formula of conversion
        self.quantity = converted # sets quantity
        self.unit = to_unit # sets unit
        return converted
    
    def scale(self, to_unit: str): # scales the timeamount to the new unit
        converted = (SECONDS_IN_UNIT[to_unit.lower()] / SECONDS_IN_UNIT[self.unit.lower()]) * self.quantity # formula of scaling
        self.quantity = converted # sets quantity
        self.unit = to_unit # sets unit
        return converted

    def get_quantity(self): # gets the quantity
        return self.quantity
    
    def get_unit(self): # gets the unit
        return self.unit

# Functions
def calculate_population_size(model_type: str, initial_population: float, growth_rate: TimeAmount, fission_frequency: int, projection_time: TimeAmount) -> float: # Function that calculates the final population based on inputted variables
    initial_population = float(initial_population) # changes the initial population to a float to avoid errors
    rate = TimeAmount(growth_rate.get_quantity(), growth_rate.get_unit()) # Make sure that the outside growth_rate is not modified by setting to new variable
    rate.scale(projection_time.get_unit()) # scales the growth rate to the same unit as the projection time
    rate.quantity /= 100 # divides the growth rate by 100 to make it from a percentage to decimal
    if model_type == "naive": # if the model type is naive
        return initial_population + (rate.get_quantity() * initial_population * projection_time.get_quantity()) # returns the final population A = P + (PRT)
    if model_type == "sophisticated": # if the model type is sophisticated
        fission_frequency = SECONDS_IN_UNIT[projection_time.get_unit()] / SECONDS_IN_UNIT[growth_rate.get_unit()] * fission_frequency # scales the fission frequency to the same unit as the growth rate
        rate_over_fission = rate.get_quantity() / float(fission_frequency) # gets the growth rate over the fission frequency
        total_fission_events = projection_time.get_quantity() * fission_frequency # gets the total number of fission events
        return initial_population * ((1 + rate_over_fission) ** total_fission_events) # returns the final population (1+r/n)^(nt)

def calculate_time_to_reach_target(model_type:str, initial_population: float, growth_rate: TimeAmount, fission_frequency: int, target_population: float) -> TimeAmount|int: # Function that calculates the time needed to reach the target population based on inputted variables
    target_population_ratio = target_population / initial_population # gets the target population ratio
    rate = TimeAmount(growth_rate.get_quantity(), growth_rate.get_unit()) # Make sure that the outside growth_rate is not modified by setting to new variable
    rate.quantity /= 100 # divides the growth rate by 100 to make it from a percentage to decimal
    try: increment = 1 / fission_frequency # gets the frequency increment
    except: increment = 1 # if the fission frequency is None, set the increment to 1 (for naive models)
    if model_type == "naive": # if the model type is naive
        time_needed = ceil((target_population - initial_population) / (initial_population * rate.get_quantity())) # this is to ceiling the time needed by the increment
    elif model_type == "sophisticated": # if the model type is sophisticated
        time_needed = log(target_population_ratio) / (fission_frequency * log(1 + rate.get_quantity() / float(fission_frequency))) # gets the time needed using the formula and logarithms
        time_needed = ceil(time_needed / increment) * increment # this is to ceiling the time needed by the frequency increment
    return TimeAmount(time_needed, rate.get_unit()), increment # returns the time needed

def show_graph(results: dict[str, list], opening_population: list[list], added_population: list[list], final_population: list[list], model_configuration: dict[str, list[int|TimeAmount]], condition: str, output_as: str): # Function that shows the graph based on output type
    if limited_input(prompt="Print Graph?") == "n": return # stop anything from happening if the user doesnt want to print a graph
    if output_as == "columns": # if the output type is columns
        columns = ceil(len(results)**0.5) # gets the number of columns
        rows = ceil(len(results)/columns) # gets the number of rows
        for i in range(len(results)): # for each result
            time_amount_of_condition = model_configuration[list(results.keys())[i]][-1] # time_amount_of_condition is the projection time
            increment = model_configuration[list(results.keys())[i]][-2] # increment is the fission frequency
            plt.subplot(rows, columns, i+1) # creates a subplot
            plt.plot([i*increment for i in range(len(opening_population[i]))], opening_population[i], label="Opening") # plots the opening population
            plt.plot([i*increment for i in range(len(added_population[i]))], added_population[i], label="Added") # plots the added population
            plt.plot([i*increment for i in range(len(final_population[i]))], final_population[i], label="Final") # plots the final population
            plt.title(list(results.keys())[i]) # sets the title
            plt.xlabel(f"Time ({time_amount_of_condition.get_unit()})") # sets the x label
            plt.ylabel("Population Size") # sets the y label

    elif output_as == "list" or output_as == "compare": # line graph
        for model, result in results.items(): # for each result
            increment = model_configuration[model][-2] # increment is the fission frequency
            if condition == "population": # if the condition is population
                plt.plot([i*increment for i in range(len(result))], result, label=model) # plots the population
            elif condition == "projected": # if the condition is projected
                plt.plot([i for i in range(len(result))], result, label=model) # plots the projected population
        plt.title("Population Size Over Time") # sets the title
        plt.xlabel(f"Time ({model_configuration[list(results.keys())[0]][-1].get_unit()})") # sets the x label
        plt.ylabel("Population Size") # sets the y label

    elif output_as == "final": # bar graph
        for model, result in results.items(): # for each result
            plt.bar("".join([model[0][0], model.split()[2]]), result[-1]) # plots the final population
        plt.title("Final Population Size by Model") # sets the title
        plt.xlabel("Models") # sets the x label
        plt.ylabel("Population Size") # sets the y label
    
    plt.legend() # shows the legend
    plt.tight_layout() # tightens the layout
    cprint("Opened Graph. Close the graph to continue...\n", color="grey", attrs=["dark"]) # prints a message to tell the user to close the graph to continue
    plt.show() # shows the graph

def input_custom_settings(): # Function that inputs custom settings
    print_title("Input Custom Settings") # prints a title
    naive_models = ranged_input(0, 10, "Enter the number of naive models: ") # gets the number of naive models
    sophisticated_models = ranged_input(0, 10, "Enter the number of sophisticated models: ") # gets the number of sophisticated models
    output:str = listed_input( # gets the output type
        choices = {"final": "Final Population Size", 
                   "list": "List of Populations over Time", 
                   "columns": "Columns of Populations over Time (start, added, end)",
                   "compare": "Compare Models next to each other"},
        prompt = "Select the output type:",
        return_key=True,
    )
    condition:str = listed_input( # gets the condition
        choices = {"population": "Target Population", 
                   "varied": "Varied Population",   
                   "projected": "Projected Time"},
        prompt = "Select the condition type:",
        return_key=True,
    )
    forced = {}
    selected_forced_setting = ""
    while selected_forced_setting != "done/continue":
        selected_forced_setting = listed_input( # gets the forced setting
            choices = {"i": "Inital Population", 
                       "g": "Growth Rate",
                       "f": "Fission Frequency",
                       "t": "Projection Time",
                       "tp": "Target Population",
                       "d": "Done/Continue"},
            prompt = "Select a variable to force:"
        ).lower()
        if selected_forced_setting == "inital population": 
            forced["initial_population"] = ranged_input(*inital_population_limits, "Enter the initial population value to force: ", infinite_end=True)
        elif selected_forced_setting == "growth rate": 
            forced["growth_rate"] = time_amount_input(*growth_rate_limits, "Enter the growth rate value to force: ", infinite_end=True)
        elif selected_forced_setting == "fission frequency": 
            forced["fission_frequency"] = time_amount_input(
                1, 1, "Enter the fission-event frequency time unit to force (or custom): ",
                special=["custom"],
                avaliable_units=UNITS_ABBREVIATION | {"custom": "c"},
            )
            if "custom" in forced["fission_frequency"]: forced["fission_frequency"] = ranged_input(*fission_frequency_limits, "Enter the number of fission-events per growth rate unit to force: ", infinite_end=True)
            else: forced["fission_frequency"] = forced["fission_frequency"][1]
        elif selected_forced_setting == "projection time": 
            forced["projection_time"] = time_amount_input(*projection_time_limits, "Enter the projection time value to force: ", allow_float=False, infinite_end=True)
        elif selected_forced_setting == "target population": 
            forced["target_population"] = ranged_input(*target_population_limits, "Enter the target population value to force: ", infinite_end=True)

    print_title("Selected Settings")
    print(f"Output: {output.capitalize()}, Condition: {condition.capitalize()}")
    print(f"Naive Models: {naive_models}, Sophisticated Models: {sophisticated_models}")
    print(f"Forced Settings: {forced}")
    return {
        "name": "Custom Settings",
        "output": output,
        "condition": condition,
        "naive_models": naive_models,
        "sophisticated_models": sophisticated_models,
        "forced": forced
    }

def summary(models_data, projection_time:TimeAmount, target_population:TimeAmount, condition:str): # Function that prints a summary
    print_title("Summary") # prints a title
    naive_model_count = 1 # sets the naive model count to 0 for counting up later
    sophisticated_model_count = 1 # sets the sophisticated model count to 0 for counting up later
    model:list[str|int|TimeAmount] 
    for model in models_data: # loops through each model
        model_type = model[0] # gets the model type
        if model_type == "naive": # if the model type is naive
            model_number = naive_model_count 
            naive_model_count += 1 # update new naive model count
        else: # if the model type is sophisticated
            model_number = sophisticated_model_count
            sophisticated_model_count += 1 # update new sophisticated model count
        model_population:int = model[1] # sets variables for printing
        model_growth_rate:int = model[2].get_quantity()
        model_growth_unit:str = model[2].get_unit()
        fission_frequency:TimeAmount = model[3]

        print(f"{model_type.title()} Model {model_number}: I = {model_population}, g = {model_growth_rate}% per {model_growth_unit}", end="") # prints summary

        print(f", Fission Event Frequency: {fission_frequency}") if model_type == "sophisticated" else print("") # prints summary (only sophisticated models have fission frequency)

        if condition == "projected": # prints the timeframe if the condition is projected
            print(f"Projected Timeframe: {projection_time}")
        if condition == "population": # prints the target population if the condition is population
            print(f"Target Population: {target_population}")

def calculate_models(calculate_data:list[list[list]], output_unit:str): # Function that calculates the models
    results:dict[str, list] = {} # creates a dictionary of results
    model_configuration:dict[str, list[int|TimeAmount]] = {} # creates a dictionary of model configurations
    model_result = 0 
    sophisticated_model_count = 1 
    naive_model_count = 1
    opening_population:list[list] = []
    added_population:list[list] = []
    final_population:list[list] = []
    for i in range(len(calculate_data)): # loops through every model
        if calculate_data[i][0][0] == "naive": # getting first model type
            model_name = f"Naive Model {naive_model_count}"
            naive_model_count += 1
        elif calculate_data[i][0][0] == "sophisticated":
            model_name = f"Sophisticated Model {sophisticated_model_count}"
            sophisticated_model_count += 1
        results[model_name] = [] # add a new model to the dictionary of results
        calculate_data[i][-1][-1].convert(output_unit) # changes the time amount of the condition to the output unit
        model_configuration[model_name] = calculate_data[i][-1] # add a new model to the model configurations
        
        opening_population.append([]) # add a new model to the opening pop list
        added_population.append([]) # add a new model to the added pop list
        final_population.append([]) # add a new model to the final pop list

        last_population = 0 
        for calculation in calculate_data[i]: # loops through each calculation
            if last_population == 0:
                last_population = calculation[1]
            model_result = round(calculate_population_size(*calculation[:5]), rounding_amount) # calculate the model result
            results[model_name].append(model_result) # add the result to the dictionary of results

            opening_population[i].append(last_population) # add to opening pop list
            added_population[i].append(round(model_result - last_population, rounding_amount)) # add to added pop list
            final_population[i].append(model_result) # add to final pop list

            last_population = model_result
    
    return (results, opening_population, added_population, final_population, model_configuration) # return everything

def compile_data(models_data: list[list[str|int|TimeAmount]], projection_time:TimeAmount|None, target_population:int|None, condition:str, output_as:str): # Function that compiles the data for calculation
    calculation_data:list[list[list[str|int|TimeAmount]]] = [] # creates a list of calculations

    for i in range(len(models_data)): # loops through every model
        calculation_data.append([]) # add a new model to the list
        projection_time_count = 0
        if models_data[i][0] == "sophisticated": # models_data[i][3] is the fission frequency convert before calculations
            if type(models_data[i][3]) == str: # if the fission frequency is a string
                models_data[i][3] = SECONDS_IN_UNIT[models_data[i][2].get_unit()] / SECONDS_IN_UNIT[models_data[i][3]] # models_data[i][2] is the growth rate, converts fission frequency unit to a number
        if condition == "projected": # if the condition is projected
            if output_as == "final": # if the output is final
                calculation_data[i].append(models_data[i] + [projection_time]) # add a calculation for that model to the list
            elif output_as in ["list", "columns", "compare"]: # if the output is a list
                for _ in range(projection_time.get_quantity() + 1): # loops through every time for each projected time unit
                    calculation_data[i].append(models_data[i] + [TimeAmount(projection_time_count, projection_time.get_unit())]) # add a calculation to the new model
                    projection_time_count += 1 # increment
        elif condition == "population": # if the condition is population
            time_needed:TimeAmount; increment:int
            time_needed, increment = calculate_time_to_reach_target(*models_data[i], target_population) # models_data[i][2] is the growth rate. Calculates the amount of time needed to reach the target population
            if output_as == "final": # if the output is final
                calculation_data[i].append(models_data[i] + [time_needed]) # add a calculation to the list
            elif output_as in ["list", "columns", "compare"]: # if the output is a list
                for _ in range(int(time_needed.get_quantity()/increment) + 1): # loops through every time for each fission event
                    calculation_data[i].append(models_data[i] + [TimeAmount(projection_time_count, time_needed.get_unit())]) # add a calculation to the new model
                    projection_time_count += increment # increment
    return calculation_data # return all the data, ready to be calculated

def print_results(results:dict[str, list], opening_population:list[list], added_population:list[list], final_population:list[list], model_configuration:dict[str, list[int|TimeAmount]], condition:str, output_as:str): # Function that prints the results
    print_title("Results")
    if output_as == "columns": # if the output is columns
        for i in range(len(results)): # loops through every model
            time_amount_of_condition = model_configuration[list(results.keys())[i]][-1] # time_amount_of_condition is the projection time
            increment = model_configuration[list(results.keys())[i]][-2] # increment is the fission frequency
            print_table( # prints a table with the opening, added and final populations
                data=[[n for n in range(len(opening_population[i]))], opening_population[i], added_population[i], final_population[i]],
                table_length=len(opening_population[i]) + 1,
                table_title=list(results.keys())[i],
                titles=[f"Time (in {time_amount_of_condition.get_unit()}s)", "Opening", "Added", "Final"],
            )
            if condition == "population": # if the condition is population
                # format the time needed
                if time_amount_of_condition.get_quantity() - int(time_amount_of_condition.get_quantity()) == 0:
                    time_needed_format = f"{time_amount_of_condition}"
                else:
                    extra_fission_events = round((time_amount_of_condition.get_quantity() - int(time_amount_of_condition.get_quantity())) * increment)
                    time_needed_format = f"{TimeAmount(int(time_amount_of_condition.get_quantity()), time_amount_of_condition.get_unit())} and {extra_fission_events} fission event(s) ({round(time_amount_of_condition, rounding_amount)})"
                print(f"Time taken to reach population: {time_needed_format}\n") # prints the time needed
            elif condition == "projected": # if the condition is projected
                print(f"Final Population after {time_amount_of_condition}: {final_population[i][-1]}\n") # prints the final population
    elif output_as == "list": # if the output is a list
        for i in range(len(results)): # loops through every model
            time_amount_of_condition = model_configuration[list(results.keys())[i]][-1] # time_amount_of_condition is the projection time
            increment = model_configuration[list(results.keys())[i]][-2] # increment is the fission frequency
            model = list(results.keys())[i] # model is the name of the model
            result = results[model] # result is the list of populations
            printing_results_list = ", ".join([str(i) for i in result]) # printing_results_list is the list of populations as a string
            if condition == "population": # if the condition was population
                # format the time needed
                if time_amount_of_condition.get_quantity() - int(time_amount_of_condition.get_quantity()) == 0:
                    time_needed_format = f"{time_amount_of_condition}"
                else:
                    extra_fission_events = round((time_amount_of_condition.get_quantity() - int(time_amount_of_condition.get_quantity())) * increment)
                    time_needed_format = f"{TimeAmount(int(time_amount_of_condition.get_quantity()), time_amount_of_condition.get_unit())} and {extra_fission_events} fission event(s) ({round(time_amount_of_condition, rounding_amount)})"
                print(f"Forward Projection for {model}: {printing_results_list}") # print list of populations
                print(f"Time taken to reach population: {time_needed_format}\n") # print time needed
            elif condition == "projected": # if the conditon was projected
                print(f"Over Time for {model}: {printing_results_list}") # print list of populations
                print(f"Final Population after {time_amount_of_condition}: {result[-1]}\n") # print final population
    elif output_as == "compare": # if the output is compare
        time_amount_of_condition = model_configuration[list(results.keys())[0]][-1] # time_amount_of_condition is the projection time
        table_data = [] # table_data is the data for the table
        table_data.append([i for i in range(int(time_amount_of_condition.get_quantity()) + 1)]) # table_data[0] is the time
        for i in range(len(results)): # loops through every model
            increment = model_configuration[list(results.keys())[i]][-2] # increment is the fission frequency
            if condition == "population": # if the condition was population
                skip = round(increment)
                table_data.append(results[list(results.keys())[i]][::skip]) # adds results to table data but skips ones to shorten list
            elif condition == "projected": # if the condition was projected
                table_data.append(results[list(results.keys())[i]]) # adds results to table data
        print_table( # prints table
            data=table_data,
            table_length=len(table_data[0]) + 1,
            table_title="Comparison",
            titles=[f"Time (in {time_amount_of_condition.get_unit()}s)"] + [model for model in results.keys()],
        )
    elif output_as == "final": # if the output is final
        for model, result in results.items(): # for each result
            print(f"{model}: {result[-1]}\n") # print final population

def run_inputs(settings:dict[str, str|int|list|dict]):
    models_data = [] # models_data is the data for the models
    if len(settings["forced"]) > 0: cprint("Some variables may have been forced...", "grey", attrs=["dark"]) # if some variables have been forced print that some were forced

    for i in range(settings["naive_models"]): # loops through naive models and run inputs
        print_title(f"Naive Model {i + 1}")
        if "initial_population" in settings["forced"].keys(): initial_population = settings["forced"]["initial_population"]
        else: initial_population = ranged_input(*inital_population_limits, "Enter the initial population: ")
        if "growth_rate" in settings["forced"].keys(): growth_rate = TimeAmount(*settings["forced"]["growth_rate"])
        else: growth_rate = TimeAmount(*time_amount_input(*growth_rate_limits, "Enter the growth rate % (7% = 7): ",))
        models_data.append(["naive"] + [initial_population, growth_rate, None])
    
    for i in range(settings["sophisticated_models"]): # loops through sophisticated models and run inputs
        print_title(f"Sophisticated Model {i + 1}")
        if "initial_population" in settings["forced"].keys(): initial_population = settings["forced"]["initial_population"]
        else: initial_population = ranged_input(*inital_population_limits, "Enter the initial population: ")
        if "growth_rate" in settings["forced"].keys(): growth_rate = TimeAmount(*settings["forced"]["growth_rate"])
        else: growth_rate = TimeAmount(*time_amount_input(*growth_rate_limits, "Enter the growth rate % (7% = 7): ",))
        if "fission_frequency" in settings["forced"].keys(): 
            if type(settings["forced"]["fission_frequency"]) == list:
                fission_frequency = settings["forced"]["fission_frequency"][i]
                cprint(f"Fission Frequency set to: {fission_frequency}...", "grey", attrs=["dark"])
            else:
                fission_frequency = settings["forced"]["fission_frequency"]
        else:
            fission_frequency = time_amount_input(
                1, 1, "Enter the fission-event frequency time unit (or custom): ",
                special=["custom"],
                avaliable_units=UNITS_ABBREVIATION | {"custom": "c"},
            )
            if "custom" in fission_frequency: fission_frequency = ranged_input(*fission_frequency_limits, "Enter the number of fission-events per growth rate unit: ")
            else: fission_frequency = fission_frequency[1] # returns as total fission events unit
        models_data.append(["sophisticated"] + [initial_population, growth_rate, fission_frequency])

    if "initial_population" in settings["forced"].keys(): # MODULE 5 ONLY: get inital population for all modules
        if settings["forced"]["initial_population"] == "same":
            print_title("Initial Population")
            initial_population = ranged_input(*inital_population_limits, "Enter the initial population for all modules: ")
            for i in range(len(models_data)):
                models_data[i][1] = initial_population # set initial population for all modules

    # Get projection time or target population
    target_population = None
    projection_time = None
    condition = settings["condition"]
    if condition == "varied":
        print_title("Condition Type")
        condition = listed_input(
            choices = {"population": "Target Population", 
                       "projected": "Projected Time"},
            prompt = "Select the condition type:",
            return_key=True,
        )
    if condition == "population":
        if "target_population" in settings["forced"].keys(): target_population = settings["forced"]["target_population"]
        else: 
            print_title("Target Population")
            target_population = ranged_input(*target_population_limits, "Enter the target population for all models: ", infinite_end=True)
        output_unit = time_amount_input(1, 1, "Enter the output unit of data: ")[1]
    elif condition == "projected":
        if "projection_time" in settings["forced"].keys(): projection_time = TimeAmount(*settings["forced"]["projection_time"])
        else:
            print_title("Projection Timeframe")
            projection_time = TimeAmount(*time_amount_input(
                *projection_time_limits, 
                "Enter the projection timeframe for all models: ",
                allow_float=False,
                infinite_end=True,
            ))
        output_unit = projection_time.get_unit()
    
    return models_data, projection_time, target_population, output_unit, condition # returns everything user entered

def module_5_info(results: dict[str, list[int]], initial_population: int): # Function to print info for module 5
    # Printing Information
    print_title("Population Limit")
    print(f"Theoretical population limit as fission frequency approaches infinity: {round(e*initial_population, rounding_amount)}")
    print(f"This limit is {round(e, rounding_amount)} times the initial population.")
    print_title("Research Summary")
    print("The limit observed here is related to the mathematical constant 'e'. When growth happens continuously (which is approximated by very high fission frequencies), the formula for population growth becomes P(t) = P0 * e^(rt), where r is the continuous growth rate. In this case, r = 1.0 (100% per day), so the limit is the initial population multiplied by e.")
    input(colored("Press enter to continue...", "grey", attrs=["dark"]))
    # Graphing Module 5
    for model, result in results.items():
        plt.bar(["quarter-day", "2-hour", "hour", "minute", "second"][list(results.keys()).index(model)], result[-1])
    plt.title("How Fission Frequency Affects Final Population Size")
    plt.xlabel("Fission Frequencies")
    plt.ylabel("Population Size")
    cprint("Opened Graph. Close the graph to continue...\n", color="grey", attrs=["dark"])
    plt.show()

def run_module(module_number: int): # run the module based on the module number and settings
    if module_number == 0: # for custom settings
        settings = input_custom_settings()
    else: # for preset settings (modules)
        settings = SIMULATION_SETTINGS[module_number - 1]
    
    replay = ""
    while replay != "n": # replay loop
        print_header(f"Simulation {module_number}: {settings['name']}") # prints the current running simulation
        if replay == "y": cprint("Replaying the last module...", "grey", attrs=["dark"]) # if replaying, print replaying
        
        models_data, projection_time, target_population, output_unit, condition = run_inputs(settings) # get user inputs

        # SUMMARY
        summary(models_data, projection_time, target_population, condition) # print summary
        
        # COMPILE DATA FOR CACULATION
        output_as = settings["output"] # set output as to the settings
        calculation_data = compile_data(models_data, projection_time, target_population, condition, output_as) # compile data for calculation

        # CALCULATE & PRINT RESULTS
        calculations = calculate_models(calculation_data, output_unit) # calculate all the data
        print_results(*calculations, condition, output_as) # print results based on output type

        if module_number == 5: # for module 5, print information
            module_5_info(calculations[0], models_data[0][1])
        else:
            show_graph(*calculations, condition, output_as) # show graphs based on output type

        # REPLAY
        replay = listed_input( # ask for replay
            choices = {"y": "Replay", "n": "Exit to Main Menu"},
            prompt = "Replay Last Module?",
            return_key=True,
        )

if __name__ == "__main__": # main code that runs everything
    print("-------------------------------------------------------------------") # print title and stuff
    cprint("Population Modelling Bacteria Simulator", attrs=["bold", "underline"])
    cprint("By Sean Chan", attrs=["bold"])
    cprint("Disclaimer: This was made for a school project. Do not take seriously.")
    print("-------------------------------------------------------------------")
    command = None
    while True: # game loop
        command:str = listed_input( # asks for a command
            choices = {
                "1": "Compare a naive and sophisticated model", 
                "2": "Time for a sophisticated model to reach the target population", 
                "3": "Compare two sophisticated population models", 
                "4": "Generate detailed projections formatted as columns", 
                "5": "Model increases in fission-event frequency",
                "0": "Custom Simulation Settings (Sandbox)",
                "s": "Settings"
            },
            prompt = "Main Menu",
            return_key=True,
        )
        if command.isnumeric(): # if command is a number
            run_module(int(command)) # run the module
        elif command == "s": # if the settings were chosen
            change_setting = listed_input( # ask for the setting to change
                choices = {
                    "r": "Number of decimals for rounding",
                    "b": "Back"
                },
                prompt = "Select a setting to change:",
                return_key=True,
            )
            if change_setting == "b": # if the user goes back
                continue # restart loop
            elif change_setting == "r": # if the user wants to change the rounding amount
                rounding_amount = ranged_input( # sets the rounding amount
                    start = 0,
                    end = 12,
                    prompt = f"Enter the number of decimals for rounding: (Current: {rounding_amount}) ",
                )
