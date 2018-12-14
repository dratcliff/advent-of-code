package main

import (
	"fmt"
	"os"
	"strings"
)

//vVZzWwrEeCcwvoOVsSiCHhDQqdcUuWwsiCctVvT

func main() {
	f, err := os.Open("input.txt")
	if err != nil {
		panic(err)
	}
	result := make([]byte, 0)
	buf := make([]byte, 1)
	i := 0
	for {
		_, err = f.Read(buf)
		if err != nil {
			break
		}
		result = append(result, buf[0])
		last := string(result[i])
		if len(result) > 1 {
			nextToLast := string(result[i-1])
			if nextToLast != last {
				if strings.ToLower(nextToLast) == strings.ToLower(last) {
					result = result[:i-1]
					i = i - 2
				}
			}
		}
		i++
	}
	fmt.Println(len(string(result)) - 1)
}
