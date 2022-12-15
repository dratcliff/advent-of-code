from utilaoc import line_separated_file_to_2d
from collections import defaultdict

actual = line_separated_file_to_2d("a.txt")
seed = actual[0][0]
patterns = [x.split(' -> ') for x in actual[1]]


def run(n):
    counts = defaultdict(int)
    for s in seed:
        counts[s] += 1

    pairs = defaultdict(int)

    for i in range(0, len(seed)-1):
        pairs[seed[i:i+2]] += 1

    for i in range(0, n):
        last_pairs = pairs.copy()
        for p in list(last_pairs.keys()):
            for pattern in patterns:
                if pattern[0] == p:
                    if last_pairs[p] > 0:
                        counts[pattern[1]] += last_pairs[p]
                        pairs[pattern[0][0] + pattern[1]] += last_pairs[p]
                        pairs[pattern[1] + pattern[0][1]] += last_pairs[p]
                        pairs[p] -= last_pairs[p]
        last_pairs = pairs

    print(max(counts.values()) - min(counts.values()))


run(10)
run(40)
