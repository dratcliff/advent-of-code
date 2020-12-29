import hashlib

def get_md5(s):
    return hashlib.md5(s.encode('utf-8')).hexdigest()

def day_four():
    v = get_md5("abcdef609043")
    assert "00000" == v[0:5]

    i = 0
    v = get_md5("yzbqklnj" + str(i))
    while "00000" != v[0:5]:
        i += 1
        v = get_md5("yzbqklnj" + str(i))

    assert 282749 == i

def day_four_part_two():
    v = get_md5("abcdef609043")
    assert "00000" == v[0:5]

    i = 0
    v = get_md5("yzbqklnj" + str(i))
    while "000000" != v[0:6]:
        i += 1
        v = get_md5("yzbqklnj" + str(i))

    assert i == 9962624

if __name__=="__main__":
    day_four()
    day_four_part_two()