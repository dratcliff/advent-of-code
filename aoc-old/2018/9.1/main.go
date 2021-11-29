package main

import (
	"container/list"
	"fmt"
	"log"
)

func print(circles *list.List) {
	for i := circles.Front(); i != nil; i = i.Next() {
		fmt.Print(i.Value)
		fmt.Print(" ")
	}
	fmt.Println()
}

func remove(circles *list.List, currentElement *list.Element) (int, *list.Element) {
	i := 0
	var prev *list.Element
	for prev = currentElement.Prev(); prev != nil; prev = prev.Prev() {
		i++
		if i == 7 {
			break
		}
	}
	if i != 7 {
		prev = circles.Back()
		for j := 0; j < 7-i-1; j++ {
			prev = prev.Prev()
		}
	}
	next := prev.Next()
	removed := circles.Remove(prev)
	return removed.(int), next
}

func insert(circles *list.List, currentElement *list.Element, value int) *list.Element {
	var e *list.Element
	if currentElement.Next() == nil {
		e = circles.InsertAfter(value, circles.Front())
	} else {
		e = circles.InsertAfter(value, currentElement.Next())
	}
	return e
}

func run(players int, lastMarble int) int {
	scores := make(map[int]int, 0)
	player := 1

	circles := list.New()
	e := circles.PushBack(0)
	removed := 0
	for i := 1; i <= lastMarble; i++ {
		if i%23 == 0 {
			removed, e = remove(circles, e)
			_, ok := scores[player]
			if !ok {
				scores[player] = 0
			}
			scores[player] = scores[player] + removed + i
		} else {
			e = insert(circles, e, i)
		}
		if player == players {
			player = 1
		} else {
			player++
		}
	}
	max := 0
	for _, v := range scores {
		if v > max {
			max = v
		}
	}
	return max
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
	score = run(478, 7124000)
	fmt.Println(score)
}
