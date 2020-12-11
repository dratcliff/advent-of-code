def get_next(seq):
    if len(seq) == 0:
        return ""
    if len(seq) == 1:
        return "1" + seq[0]
    
    
    result = ""
    i = 0
    cnt = 1
    l = len(seq)
    while i < l:
        cur = seq[i]
        
        if i < l-1 and seq[i+1] == seq[i]:
            cnt += 1
        else:
            result +=  str(cnt) + cur
            cnt = 1
        i += 1
    return result

def test_day_ten():
    assert get_next("1") == "11"
    assert get_next("11") == "21"
    assert get_next("21") == "1211"
    assert get_next("1211") == "111221"
    assert get_next("111221") == "312211"

def day_ten():
    s = "3113322113"
    for i in range(0, 50):
        s = get_next(s)
    assert 4666278 == len(s)

if __name__=="__main__":
    test_day_ten()
    day_ten()