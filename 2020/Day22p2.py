import utils
import collections

"""
Before either player deals a card, if there was a previous round in this game that had exactly the same cards in the same order in the same players' decks,
 the game instantly ends in a win for player 1. Previous rounds from other games are not considered. (This prevents infinite games of Recursive Combat, 
 which everyone agrees is a bad idea.)
Otherwise, this round's cards must be in a new configuration; the players begin the round by each drawing the top card of their deck as normal.
If both players have at least as many cards remaining in their deck as the value of the card they just drew, the winner of the round is determined by playing
 a new game of Recursive Combat (see below).
Otherwise, at least one player must not have enough cards left in their deck to recurse; the winner of the round is the player with the higher-value card.

During a round of Recursive Combat, if both players have at least as many cards in their own decks as the number on the card they just dealt, the winner of the round is
 determined by recursing into a sub-game of Recursive Combat. (For example, if player 1 draws the 3 card, and player 2 draws the 7 card, this would occur if player 1 has
  at least 3 cards left and player 2 has at least 7 cards left, not counting the 3 and 7 cards that were drawn.)

To play a sub-game of Recursive Combat, each player creates a new deck by making a copy of the next cards in their deck (the quantity of cards copied is equal to
 the number on the card they drew to trigger the sub-game). During this sub-game, the game that triggered it is on hold and completely unaffected; no cards are
  removed from players' decks to form the sub-game. (For example, if player 1 drew the 3 card, their deck in the sub-game would be copies of the next three cards in their deck.)

"""


def collapse(n, n2):
    return 'x'.join([str(x) for x in n]) + 'x'.join([str(y) for y in n2])


def play(player1, player2):
    prevs = set()
    while len(player1) > 0 and len(player2) > 0:
        prev = collapse(player1, player2)
        if prev in prevs:
            return (player1, "p1")
        prevs.add(prev)
        p1c = player1.popleft()
        p2c = player2.popleft()

        if p1c <= len(player1) and p2c <= len(player2):
            player1c = collections.deque(list(player1.copy())[0:p1c])
            player2c = collections.deque(list(player2.copy())[0:p2c])
            winner = play(player1c, player2c)
            if winner[1] == "p1":
                player1.append(p1c)
                player1.append(p2c)
            else:
                player2.append(p2c)
                player2.append(p1c)
        else:
            if p1c > p2c:
                player1.append(p1c)
                player1.append(p2c)
            else:
                player2.append(p2c)
                player2.append(p1c)

    if len(player1) == 0:
        return (player2, "p2")
    else:
        return (player1, "p1")


def run(entries):
    player1 = collections.deque()
    player2 = collections.deque()
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

    winner = play(player1, player2)[0]
    score = 0
    i = 1
    while len(winner) > 0:
        bottom = winner.pop()
        score += bottom*i
        i += 1
    return score


def test_day_twenty_two():
    entries = utils.file_to_string_list("Day22sample.txt")
    assert 291 == run(entries)


def test_day_twenty_two_infinite():
    entries = utils.file_to_string_list("Day22infinite.txt")
    assert 105 == run(entries)


def day_twenty_two():
    entries = utils.file_to_string_list("Day22.txt")
    assert 33647 == run(entries)


if __name__ == "__main__":
    test_day_twenty_two()
    test_day_twenty_two_infinite()
    day_twenty_two()
