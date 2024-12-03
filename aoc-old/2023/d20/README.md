# notes

## part one

## part two

`rx` only has one input, `dt`.

`dt` has 4 inputs (in my data anyway). I checked to see how often each one flips
to high (my `len(found) == 4` trick wouldn't work in general -- I was just being
lazy because I could tell the first four flips would be for distinct sources).
once I knew how often each one flipped, I calculated the `lcm` and that's the 
answer.