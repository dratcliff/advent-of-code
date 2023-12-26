xs = [x.strip('\n') for x in open('input.txt', 'r').readlines()]

# xs = """2413432311323
# 3215453535623
# 3255245654254
# 3446585845452
# 4546657867536
# 1438598798454
# 4457876987766
# 3637877979653
# 4654967986887
# 4564679986453
# 1224686865563
# 2546548887735
# 4322674655533
# """.split('\n')

xs = [x for x in xs if len(x) > 0]

import heapq

rev = {
    'D': 'U',
    'U': 'D',
    'L': 'R',
    'R': 'L',
    'Z': 'Z'
}

def dijkstra(graph, start):
    distances = {}
    for node in graph:
        distances[node] = {
            2: {},
            1: {},
            0: {}
        }

    priority_queue = [(0, start, ('Z',))]

    while priority_queue:
        current_distance, current_node, path = heapq.heappop(priority_queue)
        last_three = path[-3:]

        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            dir = None
            if neighbor[0] < current_node[0]:
                dir = 'L'
            elif neighbor[0] > current_node[0]:
                dir = 'R'
            elif neighbor[1] < current_node[1]:
                dir = 'U'
            elif neighbor[1] > current_node[1]:
                dir = 'D'
            else:
                raise Exception
            if len(last_three) == 3 and last_three[-1] == last_three[-2] == last_three[-3] == dir:
                continue
            if last_three[-1] != dir:
                turn_in = 2
            else:
                turn_in = 1
                if len(last_three) >= 2 and last_three[-2] == dir:
                    turn_in = 0
            last_dir = last_three[-1]
            if dir == rev[last_dir]:
                continue
            # Update distance if a shorter path is found
            if last_dir not in distances[neighbor][turn_in] or distance < distances[neighbor][turn_in][last_dir]:
                distances[neighbor][turn_in][last_dir] = distance
                heapq.heappush(priority_queue, (distance, neighbor, path + (dir,)))

    return distances


def dijkstra2(graph, start):
    distances = {}
    for node in graph:
        distances[node] = {}
        for i in range(-10, 11):
            distances[node][i] = {}

    priority_queue = [(0, start, ('Z',))]

    while priority_queue:
        current_distance, current_node, path = heapq.heappop(priority_queue)
        last_three = path[-3:]

        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            dir = None
            if neighbor[0] < current_node[0]:
                dir = 'L'
            elif neighbor[0] > current_node[0]:
                dir = 'R'
            elif neighbor[1] < current_node[1]:
                dir = 'U'
            elif neighbor[1] > current_node[1]:
                dir = 'D'
            else:
                raise Exception
            
            last_dir = last_three[-1]
            
            # not at least 4 in a row, can't turn
            if last_dir != dir:
                if 'Z' not in path[-4:] and len(path[-4:]) == 4 and len(set(path[-4:])) != 1:
                    continue
            # more than ten, should've turned
            if last_dir == dir and len(path[-10:]) == 10 and len(set(path[-10:])) == 1:
                continue
            if dir == rev[last_dir]:
                continue
            # Update distance if a shorter path is found
            
            turn_in = -100

            if 'Z' in path[-4:] or len(path[-4:]) < 4 or len(set(path[-4:])) != 1:
                turn_in = -4
                p = path[-4:]
                i = len(p) - 1
                while i >= 0 and p[i] == dir:
                    turn_in += 1
                    i -= 1
            else:
                turn_in = 10
                p = path[-10:]
                i = len(p) - 1
                while i >= 0 and p[i] == dir:
                    turn_in -= 1
                    i -= 1

            assert turn_in != -100

            if last_dir not in distances[neighbor][turn_in] or distance < distances[neighbor][turn_in][last_dir]:
                distances[neighbor][turn_in][last_dir] = distance
                heapq.heappush(priority_queue, (distance, neighbor, path + (dir,)))

    return distances


G = {}
for y in range(len(xs)):
    for x in range(len(xs[y])):
        pt = (x,y)
        if pt not in G:
            G[pt] = {}
        for D in [(1,0), (-1,0), (0,1), (0,-1)]:
            adj = (x+D[0],y+D[1])
            if 0 <= adj[1] < len(xs) and 0 <= adj[0] < len(xs[y]):
                G[pt][adj] = int(xs[adj[1]][adj[0]])

start_node = (0,0)
end_node = (len(xs[0])-1, len(xs)-1)

shortest_distances = dijkstra(G, start_node)
m = 100000000
for k, v in shortest_distances[end_node].items():
    for k2, v2 in v.items():
        if v2 < m:
            m = v2

print(m)

shortest_distances = dijkstra2(G, start_node)
m = 100000000
for k, v in shortest_distances[end_node].items():
    for k2, v2 in v.items():
        if v2 < m:
            m = v2

print(m)