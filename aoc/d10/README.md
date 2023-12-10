# notes

## part one
simple BFS

## part two
Took me waaaaaay too long to figure out a "clever" way to solve this.
I eventually figured out I could just add a half space in between every
position and then close those half-spaces as I went around the loop.

From there, I just filled in the grid starting from the outside
and then counted all the tiles that weren't part of the loop and
hadn't been filled in. 