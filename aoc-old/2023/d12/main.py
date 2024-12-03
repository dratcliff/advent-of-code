xs = [x.strip('\n') for x in open('input.txt', 'r').readlines()]
xs = [x.split() for x in xs]

M = {}
def count_contiguous_hashes(input_string):
    if input_string in M:
        return M[input_string]
    counts = []
    current_count = 0
    rest = None
    for j in range(len(input_string)):
        char = input_string[j]
        if char == '?':
            M[input_string] = (tuple(counts), rest)
            return (tuple(counts), rest)
        if char == '#':
            current_count += 1
        else:
            if current_count > 0:
                counts.append(current_count)
                current_count = 0
                rest = input_string[j+1:]
    if current_count > 0:
        rest = None
        counts.append(current_count)

    M[input_string] = (tuple(counts), rest)
    return (tuple(counts), rest)


N = {}
def expand(s, p):
    t, rest = count_contiguous_hashes(s)
    if (t, rest) in N:
        return N[(t,rest)]
    if "?" not in s:
        if t == p:
            N[(t,rest)] = 1
            return 1
        else:
            return 0
    for i, v in enumerate(t):
        if i < len(p) and v != p[i]:
            N[(t,rest)] = 0
            return 0

    c = 0
    for i in ('.', '#'):
        index = s.find("?")
        nxt = s[:index] + i + s[index + 1:]
        total = sum(p)
        hashes = nxt.count("#")
        if hashes > total or (hashes + nxt.count("?") < total):
            continue
        c += expand(nxt, p)
    if len(t) > 0:
        N[(t,rest)] = c
    return c

ct = 0
for x in xs:
    y = expand(x[0], eval(x[1]))
    N = {}
    M = {}
    ct += y
print(ct)

ct = 0
for x in xs:
    x0 = "?".join([x[0][:] for _ in range(5)])
    y = expand(x0, eval(x[1])*5)
    N = {}
    M = {}
    ct += y
print(ct)
