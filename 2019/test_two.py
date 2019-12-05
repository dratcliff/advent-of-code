def file_line_to_int_array(filename):
    my_list = []
    with open(filename) as fp:
        line = fp.readline()
        while line:
            entries = str.split(line, ',')
            for e in entries:
                my_list.append(int(e))
            line = fp.readline()
    return my_list

def test_file_line_to_int_array():
    my_array = file_line_to_int_array('2.txt')
    assert len(my_array) == 145

def run(input):
    i = 0
    while i < len(input) - 1:
        opcode = input[i]
        if opcode == 99:
            return input
        position1 = input[i+1]
        position2 = input[i+2]
        outpos = input[i+3]
        if opcode == 1:
            input[outpos] = input[position1] + input[position2]
        elif opcode == 2:
            input[outpos] = input[position1] * input[position2]
        i = i + 4
    return input

def test_run():
    assert run([1,0,0,0,99]) == [2,0,0,0,99]
    assert run([2,3,0,3,99]) == [2,3,0,6,99]
    assert run([2,4,4,5,99,0]) == [2,4,4,5,99,9801]
    assert run([1,1,1,4,99,5,6,0,99]) == [30,1,1,4,2,5,6,0,99]

def test_part_one():   
    part_one = file_line_to_int_array('2.txt')
    part_one[1] = 12
    part_one[2] = 2
    assert run(part_one)[0] == 4138658

def part_two():
    out = file_line_to_int_array('2.txt')
    for i in range(0, 100):
        for j in range(0, 100):
            k = list(out)
            k[1] = i
            k[2] = j
            k = run(k)
            if k[0] == 19690720:
                return i*100 + j

def test_part_two():
    assert part_two() == 7264