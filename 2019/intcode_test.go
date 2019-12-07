package main

import (
	"testing"

	"github.com/gitchander/permutation"
)

func TestParseInstruction(t *testing.T) {
	result := ParseInstruction([]int{1002, 0, 0, 0, 0}, 0)
	if result.opcode != 2 || result.mode2 != 1 {
		t.Errorf("Parse instruction failed")
	}
}

func TestFivePartOne(t *testing.T) {
	s := SingleLineFileToString("5.txt")
	j := StringToIntArray(s)
	a := NewAmplifier(1, j)
	result := a.process()
	if result != 14155342 {
		t.Errorf("Expected 14155342 got %d", result)
	}
}

func TestFivePartTwo(t *testing.T) {
	s := SingleLineFileToString("5.txt")
	j := StringToIntArray(s)
	a := NewAmplifier(5, j)
	result := a.process()
	if result != 8684145 {
		t.Errorf("Expected 8684145 got %d", result)
	}
}

func copySoftware(s []int) []int {
	s1 := make([]int, len(s))
	copy(s1, s)
	return s1
}

func TestSevenSampleOne(t *testing.T) {
	s := []int{3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0}
	ampA := NewAmplifier(0, copySoftware(s))
	ampA.phase = 4

	ampB := NewAmplifier(0, copySoftware(s))
	ampB.previousAmp = ampA
	ampB.phase = 3

	ampC := NewAmplifier(0, copySoftware(s))
	ampC.phase = 2
	ampC.previousAmp = ampB

	ampD := NewAmplifier(0, copySoftware(s))
	ampD.phase = 1
	ampD.previousAmp = ampC

	ampE := NewAmplifier(0, copySoftware(s))
	ampE.phase = 0
	ampE.previousAmp = ampD

	result := ampE.process()

	if result != 43210 {
		t.Errorf("Expected 43210, got %d", result)
	}
}

func TestSeven(t *testing.T) {
	result, max := 0, 0
	s := SingleLineFileToString("7.txt")
	program := StringToIntArray(s)
	a := []int{0, 1, 2, 3, 4}
	p := permutation.New(permutation.IntSlice(a))
	for p.Next() {
		ampA := NewAmplifier(0, program)
		ampA.phase = a[0]

		ampB := NewAmplifier(0, program)
		ampB.previousAmp = ampA
		ampB.phase = a[1]

		ampC := NewAmplifier(0, program)
		ampC.phase = a[2]
		ampC.previousAmp = ampB

		ampD := NewAmplifier(0, program)
		ampD.phase = a[3]
		ampD.previousAmp = ampC

		ampE := NewAmplifier(0, program)
		ampE.phase = a[4]
		ampE.previousAmp = ampD

		result = ampE.process()
		if result > max {
			max = result
		}
	}

	if max != 206580 {
		t.Errorf("Expected 206580 got %d", max)
	}
}

func TestSevenPartTwoSample(t *testing.T) {
	program := []int{3, 26, 1001, 26, -4, 26, 3, 27, 1002, 27, 2, 27, 1, 27, 26,
		27, 4, 27, 1001, 28, -1, 28, 1005, 28, 6, 99, 0, 0, 5}

	programA := make([]int, len(program))
	programB := make([]int, len(program))
	programC := make([]int, len(program))
	programD := make([]int, len(program))
	programE := make([]int, len(program))

	copy(programA, program)
	copy(programB, program)
	copy(programC, program)
	copy(programD, program)
	copy(programE, program)

	ampA := NewAmplifier(0, programA)
	ampA.phase = 9
	ampA.waiting = true

	ampB := NewAmplifier(ampA.process(), programB)
	ampB.phase = 8
	ampB.waiting = true

	ampC := NewAmplifier(ampB.process(), programC)
	ampC.phase = 7
	ampC.waiting = true

	ampD := NewAmplifier(ampC.process(), programD)
	ampD.phase = 6
	ampD.waiting = true

	ampE := NewAmplifier(ampD.process(), programE)
	ampE.phase = 5
	ampE.waiting = true

	ampE.process()

	for ampE.waiting {
		ampA.input = ampE.lastOutput
		ampA.process()

		ampB.input = ampA.lastOutput
		ampB.process()

		ampC.input = ampB.lastOutput
		ampC.process()

		ampD.input = ampC.lastOutput
		ampD.process()

		ampE.input = ampD.lastOutput
		ampE.process()
	}

	if ampE.lastOutput != 139629729 {
		t.Errorf("Expected 139629729 got %d", ampE.lastOutput)
	}
}

func TestSevenPartTwo(t *testing.T) {
	s := SingleLineFileToString("7.txt")
	program := StringToIntArray(s)

	programA := make([]int, len(program))
	programB := make([]int, len(program))
	programC := make([]int, len(program))
	programD := make([]int, len(program))
	programE := make([]int, len(program))

	copy(programA, program)
	copy(programB, program)
	copy(programC, program)
	copy(programD, program)
	copy(programE, program)

	a := []int{9, 8, 7, 6, 5}
	max := 0
	p := permutation.New(permutation.IntSlice(a))
	for p.Next() {

		copy(programA, program)
		copy(programB, program)
		copy(programC, program)
		copy(programD, program)
		copy(programE, program)

		ampA := NewAmplifier(0, programA)
		ampA.phase = a[0]
		ampA.waiting = true

		ampB := NewAmplifier(ampA.process(), programB)
		ampB.phase = a[1]
		ampB.waiting = true

		ampC := NewAmplifier(ampB.process(), programC)
		ampC.phase = a[2]
		ampC.waiting = true

		ampD := NewAmplifier(ampC.process(), programD)
		ampD.phase = a[3]
		ampD.waiting = true

		ampE := NewAmplifier(ampD.process(), programE)
		ampE.phase = a[4]
		ampE.waiting = true

		ampE.process()

		for ampE.waiting {
			ampA.input = ampE.lastOutput
			ampA.process()

			ampB.input = ampA.lastOutput
			ampB.process()

			ampC.input = ampB.lastOutput
			ampC.process()

			ampD.input = ampC.lastOutput
			ampD.process()

			ampE.input = ampD.lastOutput
			ampE.process()
		}
		if ampE.lastOutput > max {
			max = ampE.lastOutput
		}
	}
	if max != 2299406 {
		t.Errorf("Expected 2299406 got %d", max)
	}
}
