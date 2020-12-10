import networkx as nx
from itertools import combinations

G = nx.DiGraph()

def parse(filename):
    entries = []
    with open(filename) as f:
        for line in f:
            line = line.rstrip('\n')
            entries.append(line.split(" "))
    return entries

def day_nine():
    entries = parse("Day9.txt")
    for e in entries:
        G.add_node(e[0])
        G.add_node(e[2])
        G.add_edge(e[0], e[2], weight=int(e[4]))
        G.add_edge(e[2], e[0], weight=int(e[4]))
    
    for n in combinations(G.nodes(), 2):
        print(nx.shortest_path(G, n[0], n[1]), n[0], n[1])

    

    print(s)

if __name__=="__main__":
    day_nine()