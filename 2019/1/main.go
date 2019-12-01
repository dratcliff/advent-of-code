package main

import "bufio"
import "os"
import "fmt"
import "strconv"

func main() {
	fmt.Println("hi")
	f, err := os.Open("input.txt")
	if err != nil {
		panic(err)
	}
	r := bufio.NewReader(f)
	scanner := bufio.NewScanner(r)
	sum := 0
	for scanner.Scan() {
		line := scanner.Text()
		value, _ := strconv.Atoi(line)
		for (value/3 -2) >= 0 {
			sum = sum + (value/3 - 2)
			value = (value/3 - 2)
			fmt.Println(value)
		}
	}
	fmt.Println(sum)
}
