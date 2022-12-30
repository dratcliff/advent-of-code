def f(a):
    a = list(a)
    b = reversed(a)
    b = ["1" if x == "0" else "0" for x in b]
    return ''.join(a + ["0"] + b)

def checksum(a):
    r = []
    for i in range(0, len(a)-1, 2):
        if a[i]==a[i+1]:
            r.append("1")
        else:
            r.append("0")
    if len(r) % 2 == 0:
        return checksum("".join(r))
    return "".join(r)



for x in [272, 35651584]:
    s = "01000100010010111"
    while len(s) < x:
        s = f(s)

    s = s[:x]
    print(checksum(s))