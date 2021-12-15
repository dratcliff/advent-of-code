from utilaoc import file_to_integer_grid
import networkx

actual = file_to_integer_grid("a.txt")

width = 0
height = 0

# figure out height/width since i'm using tuples for keys
for x in actual:
    if x[0] > width:
        width = x[0]+1
    if x[1] > height:
        height = x[1]+1

# this could be more efficient, probably didn't need to build twice like this
# but at 1am, you go with what you can understand
for w in range(0, width):
    for h in range(0, height):
        for i in range(1, 5):
            next_p = (height*i + w, h) # use height as multiplier since i only adjust width later
            last_p = (height*(i-1) + w, h)
            next_val = actual[last_p] + 1
            if next_val > 9:
                next_val = 1
            actual[next_p] = next_val

width = width * 5

for h in range(0, height):
    for w in range(0, width):
        for i in range(1, 5):
            next_p = (w, height*i+ h)
            last_p = (w, height*(i-1) + h)
            next_val = actual[last_p] + 1
            if next_val > 9:
                next_val = 1
            actual[next_p] = next_val


nodes = []
edges = []
maxp = (-1, -1)
G = networkx.DiGraph()
for x, v in actual.items():
    if x[0] >= maxp[0] and x[1] >= maxp[1]:
        maxp = x
    G.add_node(x)
    # took too long to realize in part 1 that you could also move left/up if necessary
    if (x[0], x[1]+1) in actual:
        G.add_edge(x, (x[0], x[1]+1), weight=actual[(x[0], x[1]+1)])
    if (x[0]+1, x[1]) in actual:
        G.add_edge(x, (x[0]+1, x[1]), weight=actual[(x[0]+1, x[1])])
    if (x[0]-1, x[1]) in actual:
        G.add_edge(x, (x[0]-1, x[1]), weight=actual[(x[0]-1, x[1])])
    if (x[0], x[1]-1) in actual:
        G.add_edge(x, (x[0], x[1]-1), weight=actual[(x[0], x[1]-1)])

s = 0
# no clue if this is the best algo for shortest path in weighted graph, but it works
for x in networkx.bellman_ford_path(G, (0, 0), maxp):
    s += actual[x]
s -= actual[(0,0)] # i always count start at least once, so remove it at least once
print(s) # 11 seconds on modern hardware == x seconds on old hardware? haha