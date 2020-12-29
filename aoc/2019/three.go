package main

import (
	"strconv"
	"strings"
)

type Point struct {
	X int
	Y int
}

type Distance struct {
	Manhattan int
	Signal    int
}

func Three(firstPath string, secondPath string) Distance {
	var gridOne []Point
	var gridTwo []Point
	gridOne = walkPath(firstPath, gridOne)
	gridTwo = walkPath(secondPath, gridTwo)

	return manhattan(gridOne, gridTwo)
}

func manhattan(gridOne []Point, gridTwo []Point) Distance {
	length := 0
	if len(gridOne) > len(gridTwo) {
		length = len(gridOne)
	} else {
		length = len(gridTwo)
	}

	grid := make(map[Point]string, length)

	for _, v := range gridOne {
		grid[v] = "one"
	}
	for _, v := range gridTwo {
		val, ok := grid[v]
		if ok {
			if val == "one" {
				grid[v] = "both"
			}
		}
	}
	max := 999999
	maxSignal := max

	for k, v := range grid {
		if v == "both" {
			dx := k.X
			if dx < 0 {
				dx = -dx
			}
			dy := k.Y
			if dy < 0 {
				dy = -dy
			}
			distance := dx + dy
			if distance < max {
				max = distance
			}

			signalOne := getSignal(gridOne, k)
			signalTwo := getSignal(gridTwo, k)

			if signalOne+signalTwo < maxSignal {
				maxSignal = signalOne + signalTwo
			}
		}
	}

	return Distance{max, maxSignal}
}

func getSignal(grid []Point, pointToFind Point) int {
	for k, v := range grid {
		if v == pointToFind {
			return k + 1
		}
	}
	panic("didn't find it")
}

func walkPath(path string, grid []Point) []Point {
	currentX := 0
	currentY := 0
	instructions := strings.Split(path, ",")
	for _, v := range instructions {
		direction := string(v[0])
		distance, _ := strconv.Atoi(v[1:])
		if direction == "R" {
			for i := 1; i <= distance; i = i + 1 {
				grid = append(grid, Point{currentX + i, currentY})
			}
			currentX = currentX + distance
		} else if direction == "L" {
			for i := 1; i <= distance; i = i + 1 {
				grid = append(grid, Point{currentX - i, currentY})
			}
			currentX = currentX - distance
		} else if direction == "U" {
			for i := 1; i <= distance; i = i + 1 {
				grid = append(grid, Point{currentX, currentY + i})
			}
			currentY = currentY + distance
		} else if direction == "D" {
			for i := 1; i <= distance; i = i + 1 {
				grid = append(grid, Point{currentX, currentY - i})
			}
			currentY = currentY - distance
		}
	}
	return grid
}
