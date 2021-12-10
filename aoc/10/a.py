from collections import defaultdict
from utilaoc import file_to_strings

actual = file_to_strings("a.txt")


inv = {
    ')': '(',
    ']': '[',
    '>': '<',
    '}': '{',
    '{': '}',
    '(': ')',
    '[': ']',
    '<': '>'
}
rights = [']', '>', '}', ')']

scores = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4
}

errors = []

for a in actual:
    error_score = 0
    counts = defaultdict(int)
    while "()" in a or "[]" in a or "{}" in a or "<>" in a:
        a = a.replace("()", "")
        a = a.replace("[]", "")
        a = a.replace("<>", "")
        a = a.replace("{}", "")
    skip = False
    for i in a:
        if i in rights:
            skip = True
            break
    if not skip:
        for i in reversed(a):
            error_score *= 5
            error_score += scores[inv[i]]
        errors.append(error_score)

errors = sorted(errors)
print(errors[len(errors)//2])
