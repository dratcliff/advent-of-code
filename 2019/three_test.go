package main

import (
	"fmt"
	"testing"
)

func TestThreeSmallSampleOne(t *testing.T) {
	distance := Three("R8,U5,L5,D3", "U7,R6,D4,L4")
	if distance.Manhattan != 6 {
		t.Errorf("Expected 6 got %d", distance)
	}
}
func TestThreeSampleOne(t *testing.T) {
	distance := Three("R75,D30,R83,U83,L12,D49,R71,U7,L72",
		"U62,R66,U55,R34,D71,R55,D58,R83")
	if distance.Manhattan != 159 {
		t.Errorf("Expected 159 got %d", distance)
	}
}

func TestThreeSampleTwo(t *testing.T) {
	distance := Three("R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51",
		"U98,R91,D20,R16,D67,R40,U7,R15,U6,R7")
	if distance.Manhattan != 135 {
		t.Errorf("Expected 135 got %d", distance)
	}
}

func TestThree(t *testing.T) {
	pathOne := SingleLineFileToString("resources/3a.txt")
	pathTwo := SingleLineFileToString("resources/3b.txt")
	distance := Three(pathOne, pathTwo)
	fmt.Println(distance)
}

func TestThreePartTwoSampleOne(t *testing.T) {
	distance := Three("R75,D30,R83,U83,L12,D49,R71,U7,L72",
		"U62,R66,U55,R34,D71,R55,D58,R83")
	if distance.Signal != 610 {
		t.Errorf("Expected 610 got %d", distance.Signal)
	}
}

func TestThreePartTwoSampleTwo(t *testing.T) {
	distance := Three("R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51",
		"U98,R91,D20,R16,D67,R40,U7,R15,U6,R7")
	if distance.Signal != 410 {
		t.Errorf("Expected 410 got %d", distance.Signal)
	}
}

func TestThreePartTwo(t *testing.T) {
	pathOne := SingleLineFileToString("resources/3a.txt")
	pathTwo := SingleLineFileToString("resources/3b.txt")
	fmt.Println(Three(pathOne, pathTwo))
}
