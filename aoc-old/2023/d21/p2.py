xs = [x.strip('\n') for x in open('input.txt', 'r').readlines()]

X_DIM = len(xs[0])
Y_DIM = len(xs)

G = {}
S = None
for y in range(len(xs)):
    for x in range(len(xs[y])):
        G[(x,y)] = xs[y][x]
        if G[(x,y)] == 'S':
            S = (x,y)
            G[(x,y)] = '.'

print(S)

counts = {}
counts[S] = 1

terms = []

from collections import deque
at = set()
at.add(S)
for i in range(1, 500):
    Q = deque()
    Q.extend(at)
    at = set()
    while Q:
        cur = Q.popleft()
        for D in [(0,1),(0,-1),(1,0),(-1,0)]:
            nxt_m = ((cur[0]+D[0])%X_DIM,(cur[1]+D[1])%Y_DIM)
            nxt = ((cur[0]+D[0]),(cur[1]+D[1]))
            if nxt_m in G and G[nxt_m] == '.':
                at.add(nxt)
    if i % 131 == 65:
        terms.append(len(at))
    if len(terms) == 3:
        break
    # print(i, len(at))

# i looked at this for too long trying to find a pattern
# before eventually seeing on reddit that you can fit a quadratic
# curve using the values for f(65), f(131+65), f(131*2+65).
# i guess i at least had already solved the problem of 
# being able to generate those values.
    
# quadratic stuff below came from chatgpt with some slight modifications.
# i kept getting a bunch of wrong answers from numpy
# (i originally used wolfram alpha to do the fitting).
# i think the important part was rounding the coefficients first.
import numpy as np

# Sample data
x = np.array([0, 1, 2])
y = np.array(terms)

n = len(x)
A = np.vstack([x**2, x, np.ones(n)]).T
coefficients = np.linalg.solve(A.T @ A, A.T @ y)

# Extract coefficients
a, b, c = [round(x) for x in coefficients]
print(a,b,c)
x = (26501365-65)/131
print(int(a*x**2 + b*x + c))
