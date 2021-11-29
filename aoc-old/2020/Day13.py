def parse(filename):
    m = {}
    with open(filename) as f:
        lines = f.readlines()
        m["estimate"] = int(lines[0])
        schedule = lines[1].replace("x,", "")
        schedule = schedule.split(",")
        schedule = [int(x) for x in schedule]
        m["schedule"] = schedule
    return m

def run(m):
    e = m["estimate"]
    s = m["schedule"]
    waits = {}
    for b in s:
        i = e // b
        first_after = (i+1) * b
        wait = first_after - e
        waits[wait] = b
    min_wait = min(waits.keys())
    return (waits[min_wait], min_wait)

def test_day_thirteen():
    m = parse("Day13sample.txt")
    ans = run(m)
    assert 295 == ans[0]*ans[1]

def day_thirteen():
    m = parse("Day13.txt")
    ans = run(m)
    print(ans[0]*ans[1])

if __name__=="__main__":
    test_day_thirteen()
    day_thirteen()