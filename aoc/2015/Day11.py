"""Passwords must include one increasing straight of at least three letters, like abc, bcd, cde, and so on, up to xyz. They cannot skip letters; abd doesn't count.
Passwords may not contain the letters i, o, or l, as these letters can be mistaken for other characters and are therefore confusing.
Passwords must contain at least two different, non-overlapping pairs of letters, like aa, bb, or zz."""
def is_valid(p):
    straight = False
    for i in range(0, len(p)-2):
        if ord(p[i]) == ord(p[i+1]) - 1 == ord(p[i+2]) - 2:
            straight = True
    
    confusing = False
    if "i" in p or "o" in p or "l" in p:
        confusing = True

    overlaps = set()
    for i in range(0, len(p)-1):
        if p[i] == p[i+1]:
            if p[i] not in overlaps:
                overlaps.add(p[i])
            else:
                overlaps.remove(p[i])

    return straight and not confusing and len(overlaps) >= 2




def increment(p):
    cur = 7
    p = list(p)
    if p[cur] == 'z':
        while p[cur] == 'z':
            p[cur] = 'a'
            cur -= 1
    
    p[cur] = chr(ord(p[cur])+1)
    return ''.join(p)

def get_next(p):
    p = increment(p)
    while not is_valid(p):
        p = increment(p)
    return p

def test_day_eleven():
    assert "abcdffaa" == get_next("abcdefgh")
    assert "ghjaabcc" == get_next("ghijklmn") #takes a while
    assert "vzbxxyzz" == get_next("vzbxkghb")
    assert "vzcaabcc" == get_next("vzbxxyzz")

if __name__=="__main__":
    test_day_eleven()