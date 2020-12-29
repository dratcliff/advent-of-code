import numpy as np

operators = set(["AND", "OR", "LSHIFT", "RSHIFT", "NOT"])

class Instruction:
    def __init__(self, txt):
        s = txt.split(" -> ")
        self.left = s[0]
        self.right = s[1]

def parse(filename):
    entries = []
    with open(filename) as f:
        for line in f:
            entries.append(Instruction(line.strip('\n')))
    return entries

def run(entries, circuit):
    failed = []
    for e in entries:
        try:
            if "AND" in e.left:
                s = e.left.split(" ")
                left = s[0]
                try:
                    left = int(left)
                except:
                    left = circuit[left]
                right = s[2]
                circuit[e.right] = left & circuit[right]
            elif "OR" in e.left:
                s = e.left.split(" ")
                left = s[0]
                right = s[2]
                circuit[e.right] = circuit[left] | circuit[right]
            elif "LSHIFT" in e.left:
                s = e.left.split(" ")
                left = s[0]
                right = s[2]
                circuit[e.right] = circuit[left] << int(right)
            elif "RSHIFT" in e.left:
                s = e.left.split(" ")
                left = s[0]
                right = s[2]
                circuit[e.right] = circuit[left] >> int(right)
            elif "NOT" in e.left:
                s = e.left.split(" ")
                right = s[1]
                circuit[e.right] = ~ circuit[right]
            else:
                try:
                    if e.right not in circuit:
                        i = np.uint16(e.left)
                        circuit[e.right] = i
                except:
                    circuit[e.right] = circuit[e.left]
        except KeyError as ke:
            failed.append(e)
    return (failed, circuit)

def day_seven():
    entries = parse("Day7sample.txt")
    circuit = run(entries, {})[1]
    assert circuit['d'] == 72
    entries = parse("Day7.txt")
    circuit = {}
    while len(entries) > 0:
        result = run(entries, circuit)
        entries = result[0]
        circuit = result[1]
    assert 16076 == circuit['a']

    # part two
    circuit = {}
    circuit['b'] = 16076
    entries = parse("Day7.txt")
    while len(entries) > 0:
        result = run(entries, circuit)
        entries = result[0]
        circuit = result[1]
    
    assert 2797 == result[1]['a']



if __name__=="__main__":
    day_seven()