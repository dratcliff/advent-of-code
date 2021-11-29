import utils.utils as utils

def new_math(expr):
    if "*" in expr:
        expr = expr.split(" * ")
        to_mult = []
        for e in expr:
            e = e.split(" + ")
            e = [int(e) for e in e]
            to_mult.append(sum(e))
        p = 1
        for t in to_mult:
            p *= t
        return p
    else:
        expr = expr.split(" ")
    result = None
    while len(expr) > 0:
        cur = expr[0]
        if result == None:
            result = int(cur)
            expr = expr[1:]
        elif cur == '+':
            result += int(expr[1])
            expr = expr[2:]
        elif cur == '*':
            result *= int(expr[1])
            expr = expr[2:]
    return result

def find_parens(expr):
    from collections import deque
    stack = deque()
    for i in range(0, len(expr)):
        if expr[i] == "(":
            stack.append((i, "("))
        elif expr[i] == ")":
            last = stack[-1]
            if last[1] == "(":
                to_do = expr[last[0]+1:i]
                done = new_math(to_do)
                expr = expr.replace('(' + to_do +')', str(done))
                return expr
    return expr

def evaluate(expression):
    while "(" in expression:
        expression = find_parens(expression)
    ans = new_math(expression)
    return ans

@utils.timed
def day_eighteen():
    expressions = utils.file_to_string_list("Day18.txt")       
    ans = 0
    for expr in expressions:
        ans += evaluate(expr)
    print(ans)

@utils.timed
def test_day_eighteen():
    expression = "1 + 2 * 3 + 4 * 5 + 6"
    ans = evaluate(expression)
    assert 231 == ans

    expression = "1 + (2 * 3) + (4 * (5 + 6))"
    ans = evaluate(expression)
    assert 51 == ans

    expression = "2 * 3 + (4 * 5)"
    ans = evaluate(expression)
    assert 46 == ans

    expression = "5 + (8 * 3 + 9 + 3 * 4 * 3)"
    ans = evaluate(expression)
    assert 1445 == ans

    expression = "5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))"
    ans = evaluate(expression)
    assert 669060 == ans

    expression = "((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"
    ans = evaluate(expression)
    assert 23340 == ans


if __name__=="__main__":
    test_day_eighteen()
    day_eighteen()