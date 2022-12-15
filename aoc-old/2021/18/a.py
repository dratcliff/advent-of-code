from itertools import combinations
from collections import defaultdict
from collections import deque
from utilaoc import file_to_strings
import ast
actual = file_to_strings("a.txt")
actual = [ast.literal_eval(x) for x in actual]


class Node:
    def __init__(self, as_list, depth):
        self.depth = depth
        self.val = as_list
        if type(as_list[0]) == list:
            self.left = Node(as_list[0], depth+1)
        else:
            self.left = as_list[0]
        if type(as_list[1]) == list:
            self.right = Node(as_list[1], depth+1)
        else:
            self.right = as_list[1]


def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start


def walk(node, actions, counts):
    if type(node.left) == Node:
        walk(node.left, actions, counts)
    if type(node.left) == int and type(node.right) == int:
        counts[(node.left, node.right)] += 1
    if node.depth == 4:
        actions.append(("explode", node.left, node.right,
                       counts[(node.left, node.right)]))
    elif type(node.left) == int and node.left > 9:
        actions.append(("split", node.left))
    elif type(node.right) == int and node.right > 9:
        actions.append(("split", node.right))
    if type(node.right) == Node:
        walk(node.right, actions, counts)


def reduce(sn_num):
    actions = []
    counts = defaultdict(int)
    walk(Node(sn_num, 0), actions, counts)
    next_action = None
    for action in actions:
        if action[0] == 'explode':
            next_action = action
            break
    if next_action == None and len(actions) > 0:
        next_action = actions[0]
    elif next_action == None:
        return sn_num
    sn_num_as_string = ""
    if next_action[0] == 'explode':
        pair_string = "[" + str(next_action[1]) + "," + \
            str(next_action[2]) + "]"
        sn_num_as_string = str(sn_num).replace(" ", "")
        i = find_nth(sn_num_as_string, pair_string, next_action[3])
        left = sn_num_as_string[:i]
        right = sn_num_as_string[i+len(pair_string):]
        for j in range(len(left)-1, -1, -1):
            found = ""
            if left[j] not in ['[', ']', ',']:
                k = j
                while left[k] not in ['[', ']', ',']:
                    found = left[k] + found
                    k -= 1
                left = left[:j-len(found)+1] + \
                    str(int(found) + next_action[1]) + left[j+1:]
                break
        for j in range(0, len(right)):
            found = ""
            if right[j] not in ['[', ']', ',']:
                k = j
                while right[k] not in ['[', ']', ',']:
                    found = found + right[k]
                    k += 1
                right = right[:j] + str(int(found) +
                                        next_action[2]) + right[j+len(found):]

                break
        sn_num_as_string = left + "0" + right
    elif next_action[0] == 'split':
        sn_num_as_string = str(sn_num).replace(" ", "")
        new_left = next_action[1] // 2
        new_right = next_action[1] - new_left
        replacement = "[" + str(new_left) + "," + str(new_right) + "]"
        sn_num_as_string = sn_num_as_string.replace(
            str(next_action[1]), replacement, 1)
    sn_num = ast.literal_eval(sn_num_as_string)
    return sn_num


def snadd(left, right):
    combined = []
    combined.append(left)
    combined.append(right)
    return combined


def reduce2(c):
    done = False
    while not done:
        next_c = reduce(c)
        if next_c == c:
            done = True
        c = next_c
    return c


def add_list(l):
    current = snadd(l[0], l[1])
    current = reduce2(current)
    i = 2
    while i < len(l):
        current = snadd(current, l[i])
        current = reduce2(current)
        i += 1
    return current


def solve(n):
    if type(n) == int:
        return n
    if type(n.left) == int and type(n.right) == int:
        return 3 * n.left + 2 * n.right
    return 3 * solve(n.left) + 2*solve(n.right)


m = 0
for c in combinations(actual, 2):
    l = []
    l.append(c[0])
    l.append(c[1])
    a = add_list(l)
    na = Node(a, 0)
    g = solve(na)
    if g > m:
        m = g
print(m)
