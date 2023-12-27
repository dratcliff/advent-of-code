# notes

## part one

simple BFS

## part two

Brute force obviously wasn't going to work...

ChatGPT led me to the shoelace formula for finding the area of a polygon.
The "hard" part was handling the additional area occupied by the digger
when it stops. For example, if the instructions were

```
R6
D3
L6
U3
```

A rectangle would have an area of 18, but in this problem, the area is 21.

I managed this by tracking four points occupied by a digger (represented by a car in my case).
I maintained two lists of vertices: one for those experienced by the driver's side
and one for those experienced by the passenger's side. One will be larger than the other
depending on whether the digger turns left or right first, so I just printed the max.

To calculate the vertices, I made functions to rotate the "car" left and right.
I then have a pretty crude mapping to determine whether the car should turn left or right
based on the car's previous direction.

The driver's side vertex is always appended before rotating right and after rotating left.
The passenger's side is just the opposite. This makes sure that the vertices are consistently
appended for either the inside or the outside of the digger's path, depending on which
way the digger turned initially.

This diagram may be helpful to show the orientation of the digger when its driver's side
vertices are appended:

```
>>>>>>>
#.....v
###...v
..#...v
..#...v
###.v<v
#...v..
##..>##
.#....#
.######
```