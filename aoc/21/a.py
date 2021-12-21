"""
1
11 12 13
111 112 113 121 122 123 131 132 133

2
21 22 23
211 212 213 221 222 223 231 232 233

3
31 32 33
311 312 313 321 322 323 331 332 333

27
3 1
4 3
5 6
6 7
7 6
8 3
9 1

could've been smarter about this, but oh well
"""
roll_frequencies = {
    3: 1,
    4: 3,
    5: 6,
    6: 7,
    7: 6,
    8: 3,
    9: 1
}

# i was trying to get a guess for what the worst-case scenario was memory-wise
# r p s
# 7 1 1
# 3 4 5
# 7 1 6
# 3 4 10
# 7 1 11
# 3 4 15
# 7 1 16
# 3 4 20
# 7 1 21



class Game:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.p1_score = 0
        self.p2_score = 0
        self.turn = 1
        self.rolls = []
        self.next_roll = None

rolls = list(range(3, 10))

from collections import deque

# this little manuever costs 18gb of RAM
# i should've figured out how to do it recursively, 
# but i couldn't keep it straight without making a game
# class and a queue
# i think if i kept the total running instead of waiting until
# p1 won, it would work, but i don't care enough to fix it
def run(p1a, p2a):
    total = 0
    d = deque()
    for roll in rolls:
        g = Game(p1a, p2a)
        g.next_roll = roll
        d.append(g)
    while d:
        game = d.popleft()
        p1_score = game.p1_score
        p2_score = game.p2_score
        p1 = game.p1
        p2 = game.p2
        roll2 = game.next_roll
        game.rolls.append(roll2)
        turn = game.turn
        if turn == 1:
            p1 += roll2
            if p1 > 10: 
                p1 = p1 % 10
                if p1 == 0:
                    p1 = 10
            p1_score += p1
            if p1_score >= 21:
                roll_occurs = 1
                for i in range(0, len(game.rolls)):
                    v = game.rolls[i]
                    roll_occurs *= roll_frequencies[v]
                total += roll_occurs
            else:
                for r in rolls:
                    g1 = Game(p1, p2)
                    g1.p1_score = p1_score
                    g1.p2_score = p2_score
                    g1.turn = game.turn * -1
                    g1.rolls = list(game.rolls)
                    g1.next_roll = r
                    d.append(g1)
        else:
            p2 += roll2
            if p2 > 10: 
                p2 = p2 % 10
                if p2 == 0:
                    p2 = 10
            p2_score += p2
            if p2_score >= 21:
                continue
            else:
                for r in rolls:
                    g1 = Game(p1, p2)
                    g1.p1_score = p1_score
                    g1.p2_score = p2_score
                    g1.turn = game.turn * -1
                    g1.rolls = list(game.rolls)
                    g1.next_roll = r
                    d.append(g1)
    return total

def play(p1, p2):
    p1_score = 0
    p2_score = 0
    roll = (1, 2, 3)
    i = 1
    ct = 0
    while p1_score <= 1000 and p2_score <= 1000:
        s = sum(roll)
        ct += 3
        if i > 0:
            p1 += s
            if p1 > 10: 
                p1 = p1 % 10
                if p1 == 0:
                    p1 = 10
            p1_score += p1
            if p1_score >= 1000:
                break
        else:
            p2 += s
            if p2 > 10:
                p2 = p2 % 10
                if p2 == 0:
                    p2 = 10
            p2_score += p2
            if p2_score >= 1000:
                break
        i *= -1
        roll = (roll[0]+3, roll[1]+3, roll[2]+3)
        if roll[0] > 100:
            roll = (roll[0] - 100, roll[1], roll[2])
        if roll[1] > 100:
            roll = (roll[0], roll[1]-100, roll[2])
        if roll[2] > 100:
            roll = (roll[0], roll[1], roll[2]-100)
        
    print(p2_score*ct)
    

play(4, 8)

# takes forever
#g = run(4,8)
#print(g)
