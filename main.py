def conv_time(fr:str, fr_amt:int, to:str):
    sec = {"d": 86400, "hd": 86400/2, "qd": 86400/4, "h": 3600, "m": 60, "s": 1}
    return (sec[fr.lower()] / sec[to.lower()]) * fr_amt

def pop_sz(init_pop:float, gr_rate:list[float, str], proj_time:list[float, str], fiss_rate:list[float, str] = -1):
    gr_rate, gr_tu = gr_rate
    proj_time, pt_tu = proj_time
    gr_rate = conv_time(gr_tu, gr_rate, pt_tu)
    if fiss_rate == -1:
        return round(float(init_pop) * (1 + (gr_rate / 100) * proj_time))
    else:
        pass

def inp_tf(prompt:str):
    while True:
        try:
            inp = input(prompt).split()
            a = inp[0]
            u = inp[1]
            if u not in ["d", "hd", "qd", "h", "m", "s"]:
                print("Use correct unit. (d, hd, qd, h, m, s)")
                continue
            a = float(a)
            return [a, u]
        except IndexError:
            print("Enter in format 'number<space>unit'.")
        except ValueError:
            print("First value must be a number.")


if __name__ == "__main__":
    init_pop = input("Enter the initial population: ")
    gr_rate = inp_tf("Enter the growth rate (%) and its time unit (d, hd, qd, h, m, s): ")

    print("Future projection timeframe:")
    proj_time = inp_tf("Enter the project time and its time unit (d, hd, qd, h, m, s): ")

    result = pop_sz(init_pop, gr_rate, proj_time)
    print(f"Population after {proj_time[0]} {proj_time[1]}: {result}")
