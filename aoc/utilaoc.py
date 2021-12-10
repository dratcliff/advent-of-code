def file_to_strings(filename):
    return [x.strip('\n') for x in open(filename).readlines()]

def file_to_integers(filename):
    return [int(x) for x in file_to_strings(filename)]

def line_separated_file_to_2d(filename):
    one_dimension = file_to_strings(filename)
    result = []
    record = []
    for x in one_dimension:
        if x == "":
            result.append(record)
            record = []
            continue
        record.append(x)
    record.append(x)
    result.append(record)
    return result

def file_to_grid(filename):
    grid = {}
    strings = file_to_strings(filename)
    for i in range(0, len(strings)):
        line_as_list = list(strings[i])
        for j in range(0, len(line_as_list)):
            grid[(j, i)] = line_as_list[j]
    return grid

def file_to_integer_grid(filename):
    grid = file_to_grid(filename)
    return {k: int(v) for k, v in grid.items()}

if __name__ == "__main__":
    g = file_to_integer_grid("9/b.txt")
    print(g)