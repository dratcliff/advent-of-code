from collections import deque
a = 516
b = 190


def f(pair, limit, fa, fb):
    AQ = deque()
    BQ = deque()
    a = pair[0]
    b = pair[1]
    act = 0
    bct = 0
    while act < limit:
        a *= 16807
        a %= 2147483647
        if fa(a):
            AQ.append(a)
            act += 1

    while bct < limit:
        b *= 48271
        b %= 2147483647
        if fb(b):
            BQ.append(b)
            bct += 1

    s = 0
    while AQ:
        a = AQ.popleft()
        b = BQ.popleft()

        a1 = a % 2**16
        b1 = b % 2**16

        if a1 ^ b1 == 0:
            s += 1

    return s


print(f((516, 190), 40000000, lambda _: True, lambda _: True))
print(f((516, 190), 5000000, lambda x: x % 4 == 0, lambda x: x % 8 == 0))
