package main

import (
	"testing"

	"github.com/gitchander/permutation"
)

func TestParseInstruction(t *testing.T) {
	amp := NewAmplifier(0, []int{1002, 0, 0, 0}, -1)
	result := amp.ParseInstruction(0)
	expected := Instruction{2, 0, 1, 0, 1002, 0, 0}
	if result != expected {
		t.Errorf("Expected %v got %v", expected, result)
	}

	amp = NewAmplifier(0, []int{2002, 0, 0, 0}, -1)
	result = amp.ParseInstruction(0)
	expected = Instruction{2, 0, 2, 0, 2002, 2002, 0}
	if result != expected {
		t.Errorf("Expected %v got %v", expected, result)
	}
}

func TestFivePartOne(t *testing.T) {
	s := SingleLineFileToString("resources/5.txt")
	j := StringToIntArray(s)
	a := NewAmplifier(1, j, -1)
	result := a.process()
	if result.lastOutput() != 14155342 {
		t.Errorf("Expected 14155342 got %d", result.lastOutput())
	}
}

func TestFivePartTwo(t *testing.T) {
	s := SingleLineFileToString("resources/5.txt")
	j := StringToIntArray(s)
	a := NewAmplifier(5, j, -1)
	result := a.process()
	if result.lastOutput() != 8684145 {
		t.Errorf("Expected 8684145 got %d", result.lastOutput())
	}
}

func TestSevenSampleOne(t *testing.T) {
	s := []int{3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0}
	ampA := NewAmplifier(0, copySoftware(s), 4)

	ampB := NewAmplifier(ampA.process().outputs[0], s, 3)

	ampC := NewAmplifier(ampB.process().outputs[0], s, 2)

	ampD := NewAmplifier(ampC.process().outputs[0], s, 1)

	ampE := NewAmplifier(ampD.process().outputs[0], s, 0)

	result := ampE.process()

	if result.lastOutput() != 43210 {
		t.Errorf("Expected 43210, got %d", result.lastOutput())
	}
}

func TestSeven(t *testing.T) {
	max := 0
	s := SingleLineFileToString("resources/7.txt")
	program := StringToIntArray(s)
	a := []int{0, 1, 2, 3, 4}
	p := permutation.New(permutation.IntSlice(a))
	firstInput := new(int)
	*firstInput = 0
	for p.Next() {
		// fmt.Println("hi")
		ampA := NewAmplifier(*firstInput, program, a[0])
		ampA.process()
		// fmt.Println("ampA last out", *ampA.lastOutput)
		ampB := NewAmplifier(ampA.lastOutput, program, a[1])
		// ampB.previousAmp = ampA
		ampB.process()

		ampC := NewAmplifier(ampB.lastOutput, program, a[2])
		// ampC.previousAmp = ampB
		ampC.process()

		ampD := NewAmplifier(ampC.lastOutput, program, a[3])
		// ampD.previousAmp = ampC
		ampD.process()
		// fmt.Println("ampD last out", *ampD.lastOutput)
		ampE := NewAmplifier(ampD.lastOutput, program, a[4])
		// ampE.previousAmp = ampD
		ampE.process()

		last := ampE.lastOutput
		// fmt.Println("ampE last out", *last)
		if last != -1 && last > max {
			max = last
		}
		// firstInput = last
	}

	if max != 206580 {
		t.Errorf("Expected 206580 got %d", max)
	}
}

func TestSevenPartTwoSample(t *testing.T) {
	program := []int{3, 26, 1001, 26, -4, 26, 3, 27, 1002, 27, 2, 27, 1, 27, 26,
		27, 4, 27, 1001, 28, -1, 28, 1005, 28, 6, 99, 0, 0, 5}

	amps := make([]*Amplifier, 5)

	ampA := NewAmplifier(0, program, 9)
	ampA.waiting = true
	amps[0] = ampA

	for i := 1; i < 5; i = i + 1 {
		ampA = NewAmplifier(amps[i-1].process().outputs[0], program, 9-i)
		ampA.waiting = true
		amps[i] = ampA
	}
	amps[4].process()

	for amps[4].waiting && amps[3].waiting && amps[2].waiting && amps[1].waiting && amps[0].waiting {
		amps[0].setSingleInput(amps[4].lastOutput)
		amps[0].process()
		for i := 1; i < 5; i = i + 1 {
			amps[i].setSingleInput(amps[i-1].lastOutput)
			amps[i].process()
		}
	}

	if amps[4].lastOutput != 139629729 {
		t.Errorf("Expected 139629729 got %d", amps[4].lastOutput)
	}
}

func TestSevenPartTwo(t *testing.T) {
	s := SingleLineFileToString("resources/7.txt")
	program := StringToIntArray(s)
	phases := []int{9, 8, 7, 6, 5}
	max := 0
	p := permutation.New(permutation.IntSlice(phases))
	for p.Next() {
		amps := make([]*Amplifier, 5)

		ampA := NewAmplifier(0, program, phases[0])
		ampA.waiting = true
		amps[0] = ampA

		for i := 1; i < 5; i = i + 1 {
			ampA = NewAmplifier(amps[i-1].process().outputs[0], program, phases[i])
			ampA.waiting = true
			amps[i] = ampA
		}
		amps[4].process()

		for amps[4].waiting {
			amps[0].inputs = []int{amps[4].lastOutput}
			amps[0].process()
			for i := 1; i < 5; i = i + 1 {
				amps[i].inputs = []int{amps[i-1].lastOutput}
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

func TestNine(t *testing.T) {
	sampleOneInput := []int{109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99}
	amp := NewAmplifier(0, sampleOneInput, -1)

	for i, v := range amp.process().outputs {
		if v != sampleOneInput[i] {
			t.Errorf("should've matched")
		}
	}
	amp = NewAmplifier(0, []int{1102, 34915192, 34915192, 7, 4, 7, 99, 0}, -1)
	r := amp.process()
	if r.lastOutput() != 1219070632396864 {
		t.Errorf("Expected 1219070632396864 got %d", r.lastOutput())
	}
	amp = NewAmplifier(0, []int{104, 1125899906842624, 99}, -1)
	r = amp.process()

	if r.lastOutput() != 1125899906842624 {
		t.Errorf("Expected 1125899906842624 got %d", r.lastOutput())
	}

	s := SingleLineFileToString("resources/9.txt")
	program := StringToIntArray(s)
	amp = NewAmplifier(1, program, -1)
	r = amp.process()
	if r.lastOutput() != 4234906522 {
		t.Errorf("Expected 4234906522 got %d", 4234906522)
	}

	amp = NewAmplifier(2, program, -1)
	r = amp.process()
	if r.lastOutput() != 60962 {
		t.Errorf("Expected 60962 got %d", r.lastOutput())
	}

}
