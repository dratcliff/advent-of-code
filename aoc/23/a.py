costs = {
    'A': 1,
    'B': 10,
    'C': 100,
    'D': 1000
}

def print_board(b):
    t = \
"""
#############
#12.4.6.8.0a#
###b#d#h#i###
  #y#w#u#s#
  #c#x#v#t#
  #z#e#f#g#
  #########
"""
    t = t.replace("1", b.hallway[0])
    t = t.replace("2", b.hallway[1])
    t = t.replace("b", b.hallway[2][3])
    t = t.replace("z", b.hallway[2][0])
    t = t.replace("y", b.hallway[2][2])
    t = t.replace("c", b.hallway[2][1])
    t = t.replace("4", b.hallway[3])
    t = t.replace("d", b.hallway[4][3])
    t = t.replace("w", b.hallway[4][2])
    t = t.replace("x", b.hallway[4][1])
    t = t.replace("e", b.hallway[4][0])
    t = t.replace("6", b.hallway[5])
    t = t.replace("h", b.hallway[6][3])
    t = t.replace("u", b.hallway[6][2])
    t = t.replace("v", b.hallway[6][1])
    t = t.replace("f", b.hallway[6][0])
    t = t.replace("8", b.hallway[7])
    t = t.replace("i", b.hallway[8][3])
    t = t.replace("s", b.hallway[8][2])
    t = t.replace("t", b.hallway[8][1])
    t = t.replace("g", b.hallway[8][0])
    t = t.replace("0", b.hallway[9])
    t = t.replace("a", b.hallway[10])
    print(t, b.cost)

def is_done(b):
    return b.hallway[2][0] == b.hallway[2][1] == b.hallway[2][2] == b.hallway[2][3] == 'A' and \
        b.hallway[4][0] == b.hallway[4][1] == b.hallway[4][2] == b.hallway[4][3] == 'B' and \
        b.hallway[6][0] == b.hallway[6][1] == b.hallway[6][2] == b.hallway[6][3] == 'C' and \
        b.hallway[8][0] == b.hallway[8][1] == b.hallway[8][2] == b.hallway[8][3] == 'D'

class Board:
    def __init__(self):
        self.hallway = None
        self.cost = 0
        self.prev = []

import copy

best = -1

seen = set()
def get_next_states(board):
    global best
    if best != -1 and board.cost > best:
        return
    key = tuple(tuple(x) for x in board.hallway) + (board.cost,)
    if key in seen:
        return
    seen.add(key)
    states = []
    rooms = [2, 4, 6, 8]
    spaces = [0, 1, 3, 5, 7, 9, 10]
    h = board.hallway
    for r in rooms:
        pos = 3
        pod = h[r][pos]
        if pod == '.':
            pos -= 1
            pod = h[r][pos]
        if pod == '.':
            pos -= 1
            pod = h[r][pos]
        if pod == '.':
            pos -= 1
            pod = h[r][pos]
        if pod == '.':
            continue
        if pos == 0:
            if r == 2:
                if pod == 'A':
                    continue
            elif r == 4:
                if pod == 'B':
                    continue
            elif r == 6:
                if pod == 'C':
                    continue
            elif r == 8:
                if pod == 'D':
                    continue
        elif pos == 1:
            below_pod = h[r][0]
            if r == 2:
                if pod == below_pod == 'A':
                    continue
            elif r == 4:
                if pod == below_pod == 'B':
                    continue
            elif r == 6:
                if pod == below_pod == 'C':
                    continue
            elif r == 8:
                if pod == below_pod == 'D':
                    continue
        elif pos == 2:
            below_pod = h[r][1]
            below_pod2 = h[r][0]
            if r == 2:
                if pod == below_pod == below_pod2 == 'A':
                    continue
            elif r == 4:
                if pod == below_pod == below_pod2 == 'B':
                    continue
            elif r == 6:
                if pod == below_pod == below_pod2 == 'C':
                    continue
            elif r == 8:
                if pod == below_pod == below_pod2 == 'D':
                    continue
        elif pos == 3:
            below_pod = h[r][2]
            below_pod2 = h[r][1]
            below_pod3 = h[r][0]
            if r == 2:
                if pod == below_pod == below_pod2 == below_pod3 == 'A':
                    continue
            elif r == 4:
                if pod == below_pod == below_pod2 == below_pod3 =='B':
                    continue
            elif r == 6:
                if pod == below_pod == below_pod2 == below_pod3 =='C':
                    continue
            elif r == 8:
                if pod == below_pod == below_pod2 == below_pod3 =='D':
                    continue
        left = list(reversed([x for x in spaces if x < r]))
        i = 0
        while i < len(left) and h[left[i]] == '.':
            new_h = copy.deepcopy(h)
            new_h[r][pos] = '.'
            new_h[left[i]] = pod
            b = Board()
            b.hallway = new_h
            b.cost = board.cost + (abs(r-left[i])+(4-pos))*costs[pod]
            b.prev = board.prev + [b]
            states.append(b)
            i += 1

        right = [x for x in spaces if x > r]
        i = 0
        while i < len(right) and h[right[i]] == '.':
            new_h = copy.deepcopy(h)
            new_h[r][pos] = '.'
            new_h[right[i]] = pod
            b = Board()
            b.hallway = new_h
            b.cost = board.cost + (abs(r-right[i])+(4-pos))*costs[pod]
            b.prev = board.prev + [b]
            states.append(b)
            i += 1


    for s in spaces:
        if h[s] == '.':
            continue
        pod = h[s]
        r = -1
        if pod == 'A':
            r = 2
        elif pod == 'B':
            r = 4
        elif pod == 'C':
            r = 6
        elif pod == 'D':
            r = 8
        else:
            raise Exception("what")
        destination = 1
        move = True
        if s > r:
            ms = [x for x in spaces if x > r and x < s]   
            for m in ms:
                if h[m] != '.':
                    move = False
            if not move:
                continue
        else:
            move = True
            ms = [x for x in spaces if x < r and x > s]   
            for m in ms:
                if h[m] != '.':
                    move = False
            if not move:
                continue
        
        move = True
        for i in range(0, 4):
            if h[r][i] != '.' and h[r][i] != pod:
                move = False
        if not move:
            continue

        if h[r][0] == h[r][1] == h[r][2] == h[r][3] == '.':
            destination = 0
        elif h[r][1] == h[r][2] == h[r][3] == '.':
            destination = 1
        elif h[r][2] == h[r][3] == '.':
            destination = 2
        elif h[r][3] == '.':
            destination = 3
        else:
            if h[r][0] == '.':
                if h[r][1] != '.':
                    if h[r][1] == pod:
                        new_h = copy.deepcopy(h)
                        new_h[r][0] = pod
                        new_h[r][1] = '.'
                        b = Board()
                        b.hallway = new_h
                        b.cost = board.cost + costs[pod]
                        states.append(b)
                        continue
                    else:
                        continue
            elif h[r][1] == '.':
                if h[r][2] != '.':
                    if h[r][2] == pod:
                        new_h = copy.deepcopy(h)
                        new_h[r][1] = pod
                        new_h[r][2] = '.'
                        b = Board()
                        b.hallway = new_h
                        b.cost = board.cost + costs[pod]
                        states.append(b)
                        continue
                    else:
                        continue
            elif h[r][2] == '.':
                if h[r][3] != '.':
                    if h[r][3] == pod:
                        new_h = copy.deepcopy(h)
                        new_h[r][2] = pod
                        new_h[r][3] = '.'
                        b = Board()
                        b.hallway = new_h
                        b.cost = board.cost + costs[pod]
                        states.append(b)
                        continue
                    else:
                        continue
        new_h = copy.deepcopy(h)
        new_h[r][destination] = pod
        new_h[s] = '.'
        b = Board()
        b.hallway = new_h
        b.cost = board.cost + (abs(s-r) + (4 - destination))*costs[pod]
        b.prev = board.prev + [b]
        states.append(b)
       
    
    if len(states) == 0:
        if is_done(board) and (best == -1 or board.cost < best):
            best = board.cost
            print("best", best)
    else:
        for state in states:
            get_next_states(state)

b = Board()
hallway = ['.', '.', ['B', 'D', 'D', 'C'], '.', ['A', 'B', 'C', 'D'], '.', ['B', 'A', 'B', 'D'], '.', ['C', 'C', 'A', 'A'], '.', '.']
b.hallway = hallway

get_next_states(b)
