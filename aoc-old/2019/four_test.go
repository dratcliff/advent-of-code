package main

import (
	"testing"
)

func TestSampleOne(t *testing.T) {
	valid := HasDoubleOccurrence(111111)
	if !valid {
		t.Errorf("Expected true got %v", valid)
	}
	valid = IsNonDecreasing(111111)
	if !valid {
		t.Errorf("Expected true got %v", valid)
	}
}

func TestSampleTwo(t *testing.T) {
	valid := IsValidPassword(223450)
	if valid {
		t.Errorf("223450 is not non-decreasing")
	}
}

func TestSampleThree(t *testing.T) {
	valid := IsValidPassword(123789)
	if valid {
		t.Errorf("123789 has no double occurrence")
	}
}

func TestRangePartOne(t *testing.T) {
	count := 0
	// 240298-784956
	for i := 240298; i <= 784956; i = i + 1 {
		if IsValidPassword(i) {
			count = count + 1
		}
	}
	if count != 1150 {
		t.Errorf("Expected 1150 got %d", count)
	}
}

func TestRangePartTwo(t *testing.T) {
	count := 0
	for i := 240298; i <= 784956; i = i + 1 {
		if IsValidPasswordPartTwo(i) {
			count = count + 1
		}
	}
	if count != 748 {
		t.Errorf("Expected 748 got %d", count)
	}
}
