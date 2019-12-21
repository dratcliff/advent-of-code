import test_one


def get_orbiters(filename):
    lines = test_one.getLines(filename, to_int=False)
    d = dict()
    for line in lines:
        planets = str.split(line, ')')
        orbiter = planets[1]
        orbited = planets[0]
        if orbiter not in d:
            d[orbiter] = orbited
    return d


def part_one(filename):
    sum = 0
    d = get_orbiters(filename)
    for k in d:
        sum = sum + 1
        while d[k] in d:
            sum = sum + 1
            k = d[k]

    return sum


def test_part_one():
    assert part_one('resources/6.txt') == 308790


def get_orbited(filename):
    d1 = dict()
    d = get_orbiters(filename)
    for k in d:
        # print(':::', k, d[k])
        if d[k] not in d1:
            d1[d[k]] = [k]
            # print(d1[d[k]])
        else:
            # print(d1[k])
            d1[d[k]].append(k)
    return d1


def walk_orbits(tree, rootLabel, stopLabel, sum=0):
    if stopLabel in tree[rootLabel]:
        return (rootLabel, sum)
    else:
        for k in tree[rootLabel]:
            if k in tree:
                result = walk_orbits(tree, k, stopLabel, sum=sum+1)
                if result != None:
                    return result


def test_part_two():
    d = get_orbited('resources/6.txt')
    min = len(d)*2
    for k in d:
        y = walk_orbits(d, k, 'YOU')
        s = walk_orbits(d, k, 'SAN')
        if y and s:
            sum = y[1] + s[1]
            # print(sum)
            if sum < min:
                min = sum
                print(min)
    assert min == 472
