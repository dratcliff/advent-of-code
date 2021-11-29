package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
)

func findWord(words []string) (string, string) {
	for _, w := range words {
		for _, x := range words {
			diff := 0
			for k1, v1 := range w {
				if rune(x[k1]) != v1 {
					diff = diff + 1
				}
			}
			if diff == 1 {
				return w, x
			}
		}
	}
	return "", ""
}

func commonLetters(first string, second string) string {
	word := ""
	for k1, x := range first {
		if x == rune(second[k1]) {
			word = word + string(x)
		}
	}
	return word
}

func main() {
	file, err := os.Open("input.txt")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	words := make([]string, 0)
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		words = append(words, scanner.Text())
	}

	first, second := findWord(words)
	fmt.Println(commonLetters(first, second))

}
