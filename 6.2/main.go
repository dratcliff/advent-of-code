package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
)

type point struct {
	id int
	x  int
	y  int
}

func points() []point {
	file, err := os.Open("input.txt")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	points := make([]point, 0)
	i := 0
	for scanner.Scan() {
		line := scanner.Text()
		records := strings.Split(line, ", ")
		x, _ := strconv.Atoi(records[0])
		y, _ := strconv.Atoi(records[1])
		points = append(points, point{i, x, y})
		i++
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}
	return points
}

func max(points []point) (int, int) {
	x := 0
	y := 0
	for _, p := range points {
		if p.x > x {
			x = p.x
		}
		if p.y > y {
			y = p.y
		}
	}
	return x, y
}

func abs(i int) int {
	if i < 0 {
		return i * -1
	}
	return i
}

func isClose(points []point, x int, y int, distance int) bool {
	totalDistance := 0
	for _, p := range points {
		d := abs(x-p.x) + abs(y-p.y)
		totalDistance = totalDistance + d
		if totalDistance > distance {
			return false
		}
	}
	return true
}

func calculate(points []point, x int, y int, distance int) []point {
	grid := make([][]int, x)
	for i := 0; i < x; i++ {
		grid[i] = make([]int, y)
	}

	closePoints := make([]point, 0)

	for i, _ := range grid {
		for j, _ := range grid[i] {
			isClose := isClose(points, i, j, distance)
			if isClose {
				closePoints = append(closePoints, point{0, i, j})
			}
		}
	}
	return closePoints
}

func main() {
	points := points()
	x, y := max(points)
	closePoints := calculate(points, x, y, 10000)
	fmt.Println(len(closePoints))
}
