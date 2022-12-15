from utilaoc import file_to_strings

actual = file_to_strings("a.txt")
output = [x.split(' | ')[1] for x in actual]

input = [x.split(' | ')[0] for x in actual]
input = [x.split(' ') for x in input]
input = [[set(x) for x in y] for y in input]
output = [x.split(' ') for x in output]
output = [[set(x) for x in y] for y in output]

total = 0
for idx, input_entry in enumerate(input):
    zero = set()
    one = set()
    two = set()
    three = set()
    four = set()
    five = set()
    six = set()
    seven = set()
    eight = set()
    nine = set()
    for scrambled_digit in input_entry:
        if len(scrambled_digit) == 2:
            one = scrambled_digit
        if len(scrambled_digit) == 3:
            seven = scrambled_digit
        if len(scrambled_digit) == 4:
            four = scrambled_digit
        if len(scrambled_digit) == 7:
            eight = scrambled_digit

    for scrambled_digit in input_entry:
        if len(scrambled_digit) == 6 and len(scrambled_digit & four) == 4:
            nine = scrambled_digit
    for scrambled_digit in input_entry:
        if len(scrambled_digit) == 6 and scrambled_digit != nine and len(scrambled_digit & one) == 2:
            zero = scrambled_digit
    for scrambled_digit in input_entry:
        if len(scrambled_digit) == 6 and scrambled_digit != nine and scrambled_digit != zero:
            six = scrambled_digit

    for scrambled_digit in input_entry:
        if len(scrambled_digit) == 5 and len(scrambled_digit & one) == 2:
            three = scrambled_digit
    for scrambled_digit in input_entry:
        if len(scrambled_digit) == 5 and scrambled_digit != three:
            if len(scrambled_digit & four) == 2:
                two = scrambled_digit
            else:
                five = scrambled_digit
    
    output_entry = output[idx]
    output_digit = ""
    for scrambled_digit in output_entry:
        if scrambled_digit == zero:
            output_digit += "0"
        elif scrambled_digit == one:
            output_digit += "1"
        elif scrambled_digit == two:
            output_digit += "2"
        elif scrambled_digit == three:
            output_digit += "3"
        elif scrambled_digit == four:
            output_digit += "4"
        elif scrambled_digit == five:
            output_digit += "5"
        elif scrambled_digit == six:
            output_digit += "6"
        elif scrambled_digit == seven:
            output_digit += "7"
        elif scrambled_digit == eight:
            output_digit += "8"
        elif scrambled_digit == nine:
            output_digit += "9"
    total += int(output_digit)

print(total)
