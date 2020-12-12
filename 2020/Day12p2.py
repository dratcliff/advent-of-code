import math

NS = set(["N", "S", 0, 180])
EW = set(["E", "W", 90, 270])
SW = set(["S", "W", 180, 270])

class Ship:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.waypoint = {}
        self.waypoint["x"] = 10
        self.waypoint["y"] = 1

    def rotate_waypoint(self, direction, angle):
        if direction == "R":
            angle *= -1
        angle = math.radians(angle)
        cosa = round(math.cos(angle))
        sina = round(math.sin(angle))

        new_x = cosa * self.waypoint["x"] - sina * self.waypoint["y"]
        new_y = sina * self.waypoint["x"] + cosa     * self.waypoint["y"]
        self.waypoint["x"] = round(new_x)
        self.waypoint["y"] = round(new_y)

    def move_waypoint(self, direction, distance):
        if direction in SW:
            distance *= -1
        if direction in NS:
            self.waypoint["y"] += distance
        if direction in EW:
            self.waypoint["x"] += distance

    def move_ship(self, times):
        for i in range(0, times):
            self.x += self.waypoint["x"]
            self.y += self.waypoint["y"]

def run(filename):
    samples = [x.strip('\n') for x in open(filename)]
    instructions = [(x[0], int(x[1:])) for x in samples]
    
    ship = Ship()
    
    for x in instructions:
        if x[0] == "L" or x[0] == "R":
            ship.rotate_waypoint(x[0], x[1])
        elif x[0] == "F":
            ship.move_ship(x[1])
        else:
            ship.move_waypoint(x[0], x[1])
    return ship

def test_day_twelve():
    ship = run("Day12sample.txt")
    ans = abs(ship.x) + abs(ship.y)
    assert 286 == ans

def day_twelve():
    ship = run("Day12.txt")
    assert 39518 == abs(ship.x) + abs(ship.y)

if __name__=="__main__":
    test_day_twelve()
    day_twelve()