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
import matplotlib.pyplot as plt
import numpy as np
def show_graph(x_values:list[list], y_values:list[list], graph_type:str = "line"):
    for i in range(len(x_values)):
        x = np.array(x_values[i])
        y = np.array(y_values[i])
        if graph_type == "line": plt.plot(x, y)
        elif graph_type == "bar": plt.bar(x, y)
    plt.show()
show_graph([[1, 2, 3], [1, 2, 3]], [[1, 2, 3], [1, 2, 3]], "line")

import matplotlib.pyplot as plt

# Data points
x = [1, 2, 3, 4]
y1 = [2, 4, 1, 3]
y2 = [5, 3, 4, 2]

# Create figure to avoid overlap issues
plt.figure(figsize=(8, 5))

# Plot the lines with labels
plt.plot(x, y1, label='Line 1', marker='o', linestyle='-')
plt.plot(x, y2, label='Line 2', marker='s', linestyle='--')

# Label axes and title
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Plot with Line Labels')

# Ensure the legend is properly displayed
plt.legend(loc='best')

# Show the plot
plt.show()

def myfunction(a, b): # this defines a function. a and b are parameters (what you feed to the function to do stuff for you)
    c = a + b
    d = a - b
    return c, d # this returns c and d

c, d = myfunction(1, 2) # this will set c to 3 as 1 + 2 = 3. This will also set d to -1 as 1 - 2 = -1
print(c) # this will print 3
print(d) # this will print -1

def naive_model_calculation(population, blah, stuff):
    return blah # do calculations

blah = naive_model_calculation(1, 2, 3)
