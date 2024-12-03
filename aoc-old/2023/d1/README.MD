# notes

## part one

pretty straightforward

## part two

```
Your calculation isn't quite right. It looks like some of the digits are actually spelled out with letters: one, two, three, four, five, six, seven, eight, and nine also count as valid "digits".

Equipped with this new information, you now need to find the real first and last digit on each line. For example:

two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen

In this example, the calibration values are 29, 83, 13, 24, 42, 14, and 76. Adding these together produces 281.
```

I figured that since eightwothree maps to 83, I should be able to reuse my code from part one
if I just replaced `eight` with `e8t` leaving `e8twothree` and `two` with `t2o` leaving `e8t2othree`, etc.
It's important to not replace the first and last letters entirely, otherwise for a string like
`eighthree` you'd end up with `8hree` instead of `83`.

The first way I thought to do this was with a manually constructed mapping:

```
replacements = {
    'one': 'o1e',
    'two': 't2o',
    'three': 't3e',
    'four': 'f4r',
    'five': 'f5e',
    'six': 's6x',
    'seven': 's7n',
    'eight': 'e8t',
    'nine': 'n9e'
}
```

Not very fancy, but I rarely am. ;)