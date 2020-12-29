package main

import (
	"fmt"
	"testing"
)

func TestOnePlusOne(t *testing.T) {
	p := make([]int, 5)
	p[0] = 1
	p[1] = 0
	p[2] = 0
	p[3] = 0
	p[4] = 99
	p = Two(p)
	if p[0] != 2 {
		t.Errorf("Result incorrect. Got %d expected %d", p[0], 2)
	}
	if p[1] != 0 || p[2] != 0 || p[3] != 0 || p[4] != 99 {
		t.Errorf("Remaining fields should've been unchanged. Actual: %v", p)
	}
}

func TestThreeTimesTwo(t *testing.T) {
	p := make([]int, 5)
	p[0] = 2
	p[1] = 3
	p[2] = 0
	p[3] = 3
	p[4] = 99
	p = Two(p)
	if p[3] != 6 {
		t.Errorf("Result incorrect. Got %d expected %d", p[3], 6)
	}
	if p[0] != 2 || p[1] != 3 || p[2] != 0 || p[4] != 99 {
		t.Errorf("Remaining fields should've been unchanged. Actual: %v", p)
	}
}

func TestNinetyNineTimesNinetyNine(t *testing.T) {
	p := make([]int, 6)
	p[0] = 2
	p[1] = 4
	p[2] = 4
	p[3] = 5
	p[4] = 99
	p[5] = 0
	p = Two(p)
	if p[5] != 9801 {
		t.Errorf("Result incorrect. Got %d expected %d", p[5], 9801)
	}
	if p[0] != 2 || p[1] != 4 || p[2] != 4 || p[3] != 5 || p[4] != 99 {
		t.Errorf("Remaining fields should've been unchanged. Actual: %v", p)
	}
}

func TestStringToArray(t *testing.T) {
	expected := make([]int, 9)
	expected[0] = 1
	expected[1] = 1
	expected[2] = 1
	expected[3] = 4
	expected[4] = 99
	expected[5] = 5
	expected[6] = 6
	expected[7] = 0
	expected[8] = 99
	i := StringToIntArray("1,1,1,4,99,5,6,0,99")
	for k := range i {
		if i[k] != expected[k] {
			t.Errorf("Expected %d got %d", expected[k], i[k])
		}
	}
}

func TestSingleLineFileToString(t *testing.T) {
	s := SingleLineFileToString("resources/2.txt")
	if s == "" {
		t.Errorf("Should not have been empty string")
	}
}

func TestPartOne(t *testing.T) {
	s := SingleLineFileToString("resources/2.txt")
	i := StringToIntArray(s)
	i[1] = 12
	i[2] = 2
	i = Two(i)
	fmt.Println(i)
}

func TestPartTwo(t *testing.T) {
	s := SingleLineFileToString("resources/2.txt")
	noun := 0
	v := 19690720
	for noun < 100 {
		verb := 0
		for verb < 100 {
			i := StringToIntArray(s)
			i[1] = noun
			i[2] = verb
			i = Two(i)
			if i[0] == v {
				fmt.Println("Found it", noun, verb, 100*noun+verb)
				return
			}
			verb = verb + 1
		}
		noun = noun + 1
	}
	fmt.Println("didn't find it")

}
