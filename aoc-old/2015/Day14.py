import sys

sys.path.append('../2020')

import utils.utils as utils

class Reinder:
    def __init__(self, name, speed, duration, rest):
        self.name = name
        self.speed = int(speed)
        self.duration = int(duration)
        self.rest = int(rest)

    def __repr__(self):
        return self.name + ", " + str(self.speed) + ", " + str(self.duration) + ", " + str(self.rest)

    def traveled(self, seconds):
        cycle = self.duration + self.rest
        cycles_completed = seconds // cycle
        seconds_in_cycle = seconds % cycle
        total = cycles_completed * self.speed * self.duration
        total += min(self.duration, seconds_in_cycle) * self.speed
        return total

def test_day_fourteen():
    entries = utils.file_to_string_list("Day14sample.txt")
    entries = [e.split(" ") for e in entries]
    entries = [Reinder(e[0], e[3], e[6], e[13]) for e in entries]
    #for e in entries:
        #print(e, e.traveled(1000))

def day_fourteen():
    entries = utils.file_to_string_list("Day14.txt")
    entries = [e.split(" ") for e in entries]
    entries = [Reinder(e[0], e[3], e[6], e[13]) for e in entries]
    entries = [(e.name, e.traveled(2503)) for e in entries]
    assert 2696 == max(entries, key=lambda x: x[1])[1]

def day_fourteen_part_two():
    entries = utils.file_to_string_list("Day14.txt")
    entries = [e.split(" ") for e in entries]
    entries = [Reinder(e[0], e[3], e[6], e[13]) for e in entries]
    points = {}
    for i in range(1, 2504):
        es = [(e.name, e.traveled(i)) for e in entries]
        m = max(es, key=lambda x: x[1])
        if m[0] not in points:
            points[m[0]] = 1
        else: 
            points[m[0]] += 1
    assert 1084 == max(points.values())
        
if __name__=="__main__":
    test_day_fourteen()
    day_fourteen()
    day_fourteen_part_two()