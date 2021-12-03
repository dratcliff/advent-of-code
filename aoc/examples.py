import networkx as nx

nodes = [0, 1, 2, 3]
edges = [(0, 1), (1, 0), (1, 0), (2, 1), (3, 1), (1, 4), (3, 5)]
print("edge_dfs", list(nx.edge_dfs(nx.Graph(edges), nodes)))

print("dfs_preorder_nodes", list(nx.dfs_preorder_nodes(nx.Graph(edges), source=0)))

print("bfs_edges", list(nx.bfs_edges(nx.Graph(edges), source=0)))

print("path_graph", list(nx.path_graph(5).edges()))

bin_tree = nx.binomial_tree(5)

print("binomial_tree", list(bin_tree.edges()))

print("shortest path bin tree", nx.shortest_path(bin_tree, source=0, target=31))