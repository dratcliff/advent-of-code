def get_level(n):
    i = 1
    while (i ) ** 2 < n:
        i += 2
    return i//2

print(get_level(8))
print(get_level(23))
print(get_level(47))
print(get_level(1024))

def get_steps(n):
    level = get_level(n)
    in_level = (level*2+1)**2 - ((level-1)*2+1)**2
    
    last_corner = (level*2+1)**2
    corners = []
    for i in range(0, 4):
        corners.append(last_corner - i*((level*2+1)-1))
    
    c = min([abs(n-x) for x in corners])
    print(corners, c)
    return (level*2+1)//2 -c + level

print(get_steps(1))
print(get_steps(12))
print(get_steps(23))
print(get_steps(1024))
print(get_steps(289326))