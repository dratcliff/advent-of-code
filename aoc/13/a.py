from utilaoc import line_separated_file_to_2d

actual = line_separated_file_to_2d("a.txt")

dots = actual[0]

grid = {}
x_max = 0
y_max = 0

for d in dots:
    d = d.split(",")
    x = int(d[0])
    y = int(d[1])
    grid[(x, y)] = True
    if x > x_max: 
        x_max = x
    if y > y_max:
        y_max = y

splits = []
for x in actual[1]:
    y = x.split()[2].split("=")
    splits.append((y[0], int(y[1])))

for split in splits:
    for k in list(grid.keys()):
        if split[0] == 'x':
            if k[0] > split[1]:
                grid.pop(k)
                grid[(2*split[1] - k[0], k[1])] = True
        if split[0] == 'y':
            if k[1] > split[1]:
                grid.pop(k)
                grid[(k[0], 2*split[1]-k[1])] = True

x_max = 0
y_max = 0
for d in grid:
    if d[0] > x_max: 
        x_max = d[0]
    if d[1] > y_max:
        y_max = d[1]
    
for i in range(0, y_max+1):
    s = ""
    for j in range(0, x_max+1):
        if (j,i) in grid:
            s += "W"
        else:
            s += " "
    print(s)
