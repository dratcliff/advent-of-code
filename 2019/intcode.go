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
	input        int
	phase        int
	software     []int
	currentPos   int
	waiting      bool
	lastOutput   int
	previousAmp  *Amplifier
	nextAmp      *Amplifier
	relativeBase int
}

func (a *Amplifier) getSoftware() []int {
	return a.software
}

func (a *Amplifier) getPhase() int {
	return a.phase
}

func (a *Amplifier) getSignal() int {
	return a.input
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
	if a.previousAmp != nil {
		p := a.previousAmp.process()
		a.input = p.lastOutput()
	}
	result := Run(a, a.waiting)
	a.software = result.software
	a.currentPos = result.index
	if result.lastOutput() != -1 {
		a.lastOutput = result.lastOutput()
	} else {
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

func NewAmplifier(input int, software []int) *Amplifier {
	a := &Amplifier{}
	a.input = input
	a.phase = -1
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
	outputs  []int
	software []int
	index    int
}

func (pr *ProcessResult) lastOutput() int {
	if len(pr.outputs) == 0 {
		return -1
	}
	return (pr.outputs[len(pr.outputs)-1])
}

func copySoftware(s []int) []int {
	s1 := make([]int, len(s)*1000)
	copy(s1, s)
	return s1
}

func Run(computer IntcodeComputer, feedback bool) ProcessResult {
	j := computer.getSoftware()
	lastOutput := -1
	input := computer.getPhase()
	if input == -1 {
		input = computer.getSignal()
	}
	index := computer.getCurrentIndex()
	outputs := []int{}
	for i := index; i < len(j); {
		instruction := computer.ParseInstruction(i)
		if i > 0 && computer.getSignal() >= 0 {
			input = computer.getSignal()
		}

		switch instruction.opcode {
		case 1: //add
			j[instruction.parameter3] = instruction.parameter1 + instruction.parameter2
		case 2: //mult
			j[instruction.parameter3] = instruction.parameter1 * instruction.parameter2
		case 3: //input
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
			if feedback {
				i = i + instruction.AdvanceLength()
				return ProcessResult{outputs, j, i}
			}
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
			return ProcessResult{outputs, j, -1}
		default:
			fmt.Printf("unsupported opcode %v\n", instruction)
			panic("unsupported opcode" + string(instruction.opcode))
		}
		i = i + instruction.AdvanceLength()
	}
	return ProcessResult{outputs, j, -1}
}
