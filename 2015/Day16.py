import sys

sys.path.append("../2020")

import utils

wrapping_sue = {
    "children": 3,
    "cats": 7,
    "samoyeds": 2,
    "pomeranians": 3,
    "akitas": 0,
    "vizslas": 0,
    "goldfish": 5,
    "trees": 3,
    "cars": 2,
    "perfumes": 1,
}

def day_sixteen():
    entries = utils.file_to_string_list("Day16.txt")
    entries = [e.split(" ") for e in entries]
    sues = {}
    
    for e in entries:
        s = int(e[1].replace(":", ""))
        e = e[2:]
        sue = {}
        for i in range(0, len(e)-1, 2):
            k = e[i].replace(":", "")
            v = int(e[i+1].replace(",", ""))
            sue[k] = v
        sues[s] = sue

    
    for k, v in sues.items():
        real_sue = True
        for k1, v1 in v.items():
            if k1 in wrapping_sue:
                wv = wrapping_sue[k1]
                # print(k1, v1, wv)
                if k1 in ["cats", "trees"]:
                    if v1 <= wv:
                        real_sue = False
                elif k1 in ["pomeranians", "goldfish"]:
                    if v1 >= wv:
                        real_sue = False
                else:
                    if v1 != wv:
                        real_sue = False
        if real_sue:
            print(k, v)

if __name__=="__main__":
    day_sixteen()