NS = set(["N", "S", 0, 180])
EW = set(["E", "W", 90, 270])
SW = set(["S", "W", 180, 270])
class Ship:
    def __init__(self):
        self.direction = 90
        self.x = 0
        self.y = 0
        self.waypoint = {}
        self.waypoint["x"] = 0
        self.waypoint["y"] = 0

    def turn(self, direction, degrees):
        if direction == "L":
            degrees *= -1
        self.direction += degrees
        self.direction %= 360

    def move(self, direction, distance):
        if direction in SW or direction == "F" and self.direction in SW:
            distance *= -1
        if direction in NS or (direction == "F" and self.direction in NS):
            self.y += distance
        if direction in EW or (direction == "F" and self.direction in EW):
            self.x += distance


def run(filename):
    samples = [x.strip('\n') for x in open(filename)]
    instructions = [(x[0], int(x[1:])) for x in samples]
    
    ship = Ship()
    
    for x in instructions:
        if x[0] == "L" or x[0] == "R":
            ship.turn(x[0], x[1])
        else:
            ship.move(x[0], x[1])

    
    return ship

def test_day_twelve():
    ship = run("Day12sample.txt")
    assert 25 == abs(ship.x) + abs(ship.y)

def day_twelve():
    ship = run("Day12.txt")
    assert 364 == abs(ship.x) + abs(ship.y)

if __name__=="__main__":
    test_day_twelve()
    day_twelve()