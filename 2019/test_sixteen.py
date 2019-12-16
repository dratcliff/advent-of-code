
def fft(input):
    r = []
    pattern = [0, 1, 0, -1]
    for i in range(1, len(input)+1):
        p = [x for x in pattern for y in range(0, i)]    
        while len(p) < len(input):
            p.extend(p)
        p.pop(0)
        p = p[0:len(input)]
        q = [x*y for x,y in zip(input, p)]
        r.append((abs(sum(q)) % 10))
    return r

def get_digit(number, n):
    return str(number)[n]
    
def test_fft():
    expected = 48226158
    actual = fft(12345678)
    assert expected == actual

initial = 59750530221324194853012320069589312027523989854830232144164799228029162830477472078089790749906142587998642764059439173975199276254972017316624772614925079238407309384923979338502430726930592959991878698412537971672558832588540600963437409230550897544434635267172603132396722812334366528344715912756154006039512272491073906389218927420387151599044435060075148142946789007756800733869891008058075303490106699737554949348715600795187032293436328810969288892220127730287766004467730818489269295982526297430971411865028098708555709525646237713045259603175397623654950719275982134690893685598734136409536436003548128411943963263336042840301380655801969822

def part_one():
    e = [int(i) for i in str(initial)]
    for i in range(0, 100):
        e = fft(e)

    print(e)

def part_two(input):
    print(len(input))
    a = input
    b = [None] * len(a)
    sum = 0
    for i in range(len(a)-1, -1, -1):
        sum += a[i]
        b[i] = sum
    b = [a%10 for a in b]
    return b

part_two_initial = str(initial)*10000

offset = int(part_two_initial[0:7])
# print(len(part_two_initial))
# print(offset)

remaining = part_two_initial[offset:]
remaining = [int(i) for i in remaining]
# print(remaining)

for i in range(0, 100):
    remaining = part_two(remaining)

print(remaining[0:8])