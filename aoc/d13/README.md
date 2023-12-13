# notes

## part one

seemed like brute force would work, so i just made a function
to return the "triangle" of pairs that would create a reflection, i.e.,

```
(0,1)
(1,2)(0,3)
(2,3),(1,4),(0,5)
```

then i checked each list of pairs with a nested loop for horizontal matches
and i checked against the transposed pattern (```''.join(list(zip(*pattern)))```)
for vertical matches.

## part two

still seemed like brute force would work, so i just replaced every '.' with a '#'
and vice versa (restoring the original afterwards) until i found a different
reflection line. wasted some time because i forgot that in part one
i was depending on the uniqueness of the reflective lines, so i wasn't always
finding a different one after swapping elements.