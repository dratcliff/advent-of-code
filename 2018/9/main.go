package main

import (
	"fmt"
	"log"
)

func getNextPosition(circles []int, currentPosition int) int {
	length := len(circles)
	nextPosition := currentPosition + 2
	if nextPosition > length {
		return 1
	}
	return nextPosition
}

func insert(circles []int, value int, position int) []int {
	if position == len(circles) {
		circles = append(circles, value)
	} else {
		first := circles[0:position]
		second := make([]int, len(circles[position:]))
		copy(second, circles[position:])
		circles = append(first, value)
		circles = append(circles, second...)
	}
	return circles
}

func remove(circles []int, currentPosition int) ([]int, int, int) {
	newPosition := currentPosition - 7
	if newPosition < 0 {
		newPosition = len(circles) + newPosition
	}
	removedMarble := circles[newPosition]
	circles = append(circles[:newPosition], circles[newPosition+1:]...)
	if newPosition > len(circles) {
		newPosition = 0
	}
	return circles, removedMarble, newPosition
}

func run(players int, lastMarble int) int {
	scores := make(map[int]int, 0)
	circles := []int{0, 1}
	nextPosition := 1
	player := 2
	removedMarble := 0
	newPosition := 0
	for i := 2; i <= lastMarble; i++ {
		if i%23 == 0 {
			_, ok := scores[player]
			if !ok {
				scores[player] = i
			} else {
				scores[player] = scores[player] + i
			}
			circles, removedMarble, newPosition = remove(circles, nextPosition)
			scores[player] = scores[player] + removedMarble
			nextPosition = newPosition
		} else {
			nextPosition = getNextPosition(circles, nextPosition)
			circles = insert(circles, i, nextPosition)
		}
		if player == players {
			player = 1
		} else {
			player++
		}
	}

	maxScore := 0
	for _, v := range scores {
		if v > maxScore {
			maxScore = v
		}
	}
	return maxScore
}

func check(score int, expected int) {
	if score != expected {
		log.Fatal("Should've been", expected)
	}
}

func main() {
	score := run(9, 25)
	check(score, 32)
	score = run(10, 1618)
	check(score, 8317)
	score = run(17, 1104)
	check(score, 2764)
	score = run(21, 6111)
	check(score, 54718)
	score = run(30, 5807)
	check(score, 37305)
	fmt.Println("all good")
	score = run(478, 71240)
	fmt.Println(score)
}
