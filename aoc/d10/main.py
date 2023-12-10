from collections import deque

xs = [x.strip('\n') for x in open('input.txt', 'r').readlines()]

G = {}
Y_DIM = len(xs)
X_DIM = len(xs[0])

S = None
S_SHAPE = None
MOVES = {
    '|': ((0,1),(0,-1)), # NS
    '-': ((1,0),(-1,0)), # EW
    'L': ((0,-1),(1,0)), # NE
    'J': ((0,-1),(-1,0)), #NW
    '7': ((0,1),(-1,0)), #SW
    'F': ((0,1),(1,0)) #SE
}

for y in range(len(xs)):
    for x in range(len(xs[y])):
        G[(x+0.0,y+.5)] = '.'
        G[(x+0.0,y-.5)] = '.'
        G[(x+.5,y+0.0)] = '.'
        G[(x-.5,y+0.0)] = '.'
        
        G[(x-.5,y-.5)] = '.'
        G[(x-.5,y+.5)] = '.'
        G[(x+.5,y-.5)] = '.'
        G[(x+.5,y+.5)] = '.'
        
        shape = xs[y][x]
        G[(x+0.0,y+0.0)] = shape
        if shape == 'S':
            S = (x,y)

SC = []
s_up = (S[0],S[1]-1)
if s_up in G:
    s_up_shape = G[s_up]
    if s_up_shape in ('7', 'F', '|'):
        SC.append('N')

s_down = (S[0],S[1]+1)
if s_down in G:
    s_down_shape = G[s_down]
    if s_down_shape in ('|', 'L', 'J'):
        SC.append('S')

s_left = (S[0]-1,S[1])
if s_left in G:
    s_left_shape = G[s_left]
    if s_left_shape in ('-', 'L', 'F'):
        SC.append('W')

s_right = (S[0]+1,S[1])
if s_right in G:
    s_right_shape = G[s_right]
    if s_right_shape in ('-', 'J', '7'):
        SC.append('E')

SC = "".join(sorted(SC))
if SC in ('N', 'S', 'NS'):
    S_SHAPE = '|'
elif SC in ('E', 'W', 'EW'):
    S_SHAPE = '-'
elif SC == 'ES':
    S_SHAPE = 'F'
elif SC == 'EN':
    S_SHAPE = 'L'
elif SC == 'NW':
    S_SHAPE = 'J'
elif SC == 'SW':
    S_SHAPE = '7'

G[S] = S_SHAPE

Q = deque()
seen = set()
Q.append((S, 0))
farthest = (S, 0)
while Q:
    cur, dist = Q.popleft()
    if cur not in seen and cur in G:
        if dist > farthest[1]:
            farthest = (cur, dist)
        cur_shape = G[cur]
        for m in MOVES[cur_shape]:
            Q.append(((cur[0]+m[0], cur[1]+m[1]),dist+1))
            G[(cur[0]+m[0]/2, cur[1]+m[1]/2)] = 'Y'
        G[cur] = 'X'
        seen.add(cur)

print(farthest)

def render(grid, x, y):
    s = ""
    for _y in range(y):
        for _x in range(x):
            s += grid[(_x,_y)]
        s += '\n'
    print(s)


Q = deque()
seen = set()

for _y in range(Y_DIM):
    left = (0.0, _y+0.0)
    left2 = (0.0, _y+.5)
    right = (X_DIM-1.0, _y+0.0)
    right2 = (X_DIM-1.0, _y+.5)
    for x in (left, right, left2, right2):
        if G[x] == '.':
            Q.append((x, (0,)))

for _x in range(X_DIM):
    top = (_x*1.0, 0.0)
    bottom = (_x*1.0, Y_DIM-1.0)
    top2 = (_x+.5, 0.0)
    bottom2 = (_x+.5, Y_DIM-1.0)
    for x in (top, bottom, top2, bottom2):
        if G[x] == '.':
            Q.append((x, (0,)))


while Q:
    cur, path = Q.popleft()
    if cur not in seen and cur in G:
        if G[cur] != 'X':
            G[cur] = 'O'
        for d in [(0.0,.5),(0.0,-.5),(-.5,0.0),(.5,0.0)]:
            nxt = (cur[0]+d[0], cur[1]+d[1])
            if nxt in G and G[nxt] not in ('X', 'Y'):
                Q.append((nxt, path + (cur,)))
    seen.add(cur)
    
# render(G, X_DIM, Y_DIM)

print(len([x for x, v in G.items() if v not in ('X', 'Y', 'O') and (x[0]%1==0.0 and x[1]%1==0.0)]))