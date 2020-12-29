import json



def walk_dict(j):
    all_values = []
    red = False
    for k, v in j.items():
        if isinstance(v, list):
            all_values.extend(walk(v))
        elif isinstance(v, dict):
            all_values.extend(walk_dict(v))
        else:
            if v == "red":
                red = True
            else:
                all_values.append(v)
    if red:
        return []
    else:
        return all_values


def walk(j):
    all_values = []
    if isinstance(j, dict):
        all_values.extend(walk_dict(j))
    elif isinstance(j, list):
        for i in j:
            all_values.extend(walk(i))
    else:
        all_values.append(j)
    return all_values

def day_twelve():
    objs = [json.loads(line) for line in open("Day12.txt")]
    
    all_values = walk(objs)
    c = sum(x for x in all_values if isinstance(x, int))
    print(c)
    

if __name__=="__main__":
    day_twelve()