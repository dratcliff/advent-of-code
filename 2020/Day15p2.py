import utils

entries = utils.file_to_string_list("Day15.txt")
test_entries = utils.file_to_string_list("Day15sample.txt")

last2 = {}
def next(so_far, last, length):
    """So, after the starting numbers, each turn results in that player speaking aloud either 0 (if the last number is new) or an age (if the last number is a repeat)."""
    if len(so_far[last]) == 1:
        so_far[0].append(length+1)
        last = 0
    else:
        last2 = so_far[last][-2:]
        diff = last2[1]-last2[0]
        if diff in so_far:
            so_far[diff].append(length+1)
        else:
            so_far[diff] = [length+1]
        last = diff
    return (so_far, last, length+1)
    

def test_day_fifteen():
    #2,0,6,12,1,3
    n = {
        2: [1],
        0: [2],
        6: [3],
        12: [4],
        1: [5],
        3: [6]
    }
    so_far, last, length = next(n, 3, 6)
    for i in range(0, 30000000):
        if i % 30000000 == 0:
            print(i)
        so_far, last, length = next(so_far, last, length)
    
    for k, v in so_far.items():
        if 30000000 in v:
            print(k, v)

def day_fifteen():
    pass
    # print(entries)


if __name__=="__main__":
    test_day_fifteen()
    day_fifteen()