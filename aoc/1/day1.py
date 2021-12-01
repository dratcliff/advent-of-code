import utilaoc

# sample = utilaoc.file_to_strings("day1sample.txt")
actual = utilaoc.file_to_strings("day1.txt")
# print(sample)
# print(actual)

actual = [int(x) for x in actual]

s = 0

for i in range(0, len(actual)-3):
    if actual[i+1]+actual[i+2]+actual[i+3] > actual[i]+actual[i+1]+actual[i+2]:
        s += 1

print(s)