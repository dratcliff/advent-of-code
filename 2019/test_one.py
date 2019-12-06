def getLines(filename, to_int=True):
    my_list = []

    with open(filename) as fp:
        line = fp.readline()
        while line:
            entry = line
            if to_int:
                entry = int(entry)
            else: 
                my_list.append(entry.rstrip('\n'))
            line = fp.readline()
    return my_list

def calculate(my_list):
    sum = 0
    for l in my_list:
        sum = sum + int(l/3) - 2
    return sum

def test_calculate():
    lines = getLines("1.txt")
    answer = calculate(lines)
    assert answer == 3406527

def calculate_part_two(my_list):
    sum = 0
    for l in my_list:
        fuel = int(l/3) - 2
        while fuel >= 0:
            sum = sum + fuel
            fuel = int(fuel/3) - 2
    return sum

def test_calculate_part_two():
    lines = getLines("1.txt")
    answer = calculate_part_two(lines)
    assert answer == 5106932
