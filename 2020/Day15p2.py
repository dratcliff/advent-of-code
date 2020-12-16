from utils import timed

class Sequence:
    def __init__(self, initial, max_size):
        self.initial = initial
        self.length = len(initial)
        lookup = [-1] * max_size
        for i in range(0, self.length-1):
            lookup[initial[i]] = i + 1
        self.lookup = lookup
        self.last = self.initial[self.length-1]

    def generate_until(self, limit):
        length = self.length
        lookup = self.lookup
        last = self.last
        while length < limit:
            """So, after the starting numbers, each turn results in that player speaking aloud either 0 (if the last number is new) or an age (if the last number is a repeat)."""
            if lookup[last] != -1:
                diff = length - lookup[last]
                n = diff
            else:
                n = 0
            lookup[last] = length
            last = n
            length += 1
        self.lookup = lookup
        self.last = last
        self.length = length

        return last

@timed
def test_day_fifteen():
    seq = [0, 3, 6]
    g = Sequence(seq, 2020)
    n = g.generate_until(2020)
    assert n == 436

@timed
def day_fifteen():
    seq = [2,0,6,12,1,3]
    g = Sequence(seq, 2020)
    n = g.generate_until(2020)
    assert n == 1428

@timed
def day_fifteen_part_two():
    seq = [2,0,6,12,1,3]
    g = Sequence(seq, 30000000)
    n = g.generate_until(30000000)
    assert n == 3718541

if __name__=="__main__":
    test_day_fifteen()
    day_fifteen()
    day_fifteen_part_two()