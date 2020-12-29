package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
)

func main() {
	sum := 0
	freqs := make(map[int]bool, 0)
	for {
		file, err := os.Open("input.txt")
		if err != nil {
			log.Fatal(err)
		}
		scanner := bufio.NewScanner(file)
		for scanner.Scan() {
			i, _ := strconv.Atoi(scanner.Text())
			sum = sum + i
			_, ok := freqs[sum]
			if ok {
				fmt.Println("Duplicate found", sum)
				os.Exit(0)
			} else {
				fmt.Println(sum)
				freqs[sum] = true
			}
		}
		file.Close()
	}

}
