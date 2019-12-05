package main

import (
	"testing"
)

func TestParseInstruction(t *testing.T) {
	result := ParseInstruction([]int{1002, 0, 0, 0, 0}, 0)
	if result.opcode != 2 || result.mode2 != 1 {
		t.Errorf("Parse instruction failed")
	}
}

func TestFivePartOne(t *testing.T) {
	result := Five(1)
	if result != 14155342 {
		t.Errorf("Expected 14155342 got %d", result)
	}
}

func TestFivePartTwo(t *testing.T) {
	result := Five(5)
	if result != 8684145 {
		t.Errorf("Expected 8684145 got %d", result)
	}
}
