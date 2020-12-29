import utils.utils as utils

def parse(filename):
    entries = utils.file_to_string_list(filename)
    rules = []
    messages = []
    for e in entries:
        if ":" in e:
            rules.append(e)
        else:
            messages.append(e)
    return (rules, messages)

def to_rule_map(rules):
    m = {}
    for r in rules:
        r = r.split(": ")
        m[r[0]] = list(r[1].split(" | "))
    return m

def rules_to_possibilities(rules):
    possible = set(rules['0'])
    done = False
    complete = set()
    while not done:
        done = True
        next_possible = set()
        for p in possible:
            tokens = p.split(" ")
            for i, original in enumerate(tokens):
                if original != "a" and original != "b" and original != " ":
                    done = False
                if original in rules:
                    for replacement in rules[original]:
                        starting = ""
                        for j in range(0, i):
                            starting += tokens[j]
                            starting += " "
                        starting += replacement + " "
                        for j in range(i+1, len(tokens)):
                            starting += tokens[j]
                            starting += " "
                        starting = starting.rstrip()
                        if len(starting) == starting.count("a") + starting.count("b") + starting.count(" "):
                            complete.add(starting)
                        else:
                            next_possible.add(starting)
        if len(next_possible) == 0:
            done = True
        if len(next_possible) > 0:
            possible = next_possible
            longest = max(possible, key=lambda x:len(x))
            print(len(possible), len(longest), longest)
        no_spaces = set()
        for p in complete:
            no_spaces.add(p.replace(" ", ""))
    return no_spaces

def count_valid(messages, possibilities):
    for m in messages:
        if m in possibilities:
            print("match", m,)
    return sum(1 for m in messages if m in possibilities)

def test_day_nineteen():
    rules, messages = parse("Day19sample.txt")
    rules = to_rule_map(rules)
    possibilities = rules_to_possibilities(rules)
    ct = count_valid(messages, possibilities)
    assert 2 == ct

def day_nineteen():
    rules, messages = parse("Day19.txt")
    rules = to_rule_map(rules)
    for k, v in rules.items():
        print(k, v)
    possibilities = rules_to_possibilities(rules)
    ct = count_valid(messages, possibilities)
    print(ct)

#def day_nineteen():
    # import re
    # rules, messages = parse("day19orig2.txt")
    # rules = to_rule_map(rules)
    # start = rules['0']
    
    # # for i in range(10):
    # while len(re.findall(r'[0-9]+', start)) > 0:
    #     new = ""
    #     cur = 0
    #     for t in [(m.start(0), m.end(0)) for m in re.finditer(r'[0-9]+', start)]:
    #         new += start[cur:t[0]]
    #         key = start[t[0]:t[1]]
    #         replacement = rules[key]
    #         if "|" in replacement:
    #             replacement = "(" + replacement + ")"
    #         new += replacement
    #         cur = t[1]
    #     new += start[cur:]
    #     start = new
        # for m in re.findall(r'[0-9]+', start):
        #     next_rule = rules[m]
        #     if "|" in next_rule:
        #         next_rule = " ( " + next_rule + " ) "
        #     else:
        #         next_rule += " "
        #     new += next_rule
        # start = new
        # print(start)
        # print(start.count("("), start.count(")"))
        
    
    

if __name__=="__main__":
    test_day_nineteen()
    day_nineteen()