import utils

entries = utils.file_to_string_list("Day15.txt")
test_entries = utils.file_to_string_list("Day15sample.txt")

def next(n):
    """So, after the starting numbers, each turn results in that player speaking aloud either 0 (if the last number is new) or an age (if the last number is a repeat)."""
    last = n[-1]
    count = sum(1 for x in n if x == last)
    if count == 1:
        n.append(0)
        return n
    prev = -1
    prev2 = -1
    for i in range(len(n)-1, -1, -1):
        if n[i] == last:
            if prev == -1:
                prev = i
            elif prev2 == -1:
                prev2 = i
            else:
                break
            
    n.append(prev-prev2)
    return n
    

def test_day_fifteen():
    n = [2,0,6,12,1,3]
    index = 2020
    for i in range(0, index):
        n = next(n)
    print(n[index-1])

def day_fifteen():
    pass
    # print(entries)


if __name__=="__main__":
    test_day_fifteen()
    day_fifteen()