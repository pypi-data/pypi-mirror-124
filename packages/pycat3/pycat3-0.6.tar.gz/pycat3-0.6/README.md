## An Example of How To Use the Package
from pycat3 import PyCat3, EdgeTrigger

pc3 = PyCat3()
# OR
pc3 = PyCat3(ip='127.0.0.1.1.1', port=851)

# write a tag
pc3.write_tag('MAIN.nAlive', 9)

# read a tag
print(pc3.read_tag('MAIN.nAlive')

# Tags change notification subscription
# Make lists of the tags to be monitored (Types: Integer, REAL, BOOL)
tags_int = ['MAIN.Int1', 'MAIN.Int2']
tags_real = ['MAIN.Real1']
tags_bool = ['MAIN.Bool1']

# call monitor method from ads instance
pc3.monitor(monitored_int=tags_int, monitored_real=tags_real, monitored_bool=tags_bool)

# Access 'data' dictionary to read a certain tag
print(pc3.data['MAIN.Int1']) 

# Use of Edge Detector

# Create your callback function

def my_callback(oldVal, newVal):
    print(f"Value changed from {oldVal} to {newVal}.") 

# Create EdgeTrigger object wit callback function as argument
detector = EdgeTrigger(my_callback)

# Call the detector with the monitored PLC tag
detector1(pc3.data['MAIN.Int1'])