"""
Got so frustrated with this one... part one originally finished in about 1.5 hours.
Found this solution: https://www.reddit.com/r/adventofcode/comments/ec8090/2019_day_18_solutions/fbagnxw
Modified my part one to be closer to this so that it would complete in a reasonable amount of time,
then shamelessly used this programmer's part two modifications as well.
"""

from textwrap import dedent
import string
from collections import deque
from test_one import getLines

debug = False

class MyMaze:
    def __init__(self, text):
        self.grid = {(j, i): w for i, v in enumerate(text) for j, w in enumerate(v)}
        self.keys = {}
        self.doors = {}
        self.reachable = {}
        self.reachable_cache = {}
        self.sick_of_this_cache = {}
        self.minimum = 9999999

        for k, v in self.grid.items():
            if v in list(string.ascii_lowercase):
                self.keys[v] = k
            if v in list(string.ascii_uppercase):
                self.doors[v] = k
            if v == '@':
                self.start = k
            if v == '1':
                self.start1 = k
            if v == '2':
                self.start2 = k
            if v == '3':
                self.start3 = k
            if v == '4':
                self.start4 = k
        self.bfs(self.start1)
        self.bfs(self.start2)
        self.bfs(self.start3)
        self.bfs(self.start4)
        for k, v in self.keys.items():
            self.bfs(v)
        if debug:
            for k, v in self.reachable.items():
                print("reachable", k, v)
            for k, v in self.keys.items():
                print("key", k, v)
            for k, v in self.doors.items():
                print("door", k, v)

    def bfs(self, start):
        def next_tuple(current_tuple, next_position):
            next_grid_val = self.grid[next_position]
            if next_grid_val == "#":
                return None
            if next_grid_val in string.ascii_uppercase:
                next_doors = current_tuple[2] + (next_grid_val,)
            else: 
                next_doors = current_tuple[2]
            if next_grid_val in string.ascii_lowercase:
                start_sym = self.grid[current_tuple[0]]
                if start_sym not in self.reachable:
                    self.reachable[start_sym] = {}
                if next_grid_val not in self.reachable[start_sym]:
                    self.reachable[start_sym][next_grid_val] = (next_doors, current_tuple[3]+1)

            return (current_tuple[0], next_position, next_doors, current_tuple[3]+1)
            
        
        queue = deque([])
        discovered = {}
        start_item = (start, start, (), 0)
        queue.append(start_item)
        discovered[start] = True
        while len(queue) > 0:
            v = queue.popleft()
            print(v)
            v_start = v[0]
            v_pos = v[1]
            v_doors = v[2]
            vx = v_pos[0]
            vy = v_pos[1]
            for next_pos in ((vx+1, vy), (vx-1, vy), (vx, vy+1), (vx, vy-1)):
                if next_pos not in discovered and next_pos in self.grid:
                    discovered[next_pos] = True
                    n = next_tuple(v, next_pos)
                    if n:
                        queue.append(n)

    def get_reachable(self, start, acquired_keys):
        sa = acquired_keys
        if (start, sa) in self.reachable_cache:
            return self.reachable_cache[(start, sa)]
        if debug:
            for k, v in self.reachable[start].items():
                print("get_reachable", k, v, "acquired keys", acquired_keys)
        t = ()
        for k, v in self.reachable[start].items():
            if k not in acquired_keys:
                required_keys = v[0]
                if debug:
                    print("required keys", required_keys)
                if all(i.lower() in acquired_keys for i in required_keys):
                    if debug:
                        print("all required keys present", required_keys, acquired_keys) 
                    r = (k, v[1])
                    t = t + (r,)
        if debug:
            print("will return", t, "from get reachable")
        self.reachable_cache[(start, sa)] = t
        return t


    """
    1  procedure BFS(G,start_v):
    2      let Q be a queue
    3      label start_v as discovered
    4      Q.enqueue(start_v)
    5      while Q is not empty
    6          v = Q.dequeue()
    7          if v is the goal:
    8              return v
    9          for all edges from v to w in G.adjacentEdges(v) do
    10             if w is not labeled as discovered:
    11                 label w as discovered
    12                 w.parent = v
    13                 Q.enqueue(w) 
    """

    def sick_of_this(self, start, remaining, acquired_keys, accum):
        if accum > self.minimum:
            return accum
        sr = tuple(sorted(remaining))
        sa = tuple(sorted(acquired_keys))
        if start in self.sick_of_this_cache:
            if sr in self.sick_of_this_cache[start]:
                if sa in self.sick_of_this_cache[start][sr]:
                    if accum in self.sick_of_this_cache[start][sr][sa]:
                        return self.sick_of_this_cache[start][sr][sa][accum]
        if debug:
            print("start", start, "remaining", remaining, "acquired", acquired_keys, "accum", accum)
        if len(remaining) == 0:
            return accum
        next = self.get_reachable(start, acquired_keys)
        result = 99999
        for r in next:
            new_remaining = tuple(i for i in remaining if i != r[0])
            new_acquired = acquired_keys + (r[0],)
            new_accum = accum + self.reachable[start][r[0]][1]
            if debug:
                print("new_remaining", new_remaining, "new acquired", new_acquired, "new accum", new_accum)
            if new_accum < self.minimum:
                result = self.sick_of_this(r[0], new_remaining, new_acquired, new_accum)
                if result < self.minimum:
                    self.minimum = result
                    print(self.minimum)
            else:
                result = new_accum
                break
        if start not in self.sick_of_this_cache:
            self.sick_of_this_cache[start] = {}
        if sr not in self.sick_of_this_cache[start]:
            self.sick_of_this_cache[start][sr] = {}
        if sa not in self.sick_of_this_cache[start][sr]:
            self.sick_of_this_cache[start][sr][sa] = {}
        if accum not in self.sick_of_this_cache[start][sr][sa]:
            self.sick_of_this_cache[start][sr][sa][accum] = {}
        self.sick_of_this_cache[start][sr][sa][accum] = result
        return result

    def sick_of_this2(self, start, remaining, acquired_keys, accum):
        if debug:
            print("start", start, "remaining", remaining, "acquired", acquired_keys, "accum", accum)
        tracked = {(('1','2','3','4'),frozenset()):0}
        for _ in range(0, len(self.keys)):
            next = {}
            for item in tracked:
                curlocs, curkeys, curdist = item[0], item[1], tracked[item]
                for newkey in self.keys:
                    if newkey not in curkeys:
                        for robot in range(4):
                            if debug:
                                print("newkey", newkey, "curkeys", curkeys)
                            r = self.get_reachable(curlocs[robot], curkeys)
                            if debug:
                                print("r", r)
                            reachable_tuple = None
                            for ri in r:
                                if ri[0] == newkey:
                                    reachable_tuple = ri
                            if reachable_tuple != None:
                                dist = reachable_tuple[1]
                                if debug:
                                    print("dist", dist, "curloc", curloc, "reachable_tuple", reachable_tuple, "curdist", curdist)
                                newdist = curdist + dist
                                newkeys = frozenset(curkeys | set((newkey,)))
                                newlocs = list(curlocs)
                                newlocs[robot] = newkey
                                newlocs = tuple(newlocs)

                                if (newlocs, newkeys) not in next or newdist < next[(newlocs, newkeys)]:
                                    next[(newlocs, newkeys)] = newdist
            tracked = next
        print(tracked)
        print(min(tracked.values()))
        
            
def sample_one():
    maze = """#########
              #b.A.@.a#
              #########""".splitlines()
    maze = [dedent(x) for x in maze]
    my_maze = MyMaze(maze)
    remaining = tuple(v for v in my_maze.keys.keys())
    r = my_maze.sick_of_this2("@", remaining, (), 0)
    # remaining = tuple(v for v in my_maze.keys.keys())
    # r = my_maze.sick_of_this("@", remaining, (), 0)
    # print(r)

    # first_stop = my_maze.BFS(my_maze.start)
    # second_stop = my_maze.BFS(first_stop)
    # print(nx.shortest_path(my_maze.graph, my_maze.start, first_stop))
    # print(nx.shortest_path(my_maze.graph, first_stop, second_stop))

def sample_two():
    maze = """########################
              #f.D.E.e.C.b.A.@.a.B.c.#
              ######################.#
              #d.....................#
              ########################""".splitlines()
    maze = [dedent(x) for x in maze]
    my_maze = MyMaze(maze)
    remaining = tuple(v for v in my_maze.keys.keys())
    r = my_maze.sick_of_this2("@", remaining, (), 0)
    print(r)

    # print(walk(my_maze, my_maze.start, 0))

    # first_stop = my_maze.start
    # second_stop =  my_maze.BFS(first_stop)
    # count = len(nx.shortest_path(my_maze.graph, first_stop, second_stop))-1
    
    # done = False
    # while not done:
    #     first_stop = second_stop
    #     second_stop = my_maze.DFS(first_stop)   
    #     count += len(nx.shortest_path(my_maze.graph, first_stop, second_stop))-1
    #     done = my_maze.all_keys_acquired()

    # print(count)

    

def sample_three():
    maze = """#################
            #i.G..c...e..H.p#
            ########.########
            #j.A..b...f..D.o#
            ########@########
            #k.E..a...g..B.n#
            ########.########
            #l.F..d...h..C.m#
            #################""".splitlines()
    maze = [dedent(x) for x in maze]
    my_maze = MyMaze(maze)
    remaining = tuple(v for v in my_maze.keys.keys())
    print(my_maze.sick_of_this("@", remaining, (), 0))
              
# sample_one()
# sample_two()
# sample_three()

def sample_four():
    maze = """########################
            #@..............ac.GI.b#
            ###d#e#f################
            ###A#B#C################
            ###g#h#i################
            ########################""".splitlines()
    maze = [dedent(x) for x in maze]
    my_maze = MyMaze(maze)
    remaining = tuple(v for v in my_maze.keys.keys())
    print(my_maze.sick_of_this("@", remaining, (), 0))

def part_one():
    maze = getLines("18.txt", to_int=False)
    my_maze = MyMaze(maze)
    remaining = tuple(v for v in my_maze.keys.keys())
    print(my_maze.sick_of_this2("@", remaining, (), 0))

def part_two():
    maze = getLines("182b.txt", to_int=False)
    my_maze = MyMaze(maze)
    remaining = tuple(v for v in my_maze.keys.keys())
    print(my_maze.sick_of_this2("@", remaining, (), 0))

part_two()