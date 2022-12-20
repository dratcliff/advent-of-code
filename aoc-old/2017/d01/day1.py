from utilaoc import file_to_strings

input = file_to_strings("day1input.txt")
input = input[0]
s = 0


mid = len(input)//2
front = input[:mid]
back = input[mid:]

print(len(front))
print(len(back))

for i in range(0, len(front)):
    if front[i] == back[i]:
        s += 2*int(front[i])


print(s)