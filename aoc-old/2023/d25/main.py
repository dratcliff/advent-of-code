xs = [x.strip('\n') for x in open('input.txt', 'r').readlines()]
xs = [x.split(": ") for x in xs]
xs = [(x[0], x[1].split()) for x in xs]
edges = []
for src, dests in xs:
    for d in dests:
        edges.append((src, d))

import networkx as nx

# chat GPT gave me a networkx implementation
# that iterated through all possible combinations.
# it was super slow and i eveentually found minimum_edge_cut.

def split_graph(G):
    to_remove = nx.minimum_edge_cut(G)
    G.remove_edges_from(to_remove)
    components = list(nx.connected_components(G))
    ans = 1
    for k in components:
        ans *= len(k)
    print(ans)

G = nx.Graph()
G.add_edges_from(edges)
split_graph(G)