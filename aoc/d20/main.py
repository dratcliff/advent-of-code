from collections import deque


def get_data(filename: str):
    with open(filename, 'r') as f:
        return f.read()


lines = get_data('input.txt')
lines = lines.strip().split('\n')
lines = [int(x) for x in lines]
lines = list(enumerate(lines))


def mix(lines):
    for i in range(0, len(lines)):
        val = pos = None
        val = [x for x in lines if x[0] == i]
        for j in range(0, len(lines)):
            val, pos = lines[j], lines[j][0]
            if pos == i:
                break

        lines.remove(val)
        next_pos = (j + val[1]) % len(lines)
        lines.insert(next_pos, val)

    return lines


def grove_numbers(lines):
    x = [x for x in lines if x[1] == 0][0]
    idx = lines.index(x)
    D = deque(lines)
    D.rotate(-idx)
    D = list(D)
    return [D[i % len(D)][1] for i in (1000, 2000, 3000)]


def p1(lines):
    lines = mix(lines)
    g = grove_numbers(lines)
    return sum(g)


def p2(lines):
    for i in range(0, 10):
        lines = mix(lines)
    g = grove_numbers(lines)
    return sum(g)


p2_lines = [(x[0], x[1]*811589153) for x in lines]

print(p1(lines))
print(p2(p2_lines))

"""
pypy is much faster here:

$ time python main.py
10707
2488332343098

real    0m13.526s
user    0m0.000s
sys     0m0.000s

$ time pypy main.py
10707
2488332343098

real    0m0.539s
user    0m0.000s
sys     0m0.000s
"""