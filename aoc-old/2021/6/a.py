from utilaoc import file_to_strings

actual = file_to_strings("a.txt")
actual = actual[0]
actual = actual.split(',')
actual = [int(x) for x in actual]
print(actual)

# Each day, a 0 becomes a 6 and adds a new 8 to the end of the list, 
# while each other number decreases by 1 if it was present at the 
# start of the day.

# def run(input, n):
#     for j in range(0, n):
#         b = len(input)
#         for i in range(0, b):
#             new_fish = []
#             this_fish = input[i]
#             if this_fish == 0:
#                 input[i] = 6
#                 new_fish.append(8)
#             else:
#                 input[i] -= 1
#             input += new_fish
#         print(len(input) - b, input)

# run(actual, 20)
# i don't remember if i attempted to change anything here before realizing it 
# wasn't going to be fast enough and giving up.

from collections import defaultdict

def run(input, n):
    counts = defaultdict(int)
    for i in input:
        counts[i] += 1
    for i in range(0, n):
        next_counts = defaultdict(int)
        for k, v in counts.items():
            if k == 0:
                next_counts[8] += v
                next_counts[6] += v
            else:
                next_counts[k-1] += v
        counts = next_counts
        print(counts)
    print(sum(counts.values()))

run(actual, 256)