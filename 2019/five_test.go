package main

import (
	"fmt"
	"testing"
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
	result := Five(j, []int{1})
	if result != 14155342 {
		t.Errorf("Expected 14155342 got %d", result)
	}
}

func TestFivePartTwo(t *testing.T) {
	s := SingleLineFileToString("5.txt")
	j := StringToIntArray(s)
	result := Five(j, []int{5})
	if result != 8684145 {
		t.Errorf("Expected 8684145 got %d", result)
	}
}

func TestSevenSampleOne(t *testing.T) {
	s := []int{3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0}
	result := 0
	for i := 4; i >= 0; i = i - 1 {
		result = Five(s, []int{i, result})
	}
	fmt.Println(result)
}

func TestSeven(t *testing.T) {
	result, max := 0, 0
	s := SingleLineFileToString("7.txt")
	program := StringToIntArray(s)
	for i := 0; i < 5; i = i + 1 {
		for j := 0; j < 5; j = j + 1 {
			for k := 0; k < 5; k = k + 1 {
				for l := 0; l < 5; l = l + 1 {
					for m := 0; m < 5; m = m + 1 {
						if i == j || i == k || i == l || i == m ||
							j == k || j == l || j == m || k == l || k == m || l == m {
							continue
						} else {
							seq := []int{i, j, k, l, m}
							result = 0
							for n := 0; n < 5; n = n + 1 {
								result = Five(program, []int{seq[n], result})
							}
							if result > max {
								fmt.Println(result)
								max = result
							}
						}
					}
				}
			}
		}
	}
	if max != 206580 {
		t.Errorf("Expected 206580 got %d", max)
	}
}

func TestCombo(t *testing.T) {

}
