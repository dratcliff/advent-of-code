package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
)

func One() {
	fmt.Println("hi")
	f, err := os.Open("1.txt")
	if err != nil {
		panic(err)
	}
	r := bufio.NewReader(f)
	scanner := bufio.NewScanner(r)
	sum := 0
	for scanner.Scan() {
		line := scanner.Text()
		value, _ := strconv.Atoi(line)
		for (value/3 - 2) >= 0 {
			sum = sum + (value/3 - 2)
			value = (value/3 - 2)
			fmt.Println(value)
		}
	}
	fmt.Println(sum)
}
