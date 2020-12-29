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
            masks[cur].append((e[0], int(e[1])))
            mem[e[0]] = zero
    #print(len(masks))
    #mem value = 2nd 
    #print(len(mem))

    mask1 = list(masks.keys())[0]
    mem1 = masks[mask1][0]
    #max in file = 947441529
    max_in_file = bin(947441529)[2:]
    #print(max_in_file.zfill(36))
    #print(mask1, mem1, bin(mem1[1]))
    for k, v in masks.items():
        for address, value in v:
            print(k, address, value)
            mask = k
            value = to_binary(value)
            masked = apply_mask(value, mask)
            mem[address] = masked
            print(k, address, masked)

    s = 0
    for address in mem:
        s += int(mem[address], 2)

    print(s)

def to_binary(i):
    return bin(i)[2:].zfill(36)

def apply_mask(value, mask):
    value = list(value)
    mask = list(mask)
    for i in range(0, len(mask)):
        if mask[i] in ("0", "1"):
            value[i] = mask[i]
    return ''.join(value)

def day_fourteen():
    pass

if __name__=="__main__":
    val = apply_mask("000000000000000000000000000000001011", "XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X")
    assert "000000000000000000000000000001001001" == val
    test_day_fourteen()
    #day_fourteen()