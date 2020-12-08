from utils import timed

class Instruction:
    def __init__(self, instruction, argument):
        self.instruction = instruction
        self.argument = argument
        self.executed = False

def parse(filename):
    instructions = {}
    i = 0
    with open(filename) as f:
        for line in f:
            s = line.split(' ')
            instructions[i] = Instruction(s[0], int(s[1]))
            i += 1
    
    return instructions

def run(instructions):
    counter = 0
    i = 0
    ins = instructions[0]
    while not ins.executed and i < len(instructions):
        if ins.instruction == "nop":
            i += 1
        elif ins.instruction == "jmp":
            i += ins.argument
        elif ins.instruction == "acc":
            counter += ins.argument
            i += 1
        ins.executed = True
        if i < len(instructions):
            ins = instructions[i]
    return (i, counter)

@timed
def test_day_eight():
    instructions = parse("Day8sample.txt")
    ct = run(instructions)
    assert ct[1] == 5

@timed
def day_eight():
    instructions = parse("Day8.txt")
    ct = run(instructions)
    assert ct[1] == 2058

@timed
def day_eight_part_two():
    instructions = parse("Day8.txt")
    ct = (0, 0)
    i = 0
    while ct[0] < len(instructions):
        ins = instructions[i]
        i += 1
        if ins.instruction == "nop":
            ins.instruction = "jmp"
            ct = run(instructions)
            ins.instruction = "nop"
        elif ins.instruction == "jmp":
            ins.instruction = "nop"
            ct = run(instructions)
            ins.instruction = "jmp"
        instructions = parse("Day8.txt")

    assert ct[1] == 1000


if __name__=="__main__":
    test_day_eight()
    day_eight()
    day_eight_part_two()