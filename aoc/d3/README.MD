# notes

reading is fundamental

## part one

After failing to read the problem correctly a few times, I realized that
I should just go character-by-character.

If the current position is numeric:
- if I'm not building a number, start building one
- if this position is adjacent to a symbol, mark this number to be retained

If the current position isn't numeric or the current position is the last in the line:
- if I was previously building a number and it was adjacent to a symbol,
add it to the list of numbers
- reset the state of the program

sum the numbers

## part two

just like part one, except

If the current position is numeric:
- if I'm not building a number, start building one
- if this position is adjacent to a symbol, mark this number to be retained
- *if this position is adjacent to a gear, mark this number as adjacent to a gear
and add the position of the gear to a set of gears this number is adjacent to*

If the current position isn't numeric or the current position is the last in the line:
- if I was previously building a number and it was adjacent to a symbol,
add it to the list of numbers
    - *if this number was adjacent to any gears gear, add this number to to the list of numbers
    that each gear is adjacent to*
- reset the state of the program

sum the numbers

*sum the products of numbers for each gear that is adjacent to two numbers*