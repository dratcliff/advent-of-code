# notes

Notably, I still can't remember how to make a `defaultdict` of `defaultdict`.

But here it is, again:

```
from collections import defaultdict

game_map = defaultdict(lambda: defaultdict(int))
```

## part one

Time breakdown: 90% text processing, 5% thinking, 5% getting the answer.

## part two

It evidently took me 1m54s to answer part two after answering part one. It felt both
faster and slower than that. In addition to seeing if the game was possible,
we also just sum the per-game product of the maximum number of cubes (cubes? I think)
of each color encountered.