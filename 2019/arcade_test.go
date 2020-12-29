package main

import (
	"testing"
)

func TestCountBlocks(t *testing.T) {
	s := SingleLineFileToString("resources/13.txt")
	software := StringToIntArray(s)
	software[0] = 2
	amp := NewAmplifier(0, software, -1)
	r := amp.process()
	sum := 0
	maxX := 0
	maxY := 0
	for i := 0; i < len(r.outputs); i = i + 3 {
		if r.outputs[i] > maxX {
			maxX = r.outputs[i]
		}
		if r.outputs[i+1] > maxY {
			maxY = r.outputs[i+1]
		}
		if r.outputs[i+2] == 2 {
			sum = sum + 1
		}
	}
	if sum != 341 {
		t.Errorf("Expected 341 blocks got %d", sum)
	}
}
