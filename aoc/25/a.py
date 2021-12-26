from utilaoc import file_to_grid

actual = file_to_grid("a.txt")

def run2(a):
    next_a = {}
    for k, v in a.items():
        next_a[k] = v
    moved = False
    for k in a.keys():
        if a[k] == 'v':
            if (k[0], k[1]+1) not in a:
                if a[(k[0], 0)] == '.':
                    next_a[(k[0], 0)] = 'v'
                    next_a[k] = '.'
                    moved = True
            elif a[(k[0], k[1]+1)] == '.':
                next_a[(k[0], k[1]+1)] = 'v'
                next_a[k] = '.'
                moved = True
    return moved, next_a

def run1(a):
    next_a = {}
    for k, v in a.items():
        next_a[k] = v
    moved = False
    for k in a.keys():
        if a[k] == '>':
            if (k[0]+1, k[1]) not in a:
                if a[(0, k[1])] == '.':
                    next_a[(0, k[1])] = '>'
                    next_a[k] = '.'
                    moved = True
            elif a[(k[0]+1, k[1])] == '.':
                next_a[(k[0]+1, k[1])] = '>'
                next_a[k] = '.'
                moved = True
    return moved, next_a



moved = True
i = 0
while moved:
    moved1, actual = run1(actual)
    moved2, actual = run2(actual)
    moved = moved1 or moved2
    i += 1
print(i)
    
            