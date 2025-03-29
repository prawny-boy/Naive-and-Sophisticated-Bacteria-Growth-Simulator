def conv_time(fr:str, fr_amt:int, to:str):
    sec = {"d": 86400, "hd": 86400/2, "qd": 86400/4, "h": 3600, "m": 60, "s": 1}
    return (sec[fr.lower()] / sec[to.lower()]) * fr_amt
