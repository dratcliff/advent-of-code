import utils


class Cup:
    def __init__(self, label, clockwise_cup):
        self.label = label
        self.clockwise_cup = None

def init(starting_string, size):

    m = {}
    for i in range(0, len(starting_string)):
        v = int(starting_string[i])
        m[v] = Cup(v, None)
    
    for i in range(0, len(starting_string)-1):
        v = int(starting_string[i])
        w = int(starting_string[i+1])
        m[v].clockwise_cup = m[w]
    
    last = int(starting_string[-1])
    first = int(starting_string[0])
    biggest = max(m.keys())    

    # print(m, biggest)

    for i in range(biggest+1, size+1):
        m[i] = Cup(i, None)

    m[last].clockwise_cup = m[biggest+1]
    # print("mlast", m[last].clockwise_cup.label)

    for i in range(biggest+1, size):
        m[i].clockwise_cup = m[i+1]

    m[size].clockwise_cup = m[first]

    m["max"] = max(m.keys())
    m["cur"] = first
    return m

def move(m):
    """
    The crab picks up the three cups that are immediately clockwise of the current cup. 
    They are removed from the circle; cup spacing is adjusted as necessary to maintain the circle.

    The crab selects a destination cup: the cup with a label equal to the current cup's label minus one. 
    If this would select one of the cups that was just picked up, the crab will keep subtracting one until 
    it finds a cup that wasn't just picked up. If at any point in this process the value goes below the 
    lowest value on any cup's label, it wraps around to the highest value on any cup's label instead.

    The crab places the cups it just picked up so that they are immediately clockwise 
    of the destination cup. They keep the same order as when they were picked up.
    The crab selects a new current cup: the cup which is immediately clockwise of the current cup.
    """

    # pick up
    current = m[m["cur"]]
    # print("current", current.label)
    c1 = current.clockwise_cup
    c2 = c1.clockwise_cup
    c3 = c2.clockwise_cup

    current.clockwise_cup = c3.clockwise_cup
    m["cur"] = c3.clockwise_cup.label

    labels = set([c1.label, c2.label, c3.label])
    # print("neighbors", labels)
    # destination
    destination = current.label - 1
    while destination in labels:
        destination -= 1
    
    if destination <= 0:
        destination = m["max"]
    # print("destination", destination)
    c3.clockwise_cup = m[destination].clockwise_cup
    m[destination].clockwise_cup = c1

    return m

@utils.timed
def test_day_twenty_three():
    starting_string = "389125467"
    m = init(starting_string, 1_000_000)
    for i in range(0, 10_000_000):
        m = move(m)

    one = m[1]
    first = one.clockwise_cup
    second = first.clockwise_cup

    print(first.label, second.label, first.label*second.label)
    
@utils.timed
def day_twenty_three():
    starting_string = "123487596"
    m = init(starting_string, 1_000_000)
    for i in range(0, 10_000_000):
        m = move(m)

    one = m[1]
    first = one.clockwise_cup
    second = first.clockwise_cup

    print(first.label, second.label, first.label*second.label)

if __name__=="__main__":
    test_day_twenty_three()
    day_twenty_three()