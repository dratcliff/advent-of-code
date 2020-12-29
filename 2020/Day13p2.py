def parse(filename):
    schedule = {}
    with open(filename) as f:
        lines = f.readlines()
        schedule = lines[1].split(",")
        schedule = {int(k): int(v) for k, v in enumerate(schedule) if v != "x"}
    return schedule

def run1(m):
    estimated_time = m["estimate"]
    sched = m["schedule"]
    waits = {}
    for offset, bus_id in sched.items():
        i = 1
        wait = estimated_time % bus_id
        if wait != 0:
            i = estimated_time // bus_id
            first_after = (i+1) * bus_id
            wait = first_after - estimated_time
        waits[offset] = wait

    matches = set()
    keys = list(waits.keys())
    for i in range(0, len(keys)):
        if waits[keys[i]] != keys[i] % sched[keys[i]]:
            break
        matches.add(i)
    return matches

def run(m):
    e = {}
    e["schedule"] = m
    e["estimate"] = 0

    inc = 1
    matches = run1(e)
    last_matches = set()
    while len(matches) != len(m):
        
        if matches != last_matches:
            last_matches = matches
            keys = list(m.keys())
            
            inc = 1
            for i in matches:
                inc *= m[keys[i]]
        else:
            print(inc)
        e["estimate"] += inc
        matches = run1(e)
    return e["estimate"]

def test_day_thirteen_part_two():
    m = parse("Day13sample2.txt")
    e = run(m)
    assert 1202161486 == e

def day_thirteen_part_two():
    m = parse("Day13.txt")
    e = run(m)
    assert 894954360381385 == e

# test
if __name__=="__main__":
    test_day_thirteen_part_two()
    day_thirteen_part_two()