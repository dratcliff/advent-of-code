def get_data(filename: str):
    with open(filename, 'r') as f:
        return f.read()

lines = get_data('input.txt')
lines = lines.strip().split('\n')
the_sum = 0
for line in lines:
    a = list(reversed(line))
    s = 0
    for i in range(0, len(a)):
        c = 5**i
        if a[i] == "=":
            s -= 2*c
        elif a[i] == "-":
            s -= c
        else:
            s += int(a[i])*c
    the_sum += s

print(the_sum)

s = ""
for i in range(30, -1, -1):
    print(i, the_sum//(5**i), the_sum, 5**i)
    if the_sum//(5**i) > 0:
        c = the_sum//(5**i)
        
        s += str(the_sum//(5**i))
        the_sum = the_sum - c*(5**i)
    else:
        s += "0"
print(s)

# 0000000000012343003334213440410
# once I got here, I just manually converted 4s and 3s to -s and ==s
# and then verified that it matched by putting the SNAFU number
# below in test.txt

# 2=-0=01----22-0-1-10
