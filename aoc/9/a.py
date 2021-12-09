from utilaoc import file_to_strings

actual = file_to_strings("a.txt")
actual = [[int(x) for x in y] for y in actual]

height = len(actual)
width = len(actual[0])

low_points = []

# for i in range(0, height):
#     for j in range(0, width):
#         # print(i, j)
#         if i == 0:
#             if j == 0:
#                 if actual[i][j] < actual[i+1][j] and \
#                     actual[i][j] < actual[i][j+1]:
#                         low_points.append(actual[i][j])
#             elif j == width-1:
#                 if actual[i][j] < actual[i+1][j] and \
#                     actual[i][j] < actual[i][j-1]:
#                         low_points.append(actual[i][j])
#             else:
#                 if actual[i][j] < actual[i+1][j] and \
#                     actual[i][j] < actual[i][j-1] and \
#                         actual[i][j] < actual[i][j+1]:
#                         low_points.append(actual[i][j])
#         elif i == height-1:
#             if j == 0:
#                 if actual[i][j] < actual[i-1][j] and \
#                     actual[i][j] < actual[i][j+1]:
#                         low_points.append(actual[i][j])
#             elif j == width-1:
#                 if actual[i][j] < actual[i-1][j] and \
#                     actual[i][j] < actual[i][j-1]:
#                         low_points.append(actual[i][j])
#             else:
#                 if actual[i][j] < actual[i-1][j] and \
#                     actual[i][j] < actual[i][j-1] and \
#                     actual[i][j] < actual[i][j+1]:
#                         low_points.append(actual[i][j])
#         else:
#             if j == 0:
#                 if actual[i][j] < actual[i-1][j] and \
#                     actual[i][j] < actual[i+1][j] and \
#                     actual[i][j] < actual[i][j+1]:
#                         low_points.append(actual[i][j])
#             elif j == width-1:
#                 if actual[i][j] < actual[i-1][j] and \
#                     actual[i][j] < actual[i+1][j] and \
#                     actual[i][j] < actual[i][j-1]:
#                         low_points.append(actual[i][j])
#             else:
#                 if actual[i][j] < actual[i-1][j] and \
#                     actual[i][j] < actual[i+1][j] and \
#                     actual[i][j] < actual[i][j-1] and \
#                     actual[i][j] < actual[i][j+1]:
#                         low_points.append(actual[i][j])

# print(sum([x+1 for x in low_points]))

for i in range(0, height):
    for j in range(0, width):
        # print(i, j)
        if i == 0:
            if j == 0:
                if actual[i][j] < actual[i+1][j] and \
                    actual[i][j] < actual[i][j+1]:
                        low_points.append((i, j))
            elif j == width-1:
                if actual[i][j] < actual[i+1][j] and \
                    actual[i][j] < actual[i][j-1]:
                        low_points.append((i, j))
            else:
                if actual[i][j] < actual[i+1][j] and \
                    actual[i][j] < actual[i][j-1] and \
                        actual[i][j] < actual[i][j+1]:
                        low_points.append((i, j))
        elif i == height-1:
            if j == 0:
                if actual[i][j] < actual[i-1][j] and \
                    actual[i][j] < actual[i][j+1]:
                        low_points.append((i, j))
            elif j == width-1:
                if actual[i][j] < actual[i-1][j] and \
                    actual[i][j] < actual[i][j-1]:
                        low_points.append((i, j))
            else:
                if actual[i][j] < actual[i-1][j] and \
                    actual[i][j] < actual[i][j-1] and \
                    actual[i][j] < actual[i][j+1]:
                        low_points.append((i, j))
        else:
            if j == 0:
                if actual[i][j] < actual[i-1][j] and \
                    actual[i][j] < actual[i+1][j] and \
                    actual[i][j] < actual[i][j+1]:
                        low_points.append((i, j))
            elif j == width-1:
                if actual[i][j] < actual[i-1][j] and \
                    actual[i][j] < actual[i+1][j] and \
                    actual[i][j] < actual[i][j-1]:
                        low_points.append((i, j))
            else:
                if actual[i][j] < actual[i-1][j] and \
                    actual[i][j] < actual[i+1][j] and \
                    actual[i][j] < actual[i][j-1] and \
                    actual[i][j] < actual[i][j+1]:
                        low_points.append((i, j))


grid = {}
for i in range(0, height):
    for j in range(0, width):
        grid[(i,j)] = actual[i][j]

basins = [[x] for x in low_points]

offsets = [(0, 1), (0, -1), (-1, 0), (1, 0)]

for basin in basins:
    more = True
    while more:
        more = False
        for point in basin:
            for offset in offsets:
                if (point[0]-offset[0], point[1]-offset[1]) not in basin and \
                    (point[0]-offset[0], point[1]-offset[1]) in grid and \
                        grid[(point[0]-offset[0], point[1]-offset[1])] > grid[point] and \
                            grid[(point[0]-offset[0], point[1]-offset[1])] != 9:
                    more = True
                    basin.append((point[0]-offset[0], point[1]-offset[1]))

basins = sorted(basins, key=lambda x: len(x), reverse=True)
basins = basins[:3]
s = 1
for basin in basins:
    s *= len(basin)
print(s)

# this is 141 lines of pure sophistication