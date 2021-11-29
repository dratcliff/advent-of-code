package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
)

type rule struct {
	pattern [5]bool
	outcome bool
}

func initialState() map[int]bool {
	file, err := os.Open("initial_state.txt")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	line := ""
	for scanner.Scan() {
		line = scanner.Text()
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}
	result := make(map[int]bool, 0)
	for k, v := range line {
		if string(v) == "#" {
			result[k] = true
		} else {
			result[k] = false
		}
	}
	return result
}

func rules() []rule {
	file, err := os.Open("rules.txt")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	rules := make([]rule, 0)
	for scanner.Scan() {
		line := scanner.Text()
		var pattern [5]bool
		for i := 0; i < 5; i++ {
			if string(line[i]) == "#" {
				pattern[i] = true
			}
		}
		_outcome := string(line[9])
		outcome := false
		if _outcome == "#" {
			outcome = true
		}
		rule := rule{pattern, outcome}
		rules = append(rules, rule)
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}
	return rules
}

func aliveBoundaries(state map[int]bool) (int, int) {
	min, max := 0, 0
	for k, v := range state {
		if v && k < min {
			min = k
		}
		if v && k > max {
			max = k
		}
	}
	return min, max
}

func keyBoundaries(state map[int]bool) (int, int) {
	min, max := 0, 0
	for k, _ := range state {
		if k < min {
			min = k
		}
		if k > max {
			max = k
		}
	}
	return min, max
}

func expand(state map[int]bool, first int, last int) map[int]bool {
	for i := 1; i <= 5; i++ {
		state[first-i] = false
		state[last+i] = false
	}
	return state
}

func run(initial map[int]bool, rules []rule) map[int]bool {
	length := len(initial)
	first, last := aliveBoundaries(initial)
	initial = expand(initial, first, last)
	first, last = keyBoundaries(initial)
	next := make(map[int]bool, length)
	for k, _ := range initial {
		next[k] = false
	}
	for i := first; i < last-4; i++ {
		for _, r := range rules {
			match := true
			for j := 0; j < 5; j++ {
				if r.pattern[j] != initial[i+j] {
					match = false
				}
			}
			if match {
				next[i+2] = r.outcome
			}
		}
	}
	return next
}

func printState(state map[int]bool) {
	first, last := keyBoundaries(state)
	for i := first; i <= last; i++ {
		if i == 0 {
			fmt.Print("[")
		}
		if state[i] {
			fmt.Print("#")
		} else {
			fmt.Print(".")
		}
		if i == 0 {
			fmt.Print("]")
		}
	}
	fmt.Println()
}

func sumPots(state map[int]bool) int {
	sum := 0
	for k, v := range state {
		if v {
			sum += k
		}
	}
	return sum
}

func main() {
	initialState := initialState()
	rules := rules()
	total := 0
	sum := 0
	for i := 0; i < 150; i++ {
		initialState = run(initialState, rules)
		sum = sumPots(initialState)
		total += sum
		fmt.Println(i, sum, i*194)
	}
	// for part two, some trial/error showed that
	// formula converges to ((i-1)*186)+1209
}
