def get_presents(house):
    elves = []
    if house == 1:
        return (10, [1])
    if house == 2:
        return (30, [1, 2])
    ans = 0
    for i in range(1, ((house+1)//2)+1):
        if house % i == 0:
            ans += 10*i
            elves.append(i)
    ans += 10*house
    elves.append(house)
    return (ans, elves)

def get_house_map(max_house):
    m = {i: 10 for i in range(0, max_house)}
    for i in range(2, max_house):
        current = i
        for j in range(0, 50):
            if current in m:
                m[current] += 11*i 
            current += i

    return m

def test_day_twenty():
    assert 10 == get_presents(1)[0]
    assert 30 == get_presents(2)[0]
    assert 40 == get_presents(3)[0]
    assert 70 == get_presents(4)[0]
    assert 60 == get_presents(5)[0]
    assert 120 == get_presents(6)[0]
    assert 80 == get_presents(7)[0]
    assert 150 == get_presents(8)[0]
    assert 130 == get_presents(9)[0]

def day_twenty():
    houses = 4
    most = 0
    while most < 33100000:
        houses *= 2
        m = get_house_map(houses)
        most = max(m.values())
    m = {k: v for k, v in m.items() if v >= 33100000}
    print(min(m.keys()))

if __name__=="__main__":
    # test_day_twenty()
    day_twenty()