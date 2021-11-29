class BoardingPass:
    def __init__(self, row, column, seat):
        self.row = row
        self.column = column
        self.seat = seat

def parse(filename):
    entries = []
    with open(filename) as f:
        for line in f:
            entries.append(decode(line))
    return entries

def get_row(r):
    hi = 127
    low = 0
    for i in r:
        if i == "B":
            low = (hi + low + 1) // 2
        else:
            hi = (hi + low) // 2
    if r[-1:] == "B":
        return hi
    return low

def get_column(c):
    hi = 7
    low = 0
    for i in c:
        if i == "R":
            low = (hi + low + 1) // 2
        else:
            hi = (hi + low) // 2
    if c[-1:] == "R":
        return hi
    return low

def get_seat(c, r):
    return r*8 + c

def decode(bp):
    row = bp[:7]
    col = bp[7:]
    r = get_row(row)
    c = get_column(col)
    s = get_seat(c, r)
    return BoardingPass(r, c, s)

def test_day_five():
    entries = parse("Day5sample.txt")
    hi = max(entries, key=lambda x: x.seat)
    assert 820 == hi.seat
    
def day_five():
    entries = parse("Day5.txt")
    hi = max(entries, key=lambda x: x.seat)
    assert 826 == hi.seat

def day_five_part_two():
    entries = parse("Day5.txt")
    low = min(entries, key=lambda x: x.seat).seat
    hi = max(entries, key=lambda x: x.seat).seat
    entries = set([x.seat for x in entries])
    all_seats = set([x for x in range(low, hi+1)])
    for i in entries:
        all_seats.remove(i)

    assert len(all_seats) == 1
    my_seat = next(iter(all_seats))
    assert my_seat == 678
            

if __name__=="__main__":
    test_day_five()
    day_five()
    day_five_part_two()