"""

This is terrible code, but I didn't want to clean it up because I thought
it would be a good reminder to myself if I look at this in the future.

For part 1, I didn't want to figure out the particulars of using a queue
to iterate through all the possibilities, so I hacked together some networkx
stuff that gave the right answer by adding an extra mapping (lol) to get around
the restriction of only visiting a node once. So for example, if I had something like

start -> A
A -> c

I replaced it with

start -> A
start -> Ac
Ac -> c
c -> A

That way when I used nx.all_simple_paths, I would get things with

start -> A -> ...
start -> Ac -> c -> A -> ...

and in this way, I could visit each uppercase node as many times as I wanted, but I would only
visit each lowercase node at most once. This was ridiculous, and I didn't think it would work for part two,
and it didn't. But I tried.

I tried to do something like Ac -> c1 and Ac -> c2 but I couldn't figure out a way to make it work, and
maybe it can't, because what I originally did really just removed the circular references while preserving
the count (I think) but to do part two you really _need_ the circular references (also I think).

So everything that's not commented out is only for part two, I get the answer (lol) by 
python a.py | grep end | wc -l.

I thought the part where I checked to see if there was already a lowercase node on the path twice
before adding it back to the queue should work, but it only almost works. For some reason, it's
adding every lowercase node to the queue up to twice, which is fine, but not what we want.

So I (lol) added some code at the beginning to only print lines that actually don't have more than
one lowercase node that appears twice, and then when I grep end | wc -l I get the right answer.

I should really clean this up at some point, but if I ever do (I won't) I'll put it in a different file or something.

"""


from utilaoc import file_to_strings
import networkx as nx
from collections import deque

actual = file_to_strings("a.txt")
actual = [x.split("-") for x in actual]
# print(actual)

from collections import defaultdict
nodes = defaultdict(set)

for a in actual:
    nodes[a[0]].add(a[1])
    nodes[a[1]].add(a[0])


nodes.pop('end')

for node in nodes:
    if 'start' in nodes[node]:
        nodes[node].remove('start')

# print(nodes)

to_do = deque()
to_do.append(('start', set(), []))
while to_do:
    n, visited, path = to_do.popleft()
    twos = 0
    for x in set(path):
        if x != 'start' and x != 'end' and x.islower() and path.count(x) > 1:
            twos += 1
            # print("yeet3", path, twos, x)
    if twos <= 1:
        print(n)
    
    for c in nodes[n]:
        if c not in visited:
            # print("abc")
            new_visited = set(visited)
            if c.islower():
                new_visited.add(c)
            to_do.append((c, new_visited, path + [n]))
        else:
            new_visited = set(visited)
            # if c.islower() and c + "_again" not in new_visited:
            #     new_visited.add(c + "_again")
            #     print(c + "_again")
            #     to_do.append((c, new_visited, path + [n]))
            if c.islower():
                twos = 0
                for x in set(path):
                    if x != 'start' and x != 'end' and x.islower() and path.count(x) > 1:
                        twos += 1
                        # print("abc3", path, twos, x)
                if twos < 1:
                    to_do.append((c, new_visited, path + [n]))
                else:
                    pass
                    # print(path, twos)
        # else:
        #     if c != 'end':
        #         print("abc2", c)
        #         to_do.append((c, visited))

# def new_counts():
#     counts = defaultdict(int)
#     for k in nodes.keys():
#         if 'start' != k and 'end' != k:
#             if k.islower():
#                 counts[k] = 1
#             else:
#                 counts[k] = -1
#     return counts

# def walk(current, counts):
#     global nodes
#     print(current)
#     for child in nodes[current]:
#         if child.islower():
#             if counts[child] != 0:
#                 counts[child] -= 1
#                 walk(child, counts)
#         else:
#             walk(child, new_counts())

# walk('start', new_counts())
# nodes = set()
# edges = set()

# for a in actual:
#     for b in a:
#         nodes.add(b)
#     if 'start' == a[1]:
#         a = (a[1], a[0])
#     if 'end' == a[0]:
#         a = (a[1], a[0])
#     edges.add((a[0], a[1]))
#     if 'start' not in a and 'end' not in a:
#         edges.add((a[1], a[0]))

# print(edges)
# G = nx.DiGraph(list(edges))

# def walk(g, current):
#     for edge in nx.dfs_edges(G, current):
#         print(edge)
#         walk(g, edge[1])
# walk(G, 'start')
# print(list(nx.dfs_edges(G, 'start')))
# for edge in edges.copy():
#     if 'start' not in edge and 'end' not in edge:
#         if edge[0].isupper() and edge[1].islower():
#             edges.remove(edge)
#             edges.add((edge[0]+edge[1], edge[1]+"1"))
#             for edge2 in edges.copy():
#                 if edge2[1] == edge[0]:
#                     edges.add((edge2[0], edge[0]+edge[1]))
#                 elif edge2[0] == edge[1]:
#                     print("yeet", edge, edge2)
#                     edges.remove(edge2)
#                     edges.add((edge[1]+"1", edge2[1]))

# print(edges)

# G = nx.DiGraph(list(edges))

# print(list(nx.all_simple_paths(G, 'start', 'end')))
# print(len(list(nx.all_simple_paths(G, 'start', 'end'))))

# for n in nodes:
#     for simple in nx.all_simple_paths(G, n, 'end'):
#         for simple2 in nx.all_simple_paths(G, 'start', simple[0]):
#             to_print = True
#             maybe = simple2[:-1] + simple
#             for m in maybe:
#                 if m != 'start' and m != 'end' and m.islower() and maybe.count(m) > 1:
#                     to_print = False
#             if to_print:
#                 print(maybe)

# print(actual)