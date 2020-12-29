import utils
import collections

player1 = collections.deque()
player2 = collections.deque()


def run(entries):
    current = player1
    for e in entries:
        if "Player 2" in e:
            current = player2
        elif "Player 1" in e:
            current = player1
        elif len(e) == 0:
            continue
        else:
            current.append(int(e))

    while len(player1) > 0 and len(player2) > 0:
        p1c = player1.popleft()
        p2c = player2.popleft()
        if p1c > p2c:
            player1.append(p1c)
            player1.append(p2c)
        else:
            player2.append(p2c)
            player2.append(p1c)

    winner = None
    if len(player1) == 0:
        winner = player2
    else:
        winner = player1

    score = 0
    i = 1
    while len(winner) > 0:
        bottom = winner.pop()
        score += bottom*i
        i += 1

    return score


def test_day_twenty_two():
    entries = utils.file_to_string_list("Day22sample.txt")
    assert 306 == run(entries)


def day_twenty_two():
    entries = utils.file_to_string_list("Day22.txt")
    assert 31308 == run(entries)


if __name__ == "__main__":
    test_day_twenty_two()
    day_twenty_two()
