class Instruction:
    def __init__(self, desc, start, end):
        self.desc = desc
        start = start.split(",")
        self.start = (int(start[0]), int(start[1]))
        end = end.split(",")
        self.end = (int(end[0]), int(end[1]))

def parse(filename):
    entries = []
    with open(filename) as f:
        for line in f:
            entries.append(line)

    parsed = []
    for e in entries:
        if "turn on" in e:
            e = e.split(" ")
            parsed.append(Instruction("on", e[2], e[4]))
        if "turn off" in e:
            e = e.split(" ")
            parsed.append(Instruction("off", e[2], e[4]))
        if "toggle" in e:
            e = e.split(" ")
            parsed.append(Instruction("toggle", e[1], e[3]))

    for p in parsed:
        return parsed

def day_six():
    instructions = parse("Day6.txt")
    lights = {}
    for i in range(0, 1000):
        lights[i] = {}
        for j in range(0, 1000):
            lights[i][j] = "off"

    for i in instructions:
        if i.desc == "on":
            for x in range(i.start[0], i.end[0]+1):
                for y in range(i.start[1], i.end[1]+1):
                    lights[x][y] = "on"
        if i.desc == "off":
            for x in range(i.start[0], i.end[0]+1):
                for y in range(i.start[1], i.end[1]+1):
                    lights[x][y] = "off"
        if i.desc == "toggle":
            for x in range(i.start[0], i.end[0]+1):
                for y in range(i.start[1], i.end[1]+1):
                    if lights[x][y] == "on":
                        lights[x][y] = "off"
                    else:
                        lights[x][y] = "on"
    ct = 0

    for x in lights:
        for y in lights[x]:
            if lights[x][y] == "on":
                ct += 1

    assert 377891 == ct

def day_six_part_two():
    instructions = parse("Day6.txt")
    lights = {}
    for i in range(0, 1000):
        lights[i] = {}
        for j in range(0, 1000):
            lights[i][j] = 0

    for i in instructions:
        if i.desc == "on":
            for x in range(i.start[0], i.end[0]+1):
                for y in range(i.start[1], i.end[1]+1):
                    lights[x][y] += 1
        if i.desc == "off":
            for x in range(i.start[0], i.end[0]+1):
                for y in range(i.start[1], i.end[1]+1):
                    cur = lights[x][y]
                    if cur > 0:
                        lights[x][y] -= 1
        if i.desc == "toggle":
            for x in range(i.start[0], i.end[0]+1):
                for y in range(i.start[1], i.end[1]+1):
                    lights[x][y] += 2
    brightness = 0

    for x in lights:
        for y in lights[x]:
            brightness += lights[x][y]

    assert 14110788 == brightness

if __name__=="__main__":
    day_six()
    day_six_part_two()