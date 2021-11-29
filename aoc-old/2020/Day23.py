import utils.utils as utils

class CupCircle:
    def __init__(self, labeling):
        self.arr = []
        for i in range(0, len(labeling)):
            self.arr.append(int(labeling[i]))
        self.size = len(labeling)
        self.current_pos = 0
        self.current_cup = self.arr[self.current_pos]
        self.three = []

    def pick_three(self):
        three = []
        if self.current_pos == self.size - 1:
            three = self.arr[0:3]
            del(self.arr[0:3])
            self.current_pos = len(self.arr)-1
        elif self.current_pos == self.size - 2:
            three.append(self.arr[self.size-1])
            del(self.arr[self.size-1])
            three.extend(self.arr[0:2])
            del(self.arr[0:2])
            self.current_pos = len(self.arr)-1
        elif self.current_pos == self.size - 3:
            three.extend(self.arr[self.size-2:])
            del(self.arr[self.size-2:])
            three.append(self.arr[0])
            del(self.arr[0])
            self.current_pos = len(self.arr)-1
        else:
            three.extend(self.arr[self.current_pos+1:self.current_pos+4])
            del(self.arr[self.current_pos+1:self.current_pos+4])
        self.three = three
        # print("Pick up", self.three)

    def select_destination(self):
        current_label = self.arr[self.current_pos]
        
        destination = None
        lowest_value = min(self.arr)
        highest_value = max(self.arr)
        next_value = current_label
        while destination == None:
            next_value -= 1
            if next_value < lowest_value:
                next_value = highest_value
            for i, v in enumerate(self.arr):
                if v == next_value:
                    destination = i 
        self.destination = destination
        # print("destination index", destination)

    def place_cups(self):
        self.arr.insert(self.destination+1, self.three[2])
        self.arr.insert(self.destination+1, self.three[1])
        self.arr.insert(self.destination+1, self.three[0])
        current_cup_pos = self.arr.index(self.current_cup)
        current_cup_pos += 1
        if current_cup_pos == len(self.arr):
            current_cup_pos = 0
        self.current_pos = current_cup_pos
        self.current_cup = self.arr[self.current_pos]

    def move(self):
        self.pick_three()
        self.select_destination()
        self.place_cups()

    def cups_clockwise_from(self, label):
        cups = []
        li = self.arr.index(label)
        for i in range(0, len(self.arr)-1):
            if li == len(self.arr)-1:
                li = 0
            else:
                li += 1
            cups.append(self.arr[li])
        return cups

def run(entries):
    """
    The crab picks up the three cups that are immediately clockwise of the current cup. 
    They are removed from the circle; cup spacing is adjusted as necessary to maintain the circle.

    The crab selects a destination cup: the cup with a label equal to the current cup's label minus one. 
    If this would select one of the cups that was just picked up, the crab will keep subtracting one until 
    it finds a cup that wasn't just picked up. If at any point in this process the value goes below the 
    lowest value on any cup's label, it wraps around to the highest value on any cup's label instead.

    The crab places the cups it just picked up so that they are immediately clockwise 
    of the destination cup. They keep the same order as when they were picked up.
    The crab selects a new current cup: the cup which is immediately clockwise of the current cup.
    """
    for e in entries:
        print(e)

def test_day_twenty_three():
    c = CupCircle("389125467")
    for i in range(0, 10):
        c.move()
    cf = c.cups_clockwise_from(1)
    cf_string = ''.join([str(i) for i in cf])
    assert "92658374" == cf_string

    c = CupCircle("389125467")
    for i in range(0, 100):
        c.move()
    cf = c.cups_clockwise_from(1)
    cf_string = ''.join([str(i) for i in cf])
    assert "67384529" == cf_string
    

def day_twenty_three():
    c = CupCircle("123487596")
    for i in range(0, 100):
        c.move()
    cf = c.cups_clockwise_from(1)
    cf_string = ''.join([str(i) for i in cf])
    print(cf_string)


if __name__=="__main__":
    test_day_twenty_three()
    day_twenty_three()