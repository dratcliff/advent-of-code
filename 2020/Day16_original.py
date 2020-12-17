import utils


def test_day_sixteen():
    all_valid = {}
    all_valid2 = set()
    all_invalid = []
    maybe_valid_tickets = []
    your = utils.file_to_string_list("Day16your.txt")
    nearby = utils.file_to_string_list("Day16nearby.txt")
    fields = utils.file_to_string_list("Day16fields.txt")
    for f in fields:
        f = f.split(" ")
        key = f[0]
        f = [f[1], f[3]]
        
        key = key.replace(":", "")
        all_valid_v = set()
        for g in f:
            g = g.split("-")
            for i in range(int(g[0]), int(g[1])+1):
                all_valid_v.add(i)
                all_valid2.add(i)
        all_valid[key] = all_valid_v
            

    for g in nearby:
        g = g.split(",")
        valid = True
        for i, h in enumerate(g):
            if int(h) not in all_valid2:
                all_invalid.append(int(h))
                valid = False
        if valid:    
            maybe_valid_tickets.append(g)

    # print(maybe_valid_tickets)
    # print(all_valid)

    field_map = {}

    for m in maybe_valid_tickets:
        for i, n in enumerate(m):
            if i not in field_map:
                field_map[i] = set()
            field_map[i].add(int(n))
            
    # print(field_map)

    actual_fm = {}

    for k, v in field_map.items():
        for k1, v1 in all_valid.items():
            if v < v1:
                if k not in actual_fm:
                    actual_fm[k] = set()
                actual_fm[k].add(k1)
    
    print(actual_fm)

    for k, v in actual_fm.items():
        for v1 in v:
            if "departure" in v1:
                print(k, v1, "!!!")

    what = {}

    for i in range(0, 20):
        for k, v in actual_fm.items():
            what[k] = v
        for j in range(0, 20):
            if i != j and i in what and j in actual_fm:
                what[i] = what[i] - actual_fm[j]
        for z in what:
            if len(what[z]) == 1:
                for y in what.values():
                    if y != what[z]:
                        the_key = list(what[z])[0]
                        if the_key in y:
                            y.remove(the_key)

    departures = {}
    for k, v in actual_fm.items():
        for v1 in v:
            if "departure" in v1:
                # print(k, v1, "!!!")
                if v1 not in departures:
                    departures[v1] = set()
                departures[v1].add(k)
    # print(departures)

    print(what)
    # print(actual_fm[6])

def day_sixteen():
    your = utils.file_to_string_list("Day16your.txt")
    your = your[0]
    your = your.split(",")
    your = [int(y) for y in your]
    s = your[1]*your[2]*your[12]*your[15]*your[16]*your[17]
    print(s)


if __name__=="__main__":
    # test_day_sixteen()
    day_sixteen()