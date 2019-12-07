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

func TestSevenSampleOne(t *testing.T) {
	s := []int{3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0}
	ampA := NewAmplifier(0, copySoftware(s))
	ampA.phase = 4

	ampB := NewAmplifier(0, s)
	ampB.previousAmp = ampA
	ampB.phase = 3

	ampC := NewAmplifier(0, s)
	ampC.phase = 2
	ampC.previousAmp = ampB

	ampD := NewAmplifier(0, s)
	ampD.phase = 1
	ampD.previousAmp = ampC

	ampE := NewAmplifier(0, s)
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

	amps := make([]*Amplifier, 5)

	ampA := NewAmplifier(0, program)
	ampA.phase = 9
	ampA.waiting = true
	amps[0] = ampA

	for i := 1; i < 5; i = i + 1 {
		ampA = NewAmplifier(amps[i-1].process(), program)
		ampA.phase = 9 - i
		ampA.waiting = true
		amps[i] = ampA
	}
	amps[4].process()

	for amps[4].waiting {
		amps[0].input = amps[4].lastOutput
		amps[0].process()
		for i := 1; i < 5; i = i + 1 {
			amps[i].input = amps[i-1].lastOutput
			amps[i].process()
		}
	}

	if amps[4].lastOutput != 139629729 {
		t.Errorf("Expected 139629729 got %d", amps[4].lastOutput)
	}
}

func TestSevenPartTwo(t *testing.T) {
	s := SingleLineFileToString("7.txt")
	program := StringToIntArray(s)
	phases := []int{9, 8, 7, 6, 5}
	max := 0
	p := permutation.New(permutation.IntSlice(phases))
	for p.Next() {
		amps := make([]*Amplifier, 5)

		ampA := NewAmplifier(0, program)
		ampA.phase = phases[0]
		ampA.waiting = true
		amps[0] = ampA

		for i := 1; i < 5; i = i + 1 {
			ampA = NewAmplifier(amps[i-1].process(), program)
			ampA.phase = phases[i]
			ampA.waiting = true
			amps[i] = ampA
		}
		amps[4].process()

		for amps[4].waiting {
			amps[0].input = amps[4].lastOutput
			amps[0].process()
			for i := 1; i < 5; i = i + 1 {
				amps[i].input = amps[i-1].lastOutput
				amps[i].process()
			}
		}

		if amps[4].lastOutput > max {
			max = amps[4].lastOutput
		}
	}
	if max != 2299406 {
		t.Errorf("Expected 2299406 got %d", max)
	}
}
