package main

import (
	"fmt"
)

type Amplifier struct {
	input      int
	phase      int
	software   []int
	currentPos int
	waiting    bool
	lastOutput int
}

func (a *Amplifier) process() int {
	// fmt.Println("start", a.input, a.currentPos)
	phase := a.phase
	if a.currentPos != 0 {
		phase = a.input
	}
	result, s, i := Five(a.software, []int{phase, a.input}, a.waiting, a.currentPos)
	a.software = s
	a.currentPos = i
	if result != -1 {
		a.lastOutput = result
	}

	// fmt.Println("stop", result, i)
	return result
}

type Instruction struct {
	opcode     int
	mode1      int
	mode2      int
	mode3      int
	parameter1 int
	parameter2 int
	parameter3 int
}

func (i *Instruction) AdvanceLength() int {
	if i.opcode == 3 {
		return 2
	}
	if i.opcode == 4 {
		return 2
	}
	if i.opcode == 1 || i.opcode == 2 || i.opcode == 7 || i.opcode == 8 {
		return 4
	}
	if i.opcode == 99 {
		return 1
	}
	if i.opcode == 5 || i.opcode == 6 {
		return 3
	}
	panic("unsupported opcode")
}

func ParseInstruction(input []int, index int) Instruction {
	// opcode is instruction % 100
	// modes are instruction / 100
	// if modes % 10 == 0, first parameter mode is prm, else immed
	// if modes % 100 == 0, second parameter mode is prm, else immed
	// if modes / 100 == 0, third parameter mode is prm, else immed
	instruction := input[index]
	opcode := instruction % 100
	modes := instruction / 100
	mode1, mode2, mode3 := 1, 1, 1
	if modes == 1 {
		mode2, mode3 = 0, 0
	} else if modes == 10 {
		mode1, mode3 = 0, 0
	} else if modes == 11 {
		mode3 = 0
	} else if modes == 0 {
		mode1, mode2, mode3 = 0, 0, 0
	} else {
		fmt.Println("modes", modes)
	}
	firstParameter, secondParameter, thirdParameter := 0, 0, 0
	switch opcode {
	case 99:
		return Instruction{99, 0, 0, 0, 0, 0, 0}
	case 1, 2, 5, 6, 7, 8:
		firstParameter = input[index+1]
		if mode1 == 0 {
			firstParameter = input[firstParameter]
		}
		secondParameter = input[index+2]
		if mode2 == 0 {
			secondParameter = input[secondParameter]
		}
		thirdParameter = input[index+3]
		// if mode3 == 0 && (opcode == 5 || opcode == 6) {
		// thirdParameter = input[thirdParameter]
		// }
	}
	return Instruction{opcode, mode1, mode2, mode3, firstParameter, secondParameter, thirdParameter}
}

func Five(program []int, inputs []int, feedback bool, index int) (int, []int, int) {
	j := program
	lastOutput := -1
	input := inputs[0]
	for i := index; i < len(j); {
		instruction := ParseInstruction(j, i)
		// fmt.Println(instruction)
		if i > 0 && len(inputs) > 1 {
			input = inputs[1]
		}

		switch instruction.opcode {
		case 1:
			// fmt.Println("1", i, instruction, j)
			j[instruction.parameter3] = instruction.parameter1 + instruction.parameter2
		case 2:
			j[instruction.parameter3] = instruction.parameter1 * instruction.parameter2
		case 3:
			outputPosition := j[i+1]
			j[outputPosition] = input
		case 4:
			firstParameter := j[i+1]
			if instruction.mode1 == 0 {
				firstParameter = j[firstParameter]
			}
			lastOutput = firstParameter
			if feedback {
				// fmt.Println(j[i], j[i+1], j[i+2], j[i+3])
				i = i + instruction.AdvanceLength()
				return lastOutput, j, i
			}
		case 5:
			// fmt.Println("5", i, instruction, j)
			if instruction.parameter1 != 0 {
				i = instruction.parameter2
				continue
			}
		case 6:
			// fmt.Println("5", i, instruction, j)
			if instruction.parameter1 == 0 {
				i = instruction.parameter2
				continue
			}
		case 7:
			if instruction.parameter1 < instruction.parameter2 {
				j[instruction.parameter3] = 1
			} else {
				j[instruction.parameter3] = 0
			}
		case 8:
			if instruction.parameter1 == instruction.parameter2 {
				j[instruction.parameter3] = 1
			} else {
				j[instruction.parameter3] = 0
			}
		case 99:
			// fmt.Println("halting")
			return lastOutput, j, -1
		default:
			fmt.Printf("unsupported opcode %v\n", instruction)
			panic("unsupported opcode" + string(instruction.opcode))
		}
		i = i + instruction.AdvanceLength()
	}
	return lastOutput, j, -1
}
