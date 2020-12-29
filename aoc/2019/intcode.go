package main

import (
	"fmt"
	"strconv"
)

type IntcodeComputer interface {
	getSoftware() []int
	getPhase() int
	getSignal() int
	getCurrentIndex() int
	getRelativeBase() int
	adjustRelativeBase(int)
	ParseInstruction(int) Instruction
}

type Amplifier struct {
	inputs       []int
	phase        int
	software     []int
	currentPos   int
	waiting      bool
	lastOutput   int
	relativeBase int
}

func (a *Amplifier) setSingleInput(input int) {
	a.inputs = []int{input}
}

func (a *Amplifier) getSoftware() []int {
	return a.software
}

func (a *Amplifier) getPhase() int {
	r := a.phase
	a.phase = -2
	return r
}

func (a *Amplifier) getSignal() int {
	if len(a.inputs) == 0 {
		return -2
	}
	r := a.inputs[0]
	copy(a.inputs[0:], a.inputs[1:])
	a.inputs[len(a.inputs)-1] = -1
	a.inputs = a.inputs[:len(a.inputs)-1]
	return r
}

func (a *Amplifier) getCurrentIndex() int {
	return a.currentPos
}

func (a *Amplifier) adjustRelativeBase(adjustment int) {
	a.relativeBase = a.relativeBase + adjustment
}

func (a *Amplifier) getRelativeBase() int {
	return a.relativeBase
}

func (a *Amplifier) process() ProcessResult {
	// fmt.Println("start", a.input, a.currentPos)
	result := Run(a, a.waiting)
	// fmt.Println(result.outputs)
	a.software = result.software
	a.currentPos = result.index
	last := result.lastOutput()
	lastIndex := result.index
	// if last != nil && *last != -1 {
	a.lastOutput = last
	// fmt.Println(*last)
	// } else {
	if lastIndex == -1 {
		a.waiting = false
	}
	// fmt.Println("stop", result, i)
	return result
}

func (a *Amplifier) ParseInstruction(index int) Instruction {
	// opcode is instruction % 100
	// modes are instruction / 100
	// if modes % 10 == 0, first parameter mode is prm, else immed
	// if modes % 100 == 0, second parameter mode is prm, else immed
	// if modes / 100 == 0, third parameter mode is prm, else immed
	input := a.software
	instruction := input[index]
	opcode := instruction % 100
	padded := strconv.Itoa(instruction)
	for len(padded) != 5 {
		padded = "0" + padded
	}
	mode3, _ := strconv.Atoi(string(padded[0]))
	mode2, _ := strconv.Atoi(string(padded[1]))
	mode1, _ := strconv.Atoi(string(padded[2]))
	firstParameter, secondParameter, thirdParameter := 0, 0, 0
	switch opcode {
	case 99:
		return Instruction{99, 0, 0, 0, 0, 0, 0}
	case 9:
		adjustment := input[index+1]
		if mode1 == 0 {
			adjustment = input[adjustment]
		} else if mode1 == 2 {
			adjustment = input[adjustment+a.getRelativeBase()]
		}
		return Instruction{9, 0, 0, 0, adjustment, 0, 0}
	case 1, 2, 5, 6, 7, 8:
		firstParameter = input[index+1]
		if mode1 == 0 {
			firstParameter = input[firstParameter]
		} else if mode1 == 2 {
			firstParameter = input[firstParameter+a.relativeBase]
		}
		secondParameter = input[index+2]
		if mode2 == 0 {
			secondParameter = input[secondParameter]
		} else if mode2 == 2 {
			secondParameter = input[secondParameter+a.relativeBase]
		}
		thirdParameter = input[index+3]
		if mode3 == 2 && (opcode != 5 && opcode != 6) {
			// fmt.Println("third parameter", thirdParameter, "relative base", a.relativeBase)
			thirdParameter = thirdParameter + a.relativeBase
		}
	}
	return Instruction{opcode, mode1, mode2, mode3, firstParameter, secondParameter, thirdParameter}
}

func NewAmplifier(input int, software []int, phase int) *Amplifier {
	a := &Amplifier{}
	a.inputs = make([]int, 0)
	a.inputs = append(a.inputs, input)
	a.phase = phase
	a.software = copySoftware(software)
	a.relativeBase = 0
	return a
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
	if i.opcode == 3 || i.opcode == 4 || i.opcode == 9 {
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

type ProcessResult struct {
	outputs   []int
	software  []int
	index     int
	needInput bool
}

func (pr *ProcessResult) lastOutput() int {
	if len(pr.outputs) == 0 {
		return -1
	}
	return pr.outputs[len(pr.outputs)-1]
}

func copySoftware(s []int) []int {
	s1 := make([]int, len(s)*1000)
	copy(s1, s)
	return s1
}

func Run(computer IntcodeComputer, feedback bool) ProcessResult {
	j := computer.getSoftware()
	lastOutput := -1
	index := computer.getCurrentIndex()
	outputs := []int{}
	for i := index; i < len(j); {
		instruction := computer.ParseInstruction(i)
		// fmt.Println("instruction", instruction)

		switch instruction.opcode {
		case 1: //add
			j[instruction.parameter3] = instruction.parameter1 + instruction.parameter2
		case 2: //mult
			j[instruction.parameter3] = instruction.parameter1 * instruction.parameter2
		case 3: //input
			input := computer.getPhase()

			if input == -2 {
				input = computer.getSignal()
			}
			if input == -2 {
				// i = i + instruction.AdvanceLength()
				return ProcessResult{outputs, j, i, true}
			}
			// sig := computer.getSignal()
			// fmt.Println("sig is", *sig)
			// if i > 0 && sig != nil && *sig >= 0 {
			// 	fmt.Println(*sig)
			// 	input = *sig
			// }

			outputPosition := j[i+1]
			if instruction.mode1 == 2 {
				outputPosition = outputPosition + computer.getRelativeBase()
			}
			j[outputPosition] = input
		case 4: //output
			firstParameter := j[i+1]
			if instruction.mode1 == 0 {
				firstParameter = j[firstParameter]
			} else if instruction.mode1 == 2 {
				firstParameter = j[firstParameter+computer.getRelativeBase()]
			}
			lastOutput = firstParameter
			outputs = append(outputs, lastOutput)
			// fmt.Println("outputs", outputs)
			// if feedback {
			// 	i = i + instruction.AdvanceLength()
			// 	return ProcessResult{outputs, j, i}
			// }
		case 5: //jump non-zero
			if instruction.parameter1 != 0 {
				i = instruction.parameter2
				continue
			}
		case 6: //jump zero
			if instruction.parameter1 == 0 {
				i = instruction.parameter2
				continue
			}
		case 7: //less than zero
			if instruction.parameter1 < instruction.parameter2 {
				j[instruction.parameter3] = 1
			} else {
				j[instruction.parameter3] = 0
			}
		case 8: //is zero
			if instruction.parameter1 == instruction.parameter2 {
				j[instruction.parameter3] = 1
			} else {
				j[instruction.parameter3] = 0
			}
		case 9: //adjust relative base
			computer.adjustRelativeBase(instruction.parameter1)
		case 99: //halt
			return ProcessResult{outputs, j, -1, false}
		default:
			fmt.Printf("unsupported opcode %v\n", instruction)
			panic("unsupported opcode" + string(instruction.opcode))
		}
		i = i + instruction.AdvanceLength()
	}
	return ProcessResult{outputs, j, -1, false}
}
