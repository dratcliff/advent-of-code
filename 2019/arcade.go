package main

import (
	"fmt"
	"time"

	"github.com/eiannone/keyboard"
)

func main() {
	s := SingleLineFileToString("13.txt")
	software := StringToIntArray(s)
	software[0] = 2
	amp := NewAmplifier(0, software, -1)
	r := amp.process()
	neutral := 0
	left := -1
	right := 1
	grid := make([][]string, 20)
	input := make(chan int, 1)
	go getInput(input)
	for i := 0; i < 20; i = i + 1 {
		grid[i] = make([]string, 44)
	}
	ballX := 1
	paddleX := 1
	score := 0
	for {
		grid, score, paddleX, ballX = render(r.outputs, grid, score, paddleX, ballX)
		if r.index == -1 {
			fmt.Println(score)
		}
		select {
		case i := <-input:
			amp.setSingleInput(i)

		case <-time.After(100 * time.Millisecond):
			amp.setSingleInput(neutral)
			if ballX > paddleX && paddleX < 44 {
				amp.setSingleInput(right)
			} else if ballX < paddleX && paddleX > 0 {
				amp.setSingleInput(left)
			}
		}

		r = amp.process()
	}

}

func getInput(input chan int) {
	for {
		char, _, err := keyboard.GetSingleKey()
		if err != nil {
			panic(err)
		}

		text := string(char)
		neutral := new(int)
		*neutral = 0
		left := -1
		right := 1

		if text[0] == 'a' {
			input <- left
		} else if text[0] == 's' {
			input <- right
		}
	}
}

func render(outputs []int, grid [][]string, score int, paddleX int, ballX int) ([][]string, int, int, int) {

	print("\033[H\033[2J")
	for i := 0; i < len(outputs); i = i + 3 {

		x := outputs[i]
		y := outputs[i+1]
		v := outputs[i+2]
		c := " "
		if v == 1 {
			c = "|"
		} else if v == 2 {
			c = "V"
		} else if v == 3 {
			c = "X"
			paddleX = x
		} else if v == 4 {
			c = "O"
			ballX = x
		} else if x == -1 {
			score = v
			continue
		}
		grid[y][x] = c

	}
	for _, v := range grid {
		fmt.Println(v)
	}
	fmt.Println(score)
	return grid, score, paddleX, ballX
}
