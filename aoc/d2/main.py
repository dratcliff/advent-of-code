from collections import defaultdict

game_map = defaultdict(lambda: defaultdict(int))
xs = [x.strip('\n') for x in open('input.txt', 'r').readlines()]

for x in xs:
    x = x.split(": ")
    game_id = x[0].split()[1]
    games = x[1].split("; ")
    games = [game.split(", ") for game in games]
    for game in games:
        game = [g.split() for g in game]
        game = [(int(g[0]), g[1]) for g in game]
        for color in game:
            game_map[game_id][color[1]] = max(game_map[game_id][color[1]], color[0])
    
the_sum = 0
the_sum2 = 0
for k, v in game_map.items():
    if v["red"] <= 12 and v["green"] <= 13 and v["blue"] <= 14:
        the_sum += int(k)
    the_sum2 += v["red"]*v["green"]*v["blue"]

print(the_sum, the_sum2)