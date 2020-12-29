package main

import (
	"bufio"
	"os"
	"strconv"
	"strings"
)

func Two(program []int) []int {
	i := 0
	for i < len(program)-1 {
		opCode := program[i]
		if opCode == 99 {
			return program
		}
		positionOne := program[i+1]
		positionTwo := program[i+2]
		outputPosition := program[i+3]
		i = i + 4
		if opCode == 1 {
			program[outputPosition] = program[positionOne] + program[positionTwo]
		} else if opCode == 2 {
			program[outputPosition] = program[positionOne] * program[positionTwo]
		} else {
			panic("Unsupported opCode")
		}
	}

	return program
}

func StringToIntArray(input string) []int {
	split := strings.Split(input, ",")
	result := make([]int, len(split))
	for k, v := range split {
		conv, err := strconv.Atoi(v)
		if err != nil {
			panic(err)
		}
		result[k] = conv
	}
	return result
}

func SingleLineFileToString(filename string) string {
	f, err := os.Open(filename)
	if err != nil {
		panic(err)
	}
	reader := bufio.NewReader(f)
	scanner := bufio.NewScanner(reader)
	for scanner.Scan() {
		return scanner.Text()
	}
	return ""
}
