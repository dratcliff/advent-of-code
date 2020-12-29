import networkx as nx

def parse(filename):
    entries = {}
    with open(filename) as f:
        for line in f:
            line = line.strip('\n')
            line = line.replace("bags", "")
            line = line.replace("bag", "")
            entry = line.split("contain")
            k = entry[0].rstrip(' ')
            entries[k] = entry[1]
    return entries

DG = nx.DiGraph()

def build_graph(entries):
    for e in entries:
        contents = entries[e]
        contents = contents.split(",")
        contents = [x.lstrip(' ') for x in contents]
        contents = [x.replace('.', '') for x in contents]
        contents = [x.rstrip(' ') for x in contents]
        
        DG.add_node(e)

        for c in contents:
            DG.add_node(c[2:])
            DG.add_edge(e, c[2:], weight=c[0])

def count_contains_shiny_gold():
    ct = 0
    for g in DG.nodes():
        if g != "shiny gold" and nx.has_path(DG, g, "shiny gold"):
            ct += 1
    return ct

if __name__=="__main__":
    entries = parse("Day7.txt")
    build_graph(entries)
    print(count_contains_shiny_gold())
    for edge in nx.bfs_tree(DG, "shiny gold").edges():
        print(DG.get_edge_data(edge[0], edge[1]))
