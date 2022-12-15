from utilaoc import file_to_strings

actual = file_to_strings("input.txt")
order = actual[0]
order = order.split(",")
boards = actual[1:]
pboards = []
for board in boards:
    if board == '':
        next_board = []
        pboards.append(next_board)
    else:
        board = board.lstrip()
        board = board.rstrip()
        board = board.replace("  ", " ")
        board = board.split(" ")
        next_board.append(board)

def check(game):
    winners = []
    for board in game:
        win = False
        columns = [0, 0, 0, 0, 0]
        for row in board:
            if row == ['x', 'x', 'x', 'x', 'x']:
                win = True
                if board not in winners:
                    winners.append(board)
            for i in range(0, len(row)):
                if row[i] == 'x':
                    columns[i] += 1
            for column in columns:
                if column == 5:
                    win = True
                    if board not in winners:
                        winners.append(board)
    return winners
        

def get_score(b, m):
    unmarked_sum = 0
    for row in b:
        for cell in row:
            if cell != 'x':
                unmarked_sum += int(cell)
    print(unmarked_sum, m)
    print(unmarked_sum * int(m))

for move in order:
    for board in pboards:
        for row in board:
            for i in range(0, len(row)):
                if row[i] == move:
                    row[i] = 'x'
    checked = check(pboards)
    if len(checked) != 0:
        for c in checked:
            print(c)
            get_score(c, move)
        
            pboards.remove(c)
