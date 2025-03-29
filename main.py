def convert_time(fr:str, fr_amount:int, to:str):
    seconds = {"d": 86400, "hd": 86400/2, "qd": 86400/4, "h": 3600, "m": 60, "s": 1}
    return (seconds[fr.lower()] / seconds[to.lower()]) * fr_amount

def pop_size(initial_population:int, growth_rate:float, gr_time_unit:str, projection_time:int, pt_unit:str, fission_rate:float = -1) -> float:
    growth_rate = convert_time(gr_time_unit, growth_rate, pt_unit)
    if fission_rate == -1:
        return initial_population * (1 + (growth_rate / 100) * projection_time)
    else:
        pass

if __name__ == "__main__":
    initial_population = input("Enter the initial population: ")
    growth_rate = input("Enter the growth rate (%): ")
    gr_time_unit = input("Enter the growth rate time unit (d, hd, qd, h, m, s): ")

    print("Future projection timeframe:")
    project_time = input("Enter the project time: ")
    pr_time_unit = input("Enter the project time unit (d, hd, qd, h, m, s): ")

    result = pop_size(initial_population, growth_rate, gr_time_unit, project_time, pr_time_unit)
    print(f"Population after {project_time} {pr_time_unit}: {result}")
