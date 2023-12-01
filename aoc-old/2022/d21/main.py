def get_data(filename: str):
    with open(filename, 'r') as f:
        return f.read()

class Node:
    def __init__(self, name, left, right, op, val) -> None:
        self.name = name
        self.left = left
        self.right = right
        self.op = op
        self.val = val

    def __repr__(self) -> str:
        return self.name

    def get_val(self):
        if self.val:
            return self.val
        L = nodes[self.left]
        R = nodes[self.right]

        if self.op == "+":
            return L.get_val() + R.get_val()
        if self.op == "-":
            return L.get_val() - R.get_val()
        if self.op == "*":
            return L.get_val() * R.get_val()
        if self.op == "/":
            return L.get_val() // R.get_val()

nodes = {}

lines = get_data('input.txt')
lines = lines.strip().split('\n')
for line in lines:
    line = line.replace(":", "").split()
    if len(line) == 2:
        nodes[line[0]] = Node(line[0], None, None, None, int(line[1]))
    else:
        nodes[line[0]] = Node(line[0], line[1], line[3], line[2], None)

root = nodes['root']
left = nodes[root.left]
right = nodes[root.right]
print("Part one", root.get_val())

a = (68634163976960-15610303684582)//14 # initial diff, looked like it was changing by about 28 every two iterations
a = 3787418592113-27848600000 # lazy/manual binary search
for i in range(a-80000, a+10000):
    nodes['humn'].val = i
    if left.get_val() == right.get_val():
        print("Part two", i) # worst solution ever but it works
        break