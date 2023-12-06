xs = [x.strip('\n').split(":")[1] for x in open('input.txt', 'r').readlines()]

times = list(map(int, xs[0].strip().split()))
distances = list(map(int, xs[1].strip().split()))

product = 1
for j in range(len(distances)):
    count = 0
    for i in range(0, times[j]+1):
        if i*(times[j]-i) > distances[j]:
            count += 1
    product *= count

print(product)

time = int(xs[0].strip().replace(" ", ""))
distance = int(xs[1].strip().replace(" ", ""))

count = 0
for i in range(0, time+1):
    if i*(time-i) > distance:
        count += 1

print(count)
