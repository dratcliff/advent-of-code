from collections import deque
from test_one import getLines

def shuf(deck, cmd_text):
    if cmd_text == "deal into new stack":
        deck.reverse()
        return deck
    if cmd_text.startswith("cut"):
        how_many = int(cmd_text.split(" ")[1]) * -1
        deck.rotate(how_many)
        return deck
    if cmd_text.startswith("deal with increment"):
        incr = int(cmd_text.split(" ")[3])
        new_deck = [None] * len(deck)
        i = 0
        while len(deck) > 0:
            g = deck.popleft()
            new_deck[i] = g
            i = i + incr
            if i > len(new_deck):
                i = i - len(new_deck)
        return deque(new_deck)

def shuf2(front_back, cmd_text, length):
    front = front_back[0]
    back = front_back[1]
    # print(len(front), len(back), cmd_text)
    if cmd_text == "deal into new stack":
        front.reverse()
        back.reverse()
        front, back = back, front
        return (front, back)
    if cmd_text.startswith("cut"):
        how_many = int(cmd_text.split(" ")[1])
        if how_many > 0:
            back = back + front[:how_many]
            front = front[how_many:]
        else:
            front = back[how_many:] + front
            back = back[:how_many]
        return (front, back)
    if cmd_text.startswith("deal with increment"):
        incr = int(cmd_text.split(" ")[3])
        new_front = [None] * len(front)
        for i, v in enumerate(front):
            if i*incr % length < len(front):
                new_front[i] = front[i*incr % length]
        new_back = [None] * len(back)
        for i, v in enumerate(back):
            if i*incr * length < len(back):
                new_back[i] = back[i*incr % length]
        
        deck = front + back
        return (front, back)

def new_deck(length):
    deck = deque(range(length))
    return deck

i = new_deck(10)
i = shuf(i, "deal into new stack")
print(i)

i = new_deck(10)
i = shuf(i, "cut -3")
print(i)

i = new_deck(10)
i = shuf(i, "deal with increment 3")
print(i)

def part_one():
    text = getLines("resources/22.txt", to_int=False)
    deck = new_deck(10007)
#     text = """
# deal with increment 7
# deal with increment 9
# cut -2""".splitlines()[1:]
#     text = """
# deal into new stack
# cut -2
# deal with increment 7
# cut 8
# cut -4
# deal with increment 7
# cut 3
# deal with increment 9
# deal with increment 3
# cut -1""".splitlines()[1:]
    # deck = new_deck(10)
    for i in range(0, 2)
        for t in text:
            deck = shuf(deck, t)
        for k, v in enumerate(deck):
            if i == 2019:
                print(k)

def part_two():
    text = getLines("resources/22.txt", to_int=False)
    # front = list(range(0, 100000))
    # back = list(range(119315717514047-100000, 119315717514047))
    front = list(range(0, 400000))
    back = list(range(119315717514047-400000, 119315717514047))
#     text = """
# deal with increment 7
# deal with increment 9
# cut -2""".splitlines()[1:]
#     text = """
# deal into new stack
# cut -2
# deal with increment 7
# cut 8
# cut -4
# deal with increment 7
# cut 3
# deal with increment 9
# deal with increment 3
# cut -1""".splitlines()[1:]
    # deck = new_deck(10)
    deck = (front, back)
    last = 0
    for i in range(0, 10):
        for t in text:
            deck = shuf2(deck, t, 10011931571751404707)
        for i, v in enumerate(deck[0]):
            if i == 2020:
                print(last - v)
                last = v
part_two()