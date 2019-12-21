from textwrap import dedent
from math import ceil
import test_one

class Chemical():
    def __str__(self):
        return self.sym + str(self.quant)
    def __repr__(self):
        return self.sym + str(self.quant)
    def __init__(self, representation=None, symbol=None, quantity=None, extra=None):
        self.extra = extra
        if symbol and (quantity is not None):
            self.quant = int(quantity)
            self.sym = symbol
        else:
            components = representation.split(' ')
            self.quant = int(components[0])
            self.sym = components[1]
    def __eq__(self, other):
        return self.quant == other.quant and self.sym == other.sym
    def __hash__(self):
        return hash((self.sym, self.quant))

def get_requirements(input_lines):
    lookup_table = {}
    for line in input_lines:
        split_line = line.split('=>')
        right = split_line[1].lstrip()
        chemical = Chemical(representation=right)
        left = [Chemical(representation=x) for x in split_line[0].split(', ')]
        lookup_table[chemical] = left
    return lookup_table

def buy_chemical(chemical, lookup_table, inventory):
    if chemical.sym in inventory:
        needed = chemical.quant - inventory[chemical.sym]
        inventory[chemical.sym] = 0
        chemical = Chemical(symbol=chemical.sym, quantity=needed)
    for k, chems in lookup_table.items():
        if k.sym == chemical.sym:
            required = ceil(chemical.quant/k.quant)
            to_spend = [Chemical(symbol=a.sym, quantity=a.quant*required,
                                 extra=(required*k.quant)-chemical.quant) for a in chems]
            spent = []
            for chem_to_spend in to_spend:
                if chem_to_spend.sym in inventory:
                    if inventory[chem_to_spend.sym] >= chem_to_spend.quant:
                        inventory[chem_to_spend.sym] -= chem_to_spend.quant
                    else:
                        spent.append(chem_to_spend)
                else:
                    spent.append(chem_to_spend)
            leftover = k.quant*required-chemical.quant
            if k.sym not in inventory:
                inventory[k.sym] = leftover
            else:
                inventory[k.sym] += leftover
    return spent

def find_ore_req(input_lines, fuel_quantity, inventory=None):
    if inventory is None: # if you modify a default argument, its value persists until next call
        inventory = {}
    lookup_table = get_requirements(input_lines)
    req = lookup_table[Chemical(symbol='FUEL', quantity=1)]
    scaled_req = [Chemical(symbol=x.sym, quantity=x.quant*fuel_quantity) for x in req]
    spent = []
    for r in scaled_req:
        bought = buy_chemical(r, lookup_table, inventory)
        for x in bought:
            spent.append(x)
    collapsed_spent = {}
    for bought in spent:
        if bought.sym not in collapsed_spent:
            collapsed_spent[bought.sym] = bought.quant
        else:
            collapsed_spent[bought.sym] += bought.quant
    new_spent = []
    for k, quantity in collapsed_spent.items():
        new_spent.append(Chemical(symbol=k, quantity=quantity))
    spent = new_spent
    ore_sum = spend_ore(spent, lookup_table, inventory)
    ore_sum = remove_unnecessary_ore(inventory, lookup_table, ore_sum)
    return (ore_sum, inventory)

def spend_ore(spent, lookup_table, inventory):
    for chem in spent:
        if chem.sym != 'ORE':
            bought = buy_chemical(chem, lookup_table, inventory)
            for bought_chem in bought:
                spent.append(bought_chem)
    bought = 0
    for chem in spent:
        if chem.sym == 'ORE':
            bought += chem.quant
    return bought

def remove_unnecessary_ore(inventory, lookup_table, total):
    for k, quantity in inventory.items():
        for j, items in lookup_table.items():
            if j.sym == k:
                if len(items) == 1 and items[0].sym == 'ORE':
                    if quantity >= j.quant:
                        total -= items[0].quant
    return total

def test_part_one_one():
    lines = """10 ORE => 10 A
    1 ORE => 1 B
    7 A, 1 B => 1 C
    7 A, 1 C => 1 D
    7 A, 1 D => 1 E
    7 A, 1 E => 1 FUEL"""
    lines = [dedent(x) for x in lines.splitlines()]
    out = find_ore_req(lines, 1)[0]
    assert out == 31

def test_part_one_two():
    lines = """9 ORE => 2 A
    8 ORE => 3 B
    7 ORE => 5 C
    3 A, 4 B => 1 AB
    5 B, 7 C => 1 BC
    4 C, 1 A => 1 CA
    2 AB, 3 BC, 4 CA => 1 FUEL"""
    lines = [dedent(x) for x in lines.splitlines()]
    out = find_ore_req(lines, 1)[0]
    print("out is", out)
    assert out == 165

def test_part_one_three():
    lines = """157 ORE => 5 NZVS
    165 ORE => 6 DCFZ
    44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
    12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
    179 ORE => 7 PSHF
    177 ORE => 5 HKGWZ
    7 DCFZ, 7 PSHF => 2 XJWVT
    165 ORE => 2 GPVTF
    3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT"""
    lines = [dedent(x) for x in lines.splitlines()]
    out = find_ore_req(lines, 1)[0]
    print("out is", out)
    assert out == 13312

def test_part_one_four():
    lines = """2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG
    17 NVRVD, 3 JNWZP => 8 VPVL
    53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL
    22 VJHF, 37 MNCFX => 5 FWMGM
    139 ORE => 4 NVRVD
    144 ORE => 7 JNWZP
    5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC
    5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV
    145 ORE => 6 MNCFX
    1 NVRVD => 8 CXFTF
    1 VJHF, 6 MNCFX => 4 RFSQX
    176 ORE => 6 VJHF"""
    lines = [dedent(x) for x in lines.splitlines()]
    out = find_ore_req(lines, 1)[0]
    print("out is", out)
    assert out == 180697

def test_part_one_five():
    lines = """171 ORE => 8 CNZTR
    7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
    114 ORE => 4 BHXH
    14 VRPVC => 6 BMBT
    6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
    6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
    15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
    13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
    5 BMBT => 4 WPTQ
    189 ORE => 9 KTJDG
    1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
    12 VRPVC, 27 CNZTR => 2 XDBXC
    15 KTJDG, 12 BHXH => 5 XCVML
    3 BHXH, 2 VRPVC => 7 MZWV
    121 ORE => 7 VRPVC
    7 XCVML => 6 RJRHP
    5 BHXH, 4 VRPVC => 5 LTCX"""
    lines = [dedent(x) for x in lines.splitlines()]
    out = find_ore_req(lines, 1)[0]
    print("out is", out)
    assert out == 2210736

def test_part_two():
    lines = test_one.getLines("resources/14.txt", to_int=False)
    target = 1000000000000
    guess = 5000000
    low_guess = 1000000
    high_guess = 10000000
    out = find_ore_req(lines, guess)[0]
    last_high = 0
    last_low = 0
    for _ in range(0, 200):
        if out < target:
            last_low = out
            low_guess = guess
            guess = int((low_guess + high_guess) / 2)
            out = find_ore_req(lines, guess)[0]
        elif out > target:
            last_high = out
            high_guess = guess
            guess = int((low_guess + high_guess) / 2)
            out = find_ore_req(lines, guess)[0]
        if out in (last_high, last_low):
            break
    assert guess == 6216589
