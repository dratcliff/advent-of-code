import utils

masks = {}
mem = {}
zero = ""
for i in range(0, 36):
    zero += "0"

def test_day_fourteen():
    entries = utils.file_to_string_list("day14a.txt")
    cur = ""
    for e in entries:
        e = e.split(" = ")
        if "mask" == e[0]:
            cur = e[1]
            masks[cur] = []
        else:
            masks[cur].append((int(e[1]), int(e[0])))
            mem[e[0]] = zero


    mask1 = list(masks.keys())[0]
    mem1 = masks[mask1][0]

    max_in_file = bin(947441529)[2:]
    for k, v in masks.items():
        for value, address in v:
            mask = k
            address = to_binary(address)
            masked = apply_mask(address, mask)
            addresses = apply_floating(masked)
            for a in addresses:
                i = int(a, 2)
                mem[a] = to_binary(value)

    s = 0
    for address in mem:
            s += int(mem[address], 2)

    print(s)

def to_binary(i):
    return bin(i)[2:].zfill(36)

def apply_floating(masked):
    # print(masked)
    maskeds = [masked]
    done = False
    while not done:
        for x in maskeds:
            for i, v in enumerate(x):
                if v == "X":
                    maskeds.remove(x)
                    x = list(x)
                    y = list(x)
                    x[i] = "0"
                    y[i] = "1"
                    maskeds.append(''.join(x))
                    maskeds.append(''.join(y))
                    break
        done = True
        for x in maskeds:
            done = done and ("X" not in x)
    return maskeds


def apply_mask(value, mask):
    value = list(value)
    mask = list(mask)
    for i in range(0, len(mask)):
        if mask[i] in ("X", "1"):
            value[i] = mask[i]
    return ''.join(value)

def day_fourteen():
    pass

if __name__=="__main__":
    val = apply_mask("000000000000000000000000000000101010", "000000000000000000000000000000X1001X")
    assert "000000000000000000000000000000X1101X" == val
    val = apply_floating("000000000000000000000000000000X1101X")

    test_day_fourteen()
    #day_fourteen()