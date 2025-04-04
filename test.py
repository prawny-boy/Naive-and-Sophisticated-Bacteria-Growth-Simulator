a="1"
int(a)
print(type(a))

gr_rate = ["1", "3"]
gr_rate, gr_tu = gr_rate
print(gr_rate, gr_tu)
class TimeAmount:
    def __init__(self, quantity:float, unit:str):
        self.quantity = quantity
        self.unit = unit
    
    def convert(self, to_unit: str):
        self.unit = "10000"
    
    def get_quantity(self):
        return self.quantity
    
    def get_unit(self):
        return self.unit
    
growth_rate = TimeAmount(1, "1")
projection_time = TimeAmount(1, "1")
growth_rate, projection_time.convert("1")
print(growth_rate.get_unit())
print(growth_rate.get_quantity)

q = 100
q /= 100
print(q)

def return_list():
    return [1, 2, 3]

a = return_list()
print(type(a))

projection_time = None
if projection_time:
    print("o")

def test (a, b, c):
    print(a, b, c)

l = [12, 12, 14]
test(*l)