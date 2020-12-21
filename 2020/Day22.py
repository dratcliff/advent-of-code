import utils

def run(entries):
    for e in entries:
        print(e)

def test_day_twenty_one():
    entries = utils.file_to_string_list("Day21sample.txt")
    run(entries)

def day_twenty_one():
    entries = utils.file_to_string_list("Day21.txt")
    run(entries)