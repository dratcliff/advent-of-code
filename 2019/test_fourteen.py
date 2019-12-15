from textwrap import dedent
from copy import copy
from math import ceil, floor
import test_one

class Chemical():
    def __str__(self):
        return self.sym + str(self.quant)
    def __repr__(self):
        return self.sym + str(self.quant)
    def __init__(self, representation=None, symbol=None, quantity=None, extra=None):
        self.extra = extra
        if symbol and (quantity != None):
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
        # print('line is', line)
        s = line.split('=>')
        right = s[1].lstrip()
        c = Chemical(representation=right)
        left = [Chemical(representation=x) for x in s[0].split(', ')]
        
        lookup_table[c] = left
    return lookup_table

def find_em(table, root, accum):
    a = accum
    for k, v in table.items():
        if k.sym == root.sym:
            # for j in v:
                # if j.sym == 'ORE':
                    # print('j is', j)
                    # a.append(root)
            for j in v:
                if j.sym != 'ORE':
                    a.append(j)
    return a

def aggregate_em(input):
    aggr = {}
    for r in input:
        if r.sym not in aggr:
            aggr[r.sym] = (r.quant, 0)
        else:
            aggr[r.sym] = (aggr[r.sym][0]+r.quant, aggr[r.sym][1])
        if r.extra:
            # print("extra", r, r.extra)
            aggr[r.sym] = (aggr[r.sym][0], aggr[r.sym][1]+r.extra)
    return aggr

def how_much_ore(aggr, lookup_table):
    s = 0
    remaining = len(aggr)
    while remaining != 0:
        for k, v in aggr.items():
            if v > 0:
                for j, w in lookup_table.items():
                    if k == j.sym:
                        # print(k, j, w)
                        ore = w[0]
                        s += ore.quant
                        aggr[k] -= j.quant
                        if aggr[k] <= 0:
                            remaining -= 1                    
    return s

def is_prime(chemical, lookup_table):
    for k, v in lookup_table.items():
        if len(v) == 1 and v[0].sym == 'ORE' and k.sym == chemical.sym:
            return True
    return False

def get_inputs(chemical, lookup_table, extras):
    for k, v in lookup_table.items():
        if k.sym == chemical.sym:
            required = ceil(chemical.quant/k.quant)
            # print('NEED', chemical.sym, chemical.quant, 'COMES IN:', k.sym, k.quant, v, required)
            return [Chemical(symbol=a.sym, quantity=a.quant*required, extra=(required*k.quant)-chemical.quant) for a in v]

def find_ore_req2(input):
    input_lines = input
    lookup_table = get_requirements(input_lines)
    req = lookup_table[Chemical(symbol='FUEL', quantity=1)]
    # print('req is', req)
    all_prime = False
    while not all_prime:
        inputs = []
        not_primes = [r for r in req if not is_prime(r, lookup_table)]
        # print('not primes', not_primes)
        for n in not_primes:
            inputs = inputs + get_inputs(n, lookup_table)
            # print('inputs', inputs)
        if len(not_primes) == 0:
            all_prime = True
            break
        primes = [r for r in req if is_prime(r, lookup_table)]
        req = primes + inputs
        a = aggregate_em(req)
        req2 = []
        for k, v in a.items():
            req2.append(Chemical(symbol=k, quantity=v[0], extra=v[1]))
        req = req2
        # for r in req:
        #     if not is_prime(r, lookup_table):
        #         print('not prime', r)
        #         req.remove(r)
        #         print('req is now', req)
        #         inputs = inputs + get_inputs(r, lookup_table)
        #         all_prime = False
        #     else:
        #         print('prime', r)
    # req = req + inputs
        # print('req is', req)
    aggr = aggregate_em(req)
    count = 0
    for k, v in aggr.items():
        for j, u in lookup_table.items():
            if j.sym == k:
                print(j.sym, j.quant, u, k, v[0], ceil(v[0]/j.quant))
                count += u[0].quant * ceil(v[0]/j.quant)
    # print('count is', count)
    return count
    # result = find_em(lookup_table, Chemical(symbol='FUEL', quantity=1), [])
    # print("result is", result)
    # remaining = True
    # while remaining:
    #     remaining = False
    #     more = []
    #     for k in result:
    #         more = find_em(lookup_table, k, [])
    #         if len(more) > 0:
    #             result.remove(k)
    #             print("more is", more)
    #             for i in range(0, k.quant):
    #                 result = result + more
    #             remaining = True
    #     print("result is", result)
        
    # print('result is', result)
    # aggr = aggregate_em(result)
    # print('aggr is', aggr)
    # return how_much_ore(aggr, lookup_table)

def buy_chemical(chemical, lookup_table, inventory):
    # print('buying', chemical)
    if chemical.sym in inventory:
        needed = chemical.quant - inventory[chemical.sym]
        inventory[chemical.sym] = 0
        chemical = Chemical(symbol=chemical.sym, quantity=needed)
        # print('really need', chemical)
    for k, v in lookup_table.items():
        if k.sym == chemical.sym:
            required = ceil(chemical.quant/k.quant)
            to_spend = [Chemical(symbol=a.sym, quantity=a.quant*required, extra=(required*k.quant)-chemical.quant) for a in v]
            spent = []
            for t in to_spend:
                if t.sym in inventory:
                    if inventory[t.sym] >= t.quant:
                        inventory[t.sym] -= t.quant
                    else:
                        spent.append(t)
                else:
                    spent.append(t)
            # print('to_spend', to_spend, 'inventory', inventory, 'spent', spent)
            leftover = k.quant*required-chemical.quant
            # print('leftover', chemical, leftover)
            i = Chemical(symbol=k.sym, quantity=leftover)
            if k.sym not in inventory:
                inventory[k.sym] = leftover
            else:
                inventory[k.sym] += leftover
            return spent

def find_ore_req(input, fuel_quantity, inventory={}):
    input_lines = input
    lookup_table = get_requirements(input_lines)
    req = lookup_table[Chemical(symbol='FUEL', quantity=1)]
    scaled_req = [Chemical(symbol=x.sym, quantity=x.quant*fuel_quantity) for x in req]
    print('req is', scaled_req)
    spent = []
    for r in scaled_req:
        s = buy_chemical(r, lookup_table, inventory)
        for x in s:
            spent.append(x)
    collapsed_spent = {}
    for s in spent:
        if s.sym not in collapsed_spent:
            collapsed_spent[s.sym] = s.quant
        else:
            collapsed_spent[s.sym] += s.quant
    new_spent = []
    for k, v in collapsed_spent.items():
        new_spent.append(Chemical(symbol=k, quantity=v))
    spent = new_spent
    # print(inventory, spent)
    for x in spent:
        if x.sym != 'ORE':
            s = buy_chemical(x, lookup_table, inventory)
            for x in s:
                spent.append(x)
    # print(inventory, spent)
    sum = 0
    for i in spent:
        if i.sym == 'ORE':
            sum += i.quant

    for k, v in inventory.items():
        for j, w in lookup_table.items():
            if j.sym == k:
                if len(w) == 1 and w[0].sym == 'ORE':
                    # print("hi", k, v, j, w)
                    if v >= j.quant:
                        sum -= w[0].quant
    return (sum, inventory)

def test_part_one():
    input = """10 ORE => 10 A
    1 ORE => 1 B
    7 A, 1 B => 1 C
    7 A, 1 C => 1 D
    7 A, 1 D => 1 E
    7 A, 1 E => 1 FUEL"""
    input = [dedent(x) for x in input.splitlines()]
    ores = 1000000000000
    out = find_ore_req(input, 1)[0]
    print('out is', out, 'fuel is')
    assert 31 == out

def test_part_one_two():
    input = """9 ORE => 2 A
    8 ORE => 3 B
    7 ORE => 5 C
    3 A, 4 B => 1 AB
    5 B, 7 C => 1 BC
    4 C, 1 A => 1 CA
    2 AB, 3 BC, 4 CA => 1 FUEL"""
    input = [dedent(x) for x in input.splitlines()]
    out = find_ore_req(input, 1)
    print("out is", out)
    assert 165 == out

def test_part_one_three():
    input = """157 ORE => 5 NZVS
    165 ORE => 6 DCFZ
    44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
    12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
    179 ORE => 7 PSHF
    177 ORE => 5 HKGWZ
    7 DCFZ, 7 PSHF => 2 XJWVT
    165 ORE => 2 GPVTF
    3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT"""
    input = [dedent(x) for x in input.splitlines()]
    out = find_ore_req(input, 82892753)
    print("out is", out)
    assert 13312 == out

def test_part_one_four():
    input = """2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG
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
    input = [dedent(x) for x in input.splitlines()]
    out = find_ore_req(input, 558602)
    print("out is", out)
    assert 180697 == out

def test_part_one_five():
    input = """171 ORE => 8 CNZTR
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
    input = [dedent(x) for x in input.splitlines()]
    out = find_ore_req(input, 460664)
    print("out is", out)
    assert 2210736 == out

# test_part_one()
# test_part_one_two()
# test_part_one_three()
# test_part_one_four()
# test_part_one_five()

lines = test_one.getLines("14.txt", to_int=False)
target = 1000000000000
guess = 6216589
low_guess = 1
high_guess = 100000000
out = find_ore_req(lines, guess)[0]
# for i in range(0, 200):
#     if out < target:
#         low_guess = guess
#         guess = int((low_guess + high_guess) / 2)
#         out = find_ore_req(lines, guess)[0]

#     elif out > target:
#         high_guess = guess
#         guess = int((low_guess + high_guess) / 2)
#         out = find_ore_req(lines, guess)[0]
    
#     print(i)

print('out is', out, 'guess is', guess)
