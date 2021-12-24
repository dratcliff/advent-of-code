from utilaoc import file_to_strings

actual = file_to_strings("a.txt")
actual = [x.split(" ") for x in actual]
# print(actual)


"""
inp a - Read an input value and write it to variable a.
add a b - Add the value of a to the value of b, then store the result in variable a.
mul a b - Multiply the value of a by the value of b, then store the result in variable a.
div a b - Divide the value of a by the value of b, truncate the result to an integer, then store the result in variable a. (Here, "truncate" means to round the value toward zero.)
mod a b - Divide the value of a by the value of b, then store the remainder in variable a. (This is also called the modulo operation.)
eql a b - If the value of a and b are equal, then store the value 1 in variable a. Otherwise, store the value 0 in variable a.
"""

def get_number(numbers):
    if type(numbers) == int:
        numbers = [int(x) for x in str(numbers)]
    n = numbers[0]
    numbers = numbers[1:]
    return n, numbers

from collections import defaultdict



def ALU(actual, n):
    memory = defaultdict(int)
    for a in actual:
        if len(a) == 2 and a[0] == 'inp':
            memory[a[1]], n = get_number(n)
        elif len(a) == 3:
            if a[0] == 'add':
                left = memory[a[1]]
                right = a[2]
                if right in ('w', 'x', 'y', 'z'):
                    right = memory[right]
                else:
                    right = int(right)
                memory[a[1]] = left + right
            elif a[0] == 'mul':
                left = memory[a[1]]
                right = a[2]
                if right in ('w', 'x', 'y', 'z'):
                    right = memory[right]
                else:
                    right = int(right)
                memory[a[1]] = left * right
            elif a[0] == 'div':
                left = memory[a[1]]
                right = a[2]
                if right in ('w', 'x', 'y', 'z'):
                    right = memory[right]
                else:
                    right = int(right)
                memory[a[1]] = int(left / right)
            elif a[0] == 'mod':
                left = memory[a[1]]
                right = a[2]
                if right in ('w', 'x', 'y', 'z'):
                    right = memory[right]
                else:
                    right = int(right)
                memory[a[1]] = left % right
            elif a[0] == 'eql':
                left = memory[a[1]]
                right = a[2]
                if right in ('w', 'x', 'y', 'z'):
                    right = memory[right]
                else:
                    right = int(right)
                
                if left == right:
                    memory[a[1]] = 1
                else:
                    memory[a[1]] = 0
        # print(a, memory["w"], memory["x"], memory["y"], memory["z"])
    return memory["z"]
            

# xybzza(a-4)(b+5)zzzz(y+1)(x-5)
# ALU(actual, 81291957997923)
# 81291737995723
# model_number = 81291737994623
# 81291737994623
# 81491959997923
# 88191956336893
# 81x91xx7xxxx23
# mmm = 1
# valid = ALU(actual, model_number)
# inc = 0
# while model_number < 99999999999999:
#     model_number += 100
#     while "0" in str(model_number):
#         model_number += 100
    
#     valid = ALU(actual, model_number)
#     if  valid == 0:
#         print(model_number, valid)

# print(model_number)

for x in range(6, 7):
    for y in range(1, 8):
        for b in range(1, 5):
            for a in range(5, 10):
                for z1 in range(11, 100):
                    for z2 in range(1, 10):
                        for z3 in range(1, 8):
                            model_number = str(x) + str(y) + str(b) + str(z1) + str(a) + str(a-4) + str(b+5) + str(z2) + str(z2) + str(z3) + str(z3+2) + str(y+1) + str(x-5)
                            # print(model_number)
                            if "0" in model_number:
                                continue
                            if ALU(actual, int(model_number)) == 0:
                                print(model_number)
                                import sys
                                sys.exit()

# prefix = "81"
# suffix = "23"

# for i in range(5915111111, 9999999999):
#     model_number = int(prefix + str(i) + suffix)
#     if "0" in str(model_number):
#         continue
#     valid = ALU(actual, model_number)
#     inc = 0
#     if valid == 0:
#         print(model_number, valid)
#         break
# m = "812917379946233"
# from itertools import combinations
# for p in combinations(m, 14):
#     mn = int(''.join(p))
#     print(mn, ALU(actual, mn))
# 81291737994623
# 11191736777161 95
# 111917365579122 83

"""
8119151 6666823
8119151 6667923
8119151 6771323
8119151 6772423
8119151 6773523
8119151 6774623
8119151 6775723
8119151 6776823
8119151 6777923
8119151 6881323
8119151 6882423
8119151 6883523
8119151 6884623
8119151 6885723
8119151 6886823
8119151 6887923
8119151 6991323
8119151 6992423
8119151 6993523
8119151 6994623
8119151 6995723
8119151 6996823
8119151 6997923
"""

# this is complete garbage, but I'm not cleaning it up because... I don't know
# I just tried a bunch of stuff until I found a valid model number, then searched around that one 
# for more valid model numbers. Once I had a decent number of them, I tried to figure out if there
# was some kind of pattern to them. At first I thought all of mine would end in 23, but then I found 
# one that ended in 31 or something -- realized that the last digit was the first digit - 5, next to last
# was next-to-first + 1, etc. Then I found a few more patterns -- didn't bother to find them all once
# I got the right answer.