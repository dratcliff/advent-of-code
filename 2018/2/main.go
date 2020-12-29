package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
)

func main() {
	file, err := os.Open("input.txt")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	sum := 0
	twos, threes := 0, 0
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		occurs := make(map[rune]int, 0)
		text := scanner.Text()
		for _, v := range text {
			_, ok := occurs[v]
			if !ok {
				occurs[v] = 1
			} else {
				occurs[v] = occurs[v] + 1
			}
		}
		twosPresent, threesPresent := false, false
		for _, v := range occurs {
			if v == 2 {
				twosPresent = true
			}
			if v == 3 {
				threesPresent = true
			}
		}
		if twosPresent {
			twos = twos + 1
		}
		if threesPresent {
			threes = threes + 1
		}
	}

	fmt.Println(twos * threes)

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	fmt.Println(sum)
}
