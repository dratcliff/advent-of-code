from utilaoc import file_to_strings

def run():
    input = file_to_strings("day1.txt")
    input = input[0]
    input = input.split(", ")
    input = [(x[0], int(x[1:])) for x in input]


    current_direction = 'N'
    pos = (0, 0)
    visited = set()
    for x in input:
        if x[0] == 'R':
            new_direction = ''
            if current_direction == 'N':
                new_direction = 'E'
            elif current_direction == 'E':
                new_direction = 'S'
            elif current_direction == 'S':
                new_direction = 'W'
            else:
                new_direction = 'N'
            current_direction = new_direction
        else:
            new_direction = ''
            if current_direction == 'N':
                new_direction = 'W'
            elif current_direction == 'W':
                new_direction = 'S'
            elif current_direction == 'S':
                new_direction = 'E'
            else:
                new_direction = 'N'
            current_direction = new_direction
        new_pos = None
        if current_direction == 'N':
            new_pos = (pos[0], pos[1]+x[1])
        elif current_direction == 'S':
            new_pos = (pos[0], pos[1]-x[1])
        elif current_direction == 'E':
            new_pos = (pos[0]+x[1], pos[1])
        else:
            new_pos = (pos[0]-x[1], pos[1])
        x_inc = 1
        y_inc = 1
        if new_pos[0] < pos[0]:
            x_inc = -1
        if new_pos[1] < pos[1]:
            y_inc = -1

        if pos[1] == new_pos[1]:
            for i in range(1, abs(pos[0]-new_pos[0])+1):
                n = (pos[0] + i*x_inc, pos[1])
                if n not in visited:
                    visited.add(n)
                else:
                    print(abs(n[0]) + abs(n[1]))
                    return
        if pos[0] == new_pos[0]:
            for i in range(1, abs(pos[1]-new_pos[1])+1):
                n = (pos[0], pos[1] + i * y_inc)
                if n not in visited:
                    visited.add(n)
                else:
                    print(abs(n[0]) + abs(n[1]))
                    return
            
        pos = new_pos

run()