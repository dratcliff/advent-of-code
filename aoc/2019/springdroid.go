package main

import "fmt"

func GetCommand(command string) []int {
	bytes := []byte(command)
	ints := []int{}
	for b := range bytes {
		ints = append(ints, int(bytes[b]))
	}
	return ints
}

func BooleanMoron(a, b, c, d, e, f, g, h, i bool) {
	j := false
	t := false

	t = !a
	j = !b
	t = t || j
	j = !c
	t = j || t
	t = t && d
	j = t && d
	j = t || j

	fmt.Println(j)

}

func Spring() {
	s := SingleLineFileToString("resources/21.txt")
	software := StringToIntArray(s)
	commands := GetCommand("NOT A T\nNOT B J\nOR J T\nNOT C J\nOR J T\nAND D T\nAND T J\n OR T J\nWALK\n")
	amp := NewAmplifier(0, software, -1)
	amp.inputs = commands
	r := amp.process()
	for _, o := range r.outputs {
		if o < 256 {
			fmt.Printf("%v", string(o))
		} else {
			fmt.Printf("%v", o)
		}
	}
}

func Spring2() {
	s := SingleLineFileToString("resources/21.txt")
	software := StringToIntArray(s)
	commands := GetCommand("NOT A T\nNOT B J\nOR J T\nNOT C J\nOR J T\nAND D T\nAND T J\n OR T J\nNOT H T\nNOT T T\nOR E T\nAND T J\nRUN\n")
	amp := NewAmplifier(0, software, -1)
	amp.inputs = commands
	r := amp.process()
	for _, o := range r.outputs {
		if o < 256 {
			fmt.Printf("%v", string(o))
		} else {
			fmt.Printf("%v", o)
		}
	}
}
