from utilaoc import file_to_strings

# sample = file_to_strings("sample.txt")
actual = file_to_strings("input.txt")
actual = [x.split(' ') for x in actual]
actual = [(x[0], int(x[1])) for x in actual]
# print(sample)

horizontal = 0
vertical = 0
aim = 0
depth = 0

for x in actual:
    if x[0] == 'forward':
        horizontal += x[1]
        depth += aim*x[1]
    if x[0] == 'down':
        aim += x[1]
    if x[0] == 'up':
        aim -= x[1]

print(horizontal * depth)

# print(actual)