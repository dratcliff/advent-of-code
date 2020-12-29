from string import ascii_uppercase as uppercase
from test_one import getLines
import networkx as nx


def get_portals(grid):
    portals = {}

    for k, v in grid.items():
        u = (k[0], k[1]-1)
        d = (k[0], k[1]+1)
        f = (k[0]-1, k[1])
        r = (k[0]+1, k[1])

        uu = (u[0], u[1]-1)
        dd = (d[0], d[1]+1)
        ff = (f[0]-1, f[1])
        rr = (r[0]+1, r[1])

        if u in grid and grid[u] in uppercase:
            if uu in grid and grid[uu] == ".":
                key = grid[u]+v
                if key in portals:
                    portals[key].append(uu)
                else:
                    portals[key] = [uu]

        if d in grid and grid[d] in uppercase:
            if dd in grid and grid[dd] == ".":
                key = v + grid[d]
                if key in portals:
                    portals[key].append(dd)
                else:
                    portals[key] = [dd]

        if f in grid and grid[f] in uppercase:
            if ff in grid and grid[ff] == ".":
                key = grid[f] + v
                if key in portals:
                    portals[key].append(ff)
                else:
                    portals[key] = [ff]

        if r in grid and grid[r] in uppercase:
            if rr in grid and grid[rr] == ".":
                key = v + grid[r]
                if key in portals:
                    portals[key].append(rr)
                else:
                    portals[key] = [rr]

    return portals


def graph_stuff(grid, portals):
    G = nx.Graph()
    for k, v in grid.items():
        if v == ".":
            G.add_node(k)
    for k, v in portals.items():
        if len(v) == 2:
            G.add_edge(v[0], v[1])
    for k in G.nodes():
        for j in G.nodes():
            # this was dumb -- adding edges while building nodes from grid (see graph_stuff2)
            # was much more efficient
            if k[0] == j[0]:
                if k[1] == j[1]-1 or k[1] == j[1]+1:
                    G.add_edge(k, j)
            if k[1] == j[1]:
                if k[0] == j[0]-1 or k[0] == j[0]+1:
                    G.add_edge(k, j)

    return G


def graph_stuff2(text):
    G = nx.Graph()
    grid = {(j, i): w for i, v in enumerate(text) for j, w in enumerate(v)}
    portals = get_portals(grid)
    mint, maxt = get_boundaries(grid)
    start = portals['AA'][0]
    end = portals['ZZ'][0]
    G.add_node((start, 0))
    G.add_node((end, 0))
    for i in range(200):
        print(i)
        for k, v in grid.items():
            if v == ".":
                G.add_node((k, i))
                up = ((k[0], k[1]-1), i)
                if G.has_node(up):
                    G.add_edge(up, (k, i))
                down = ((k[0], k[1]+1), i)
                if G.has_node(down):
                    G.add_edge(down, (k, i))
                left = ((k[0]-1, k[1]), i)
                if G.has_node(left):
                    G.add_edge(left, (k, i))
                right = ((k[0]+1, k[1]), i)
                if G.has_node(right):
                    G.add_edge(right, (k, i))
        for k, v in portals.items():
            if len(v) == 2:
                if is_outer(mint, maxt, v[0]) and not is_outer(mint, maxt, v[1]):
                    G.add_node((v[0], i+1))
                    G.add_node((v[1], i))
                    G.add_edge((v[0], i+1), (v[1], i))
                elif is_outer(mint, maxt, v[1]) and not is_outer(mint, maxt, v[0]):
                    G.add_node((v[1], i+1))
                    G.add_node((v[0], i))
                    G.add_edge((v[1], i+1), (v[0], i))
    # for i in range(200):
    #     print(i)
    #     for k in [y for y in G.nodes() if y[1] == i]:
    #         for j in [y for y in G.nodes() if y[1] == i]:
    #             k_level = k[1]
    #             j_level = j[1]
    #             k_coord = k[0]
    #             j_coord = j[0]
    #             if k_level == j_level:
    #                 if k_coord[0] == j_coord[0]:
    #                     if k_coord[1] == j_coord[1]-1 or k_coord[1] == j_coord[1]+1:
    #                         G.add_edge(k, j)
    #                 if k_coord[1] == j_coord[1]:
    #                     if k_coord[0] == j_coord[0]-1 or k_coord[0] == j_coord[0]+1:
    #                         G.add_edge(k, j)
    if nx.has_path(G, (start, 0), (end, 0)):
        return len(nx.shortest_path(G, (start, 0), (end, 0)))-1

    return G


def get_shortest2(text):
    grid = {(j, i): w for i, v in enumerate(text) for j, w in enumerate(v)}
    portals = get_portals(grid)
    portal_points = frozenset([k for j in portals.values() for k in j])

    G = graph_stuff(grid, portals)

    for k in portals:
        for j in portals:
            if k != j:
                start = portals[k][0]
                end = portals[j][0]

                the_path = nx.shortest_path(G, start, end)
                print(k, j, len(the_path)-1)


def sample_one():
    m = """
         A           
         A           
  #######.#########  
  #######.........#  
  #######.#######.#  
  #######.#######.#  
  #######.#######.#  
  #####  B    ###.#  
BC...##  C    ###.#  
  ##.##       ###.#  
  ##...DE  F  ###.#  
  #####    G  ###.#  
  #########.#####.#  
DE..#######...###.#  
  #.#########.###.#  
FG..#########.....#  
  ###########.#####  
             Z       
             Z       """
    text = m.splitlines()[1:]
    print(get_shortest(text))


def sample_two():
    m = """
                   A               
                   A               
  #################.#############  
  #.#...#...................#.#.#  
  #.#.#.###.###.###.#########.#.#  
  #.#.#.......#...#.....#.#.#...#  
  #.#########.###.#####.#.#.###.#  
  #.............#.#.....#.......#  
  ###.###########.###.#####.#.#.#  
  #.....#        A   C    #.#.#.#  
  #######        S   P    #####.#  
  #.#...#                 #......VT
  #.#.#.#                 #.#####  
  #...#.#               YN....#.#  
  #.###.#                 #####.#  
DI....#.#                 #.....#  
  #####.#                 #.###.#  
ZZ......#               QG....#..AS
  ###.###                 #######  
JO..#.#.#                 #.....#  
  #.#.#.#                 ###.#.#  
  #...#..DI             BU....#..LF
  #####.#                 #.#####  
YN......#               VT..#....QG
  #.###.#                 #.###.#  
  #.#...#                 #.....#  
  ###.###    J L     J    #.#.###  
  #.....#    O F     P    #.#...#  
  #.###.#####.#.#####.#####.###.#  
  #...#.#.#...#.....#.....#.#...#  
  #.#####.###.###.#.#.#########.#  
  #...#.#.....#...#.#.#.#.....#.#  
  #.###.#####.###.###.#.#.#######  
  #.#.........#...#.............#  
  #########.###.###.#############  
           B   J   C               
           U   P   P               """
    text = m.splitlines()[1:]
    print(get_shortest(text))


def part_one():
    text = getLines("resources/20.txt", to_int=False)
    print(get_shortest(text))


def is_outer(mint, maxt, p1):
    return p1[0] == mint[0]+2 or p1[0] == maxt[0]-2 or p1[1] == maxt[1]-2 or p1[1] == mint[1]+2


def get_outer(text):
    grid = {(j, i): w for i, v in enumerate(text) for j, w in enumerate(v)}
    mint, maxt = get_boundaries(grid)
    portals = get_portals(grid)
    for p in portals:
        if p not in ("AA", "ZZ"):
            for p1 in portals[p]:
                if is_outer(mint, maxt, p1):
                    grid[p1] = "#"
    return grid


def get_inner(text):
    grid = {(j, i): w for i, v in enumerate(text) for j, w in enumerate(v)}
    portals = get_portals(grid)
    for p in portals:
        if p in ("AA", "ZZ"):
            for p1 in portals[p]:
                grid[p1] = "#"
    return grid


def get_boundaries(grid):
    minx, miny, maxx, maxy = 99, 99, 0, 0
    for k in grid:
        if k[0] < minx:
            minx = k[0]
        if k[0] > maxx:
            maxx = k[0]
        if k[1] < miny:
            miny = k[1]
        if k[1] > maxy:
            maxy = k[1]
    return ((minx, miny), (maxx, maxy))


def part_two():
    text = """
             Z L X W       C                 
             Z P Q B       K                 
  ###########.#.#.#.#######.###############  
  #...#.......#.#.......#.#.......#.#.#...#  
  ###.#.#.#.#.#.#.#.###.#.#.#######.#.#.###  
  #.#...#.#.#...#.#.#...#...#...#.#.......#  
  #.###.#######.###.###.#.###.###.#.#######  
  #...#.......#.#...#...#.............#...#  
  #.#########.#######.#.#######.#######.###  
  #...#.#    F       R I       Z    #.#.#.#  
  #.###.#    D       E C       H    #.#.#.#  
  #.#...#                           #...#.#  
  #.###.#                           #.###.#  
  #.#....OA                       WB..#.#..ZH
  #.###.#                           #.#.#.#  
CJ......#                           #.....#  
  #######                           #######  
  #.#....CK                         #......IC
  #.###.#                           #.###.#  
  #.....#                           #...#.#  
  ###.###                           #.#.#.#  
XF....#.#                         RF..#.#.#  
  #####.#                           #######  
  #......CJ                       NM..#...#  
  ###.#.#                           #.###.#  
RE....#.#                           #......RF
  ###.###        X   X       L      #.#.#.#  
  #.....#        F   Q       P      #.#.#.#  
  ###.###########.###.#######.#########.###  
  #.....#...#.....#.......#...#.....#.#...#  
  #####.#.###.#######.#######.###.###.#.#.#  
  #.......#.......#.#.#.#.#...#...#...#.#.#  
  #####.###.#####.#.#.#.#.###.###.#.###.###  
  #.......#.....#.#...#...............#...#  
  #############.#.#.###.###################  
               A O F   N                     
               A A D   M                     """.splitlines()[1:]

    text = getLines("resources/20.txt", to_int=False)
    print(graph_stuff2(text))
    # print(G.edges())


part_two()
