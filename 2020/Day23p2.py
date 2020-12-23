import utils


class Cup:
    def __init__(self, label, clockwise_cup):
        self.label = label
        self.clockwise_cup = None

def init(starting_string, size):

    m = [Cup(0, Cup(0, None)) for x in range(size+1)]
    for i in range(0, len(starting_string)):
        v = int(starting_string[i])
        m[v].label = v
    
    for i in range(0, len(starting_string)-1):
        v = int(starting_string[i])
        w = int(starting_string[i+1])
        m[v].clockwise_cup = m[w]
    
    last_int = int(starting_string[-1])
    first = int(starting_string[0])
    biggest = max([int(x) for x in starting_string] )

    last = Cup(biggest+1, None)
    m[last_int].clockwise_cup = last
    m[biggest+1] = last
    for i in range(biggest+1, size):
        next_cup = m[i+1]
        last.clockwise_cup = next_cup
        next_cup.label = i+1
        last = next_cup
    m[size].clockwise_cup = m[first]

    return (m, size, m[first])

def move(m, biggest, current, times):
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
    for zzz in range(times):
        c1 = current.clockwise_cup
        c2 = c1.clockwise_cup
        c3 = c2.clockwise_cup
        c4 = c3.clockwise_cup
        current.clockwise_cup = c4
        result = c4
        destination = current.label - 1
        while destination == c1.label or destination == c2.label or destination == c3.label:
            destination -= 1
        
        if destination <= 0:
            destination = biggest
        at_destination = m[destination]
        c3.clockwise_cup = at_destination.clockwise_cup
        at_destination.clockwise_cup = c1
        current = result
    return result

@utils.timed
def test_day_twenty_three():
    starting_string = "389125467"
    (m, biggest, cur) = init(starting_string, 1_000_000)
    
    cur = move(m, biggest, cur, 10_000_000)

    one = m[1]
    first = one.clockwise_cup
    second = first.clockwise_cup

    print(first.label, second.label, first.label*second.label)
    
@utils.timed
def day_twenty_three():
    starting_string = "123487596"
    (m, biggest, cur) = init(starting_string, 1_000_000)
    cur = move(m, biggest, cur, 10_000_000)

    one = m[1]
    first = one.clockwise_cup
    second = first.clockwise_cup

    print(first.label, second.label, first.label*second.label)

if __name__=="__main__":
    test_day_twenty_three()
    day_twenty_three()