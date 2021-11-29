from utils.utils import file_to_int_list

def parse(filename):
    entries = set()
    with open(filename, "r") as f:
        for line in f:
            entries.add(int(line))
    return entries

def find(entries, desired_sum):
    for e in entries:
        f = desired_sum - e
        if f in entries:
            return e*f
    raise Exception

def test():
    entries = parse("Day1sample.txt")
    answer = find(entries, 2020)
    assert answer == 514579

def test_part_two():
    entries = parse("Day1sample.txt")
    answer = 0
    for e in entries:
        try:
            answer = e * find(entries, 2020-e)
            break
        except Exception as e:
            pass
    assert answer == 241861950

def run():
    entries = file_to_int_list("Day1.txt")
    answer = find(entries, 2020)
    print(answer)

def run_part_two():
    entries = parse("Day1.txt")
    answer = 0
    for e in entries:
        try:
            answer = e * find(entries, 2020-e)
            break
        except Exception as e:
            pass
    print(answer)

def day_one():
    test()
    run()

def day_one_part_two():
    test_part_two()
    run_part_two()

if __name__=="__main__":
    day_one_part_two()