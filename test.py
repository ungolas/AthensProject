import time

line_str = "\n" * 30
upper_str = "-" * 100
lower_str = "-" * 100
middle_str = " " * 100

for i in range(0,30):
    print(line_str)
    print(upper_str)
    print(middle_str)
    print(lower_str)
    middle_str = (" " * i) + "*" + middle_str[i+1:]
    time.sleep(0.5)