# notes

## part one
literally just added an extra row/column for each empty row/column,
then computed the manhattan distance between each pair of galaxies.

## part two

it was pretty obvious that my approach in part one wouldn't work,
so instead I computed the distances iteratively (I could've made this faster)
and if I encountered an empty row/column, instead of adding one, I
added the expansion factor.