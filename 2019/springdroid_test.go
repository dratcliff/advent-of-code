package main

import "testing"

func TestSpring(t *testing.T) {
	Spring()
}

func TestSpring2(t *testing.T) {
	Spring2()
}

func TestBooleanMoron(t *testing.T) {
	// ##.#.##.#
	BooleanMoron(true, true, false, true, false, true, true, false, true)
	// .#.##.#.
	BooleanMoron(false, true, false, true, true, false, true, false, true)
}
