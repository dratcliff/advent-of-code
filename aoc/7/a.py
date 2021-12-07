from utilaoc import file_to_strings

actual = file_to_strings("a.txt")
actual = actual[0]
actual = actual.split(',')
actual = [int(x) for x in actual]


min = 1000000000000

for j in range(0, max(actual)):
    s = 0
    for i in actual:
        k = abs(i-j)
        k *= (k+1)
        k = k // 2
        s += k
    if s < min:
        min = s

print(min)
