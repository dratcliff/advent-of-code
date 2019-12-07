package main

import (
	"fmt"
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
	result, _, _ := Five(j, []int{1}, false, 0)
	if result != 14155342 {
		t.Errorf("Expected 14155342 got %d", result)
	}
}

func TestFivePartTwo(t *testing.T) {
	s := SingleLineFileToString("5.txt")
	j := StringToIntArray(s)
	result, _, _ := Five(j, []int{5}, false, 0)
	if result != 8684145 {
		t.Errorf("Expected 8684145 got %d", result)
	}
}

func TestSevenSampleOne(t *testing.T) {
	s := []int{3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0}
	ampA := Amplifier{0, 4, s, 0, false, 0}
	ampB := Amplifier{ampA.process(), 3, s, 0, false, 0}
	ampC := Amplifier{ampB.process(), 2, s, 0, false, 0}
	ampD := Amplifier{ampC.process(), 1, s, 0, false, 0}
	ampE := Amplifier{ampD.process(), 0, s, 0, false, 0}
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
		ampA := Amplifier{0, a[0], program, 0, false, 0}
		ampB := Amplifier{ampA.process(), a[1], program, 0, false, 0}
		ampC := Amplifier{ampB.process(), a[2], program, 0, false, 0}
		ampD := Amplifier{ampC.process(), a[3], program, 0, false, 0}
		ampE := Amplifier{ampD.process(), a[4], program, 0, false, 0}
		result = ampE.process()
		if result > max {
			max = result
		}
	}

	if max != 206580 {
		t.Errorf("Expected 206580 got %d", max)
	}
}

func TestSevenPartTwo(t *testing.T) {
	program := []int{3, 26, 1001, 26, -4, 26, 3, 27, 1002, 27, 2, 27, 1, 27, 26,
		27, 4, 27, 1001, 28, -1, 28, 1005, 28, 6, 99, 0, 0, 5}
	result := 0

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

	ampA := &Amplifier{result, 9, programA, 0, true, 0}
	result = ampA.process()
	ampB := &Amplifier{result, 8, programB, 0, true, 0}
	result = ampB.process()
	ampC := &Amplifier{result, 7, programC, 0, true, 0}
	result = ampC.process()
	ampD := &Amplifier{result, 6, programD, 0, true, 0}
	result = ampD.process()
	ampE := &Amplifier{result, 5, programE, 0, true, 0}
	result = ampE.process()

	for i := 0; i < 5; i = i + 1 {
		ampA.input = result
		result = ampA.process()
		ampB.input = result
		result = ampB.process()
		ampC.input = result
		result = ampC.process()
		ampD.input = result
		result = ampD.process()
		ampE.input = result
		result = ampE.process()
		if ampE.currentPos == -1 {
			fmt.Println("DONE", ampE.lastOutput)
			break
		}
	}
	fmt.Println(result)
}
