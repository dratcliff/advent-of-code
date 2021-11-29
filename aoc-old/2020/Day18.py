import utils.utils as utils

def new_math(expr):
    if "(" in expr:
        expr = expr.split("(")
        print(expr)
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
    assert 71 == ans

    expression = "1 + (2 * 3) + (4 * (5 + 6))"
    ans = evaluate(expression)
    assert 51 == ans

    """
    2 * 3 + (4 * 5) becomes 26.
    5 + (8 * 3 + 9 + 3 * 4 * 3) becomes 437.
    5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4)) becomes 12240.
    ((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2 becomes 13632.
    """

    expression = "2 * 3 + (4 * 5)"
    ans = evaluate(expression)
    assert 26 == ans

    expression = "5 + (8 * 3 + 9 + 3 * 4 * 3)"
    ans = evaluate(expression)
    assert 437 == ans

    expression = "5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))"
    ans = evaluate(expression)
    assert 12240 == ans

    expression = "((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"
    ans = evaluate(expression)
    assert 13632 == ans


if __name__=="__main__":
    test_day_eighteen()
    day_eighteen()