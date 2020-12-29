from itertools import permutations

weapons = [
    ('Dagger',        8,     4,       0),
    ('Shortsword',   10,     5,       0),
    ('Warhammer',    25,     6,       0),
    ('Longsword',    40,     7,       0),
    ('Greataxe',     74,     8,       0)
]

armor = [
    ('None',         0,      0,       0),
    ('Leather',      13,     0,       1),
    ('Chainmail',    31,     0,       2),
    ('Splintmail',   53,     0,       3),
    ('Bandedmail',   75,     0,       4),
    ('Platemail',   102,     0,       5),
]

rings = [
    ('None',         0,      0,       0),
    ('None',         0,      0,       0),
    ('Damage +1',    25,     1,       0),
    ('Damage +2',    50,     2,       0),
    ('Damage +3',   100,     3,       0),
    ('Defense +1',   20,     0,       1),
    ('Defense +2',   40,     0,       2),
    ('Defense +3',   80,     0,       3)
]

def who_wins(me_hp, me_armor, me_dmg, boss_hp, boss_armor, boss_dmg):
    me_net_loss = max(boss_dmg - me_armor, 1)
    boss_net_loss = max(me_dmg - boss_armor, 1)

    while me_hp > 0 and boss_hp > 0:
        boss_hp -= boss_net_loss
        if boss_hp <= 0:
            return "me"
        me_hp -= me_net_loss
        if me_hp <= 0:
            return "boss"

def run():
    min_winning_cost = 100000
    max_losing_cost = 0
    for w in weapons:
        for a in armor:
            for r in permutations(rings, 2):
                me_hp = 100
                me_armor = a[3] + r[0][3] + r[1][3]
                me_dmg = w[2] + r[0][2] + r[1][2]
                winner = who_wins(me_hp, me_armor, me_dmg, 103, 2, 9)
                cost = a[1] + w[1] + r[0][1] + r[1][1]
                if winner == "me":
                    if cost < min_winning_cost:
                        min_winning_cost = cost
                else:
                    if cost > max_losing_cost:
                        max_losing_cost = cost
    print("Min winning cost", min_winning_cost)
    print("Max losing cost", max_losing_cost)

def test_day_twenty_one():
    winner = who_wins(8, 5, 5, 12, 7, 2)
    print(winner)
    run()

if __name__=="__main__":
    test_day_twenty_one()