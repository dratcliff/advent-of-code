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

func nearest(points []point, x int, y int) (point, bool) {
	distance := -1
	var pt point
	unique := true

	counts := make(map[int]int, 0)

	for _, p := range points {
		d := abs(x-p.x) + abs(y-p.y)
		if distance == -1 {
			distance = d
			counts[d] = 1
		}
		if d <= distance {
			_, ok := counts[d]
			if !ok {
				counts[d] = 1
			} else {
				counts[d] = counts[d] + 1
			}
			distance = d
			pt = p
		}
	}
	if counts[distance] > 1 {
		unique = false
	}
	return pt, unique
}

func removeUnbounded(grid [][]int, counts map[int]int) {
	width := len(grid)
	height := len(grid[0])

	for i := 0; i < width; i++ {
		id := grid[i][0]
		_, ok := counts[id]
		if ok {
			counts[id] = 0
		}
		id = grid[i][height-1]
		_, ok = counts[id]
		if ok {
			counts[id] = 0
		}
	}

	for i := 0; i < height; i++ {
		id := grid[0][i]
		_, ok := counts[id]
		if ok {
			counts[id] = 0
		}
		id = grid[width-1][i]
		_, ok = counts[id]
		if ok {
			counts[id] = 0
		}
	}
}

func calculate(points []point, x int, y int) map[int]int {
	grid := make([][]int, x)
	for i := 0; i < x; i++ {
		grid[i] = make([]int, y)
	}

	counts := make(map[int]int, 0)

	for i, _ := range grid {
		for j, _ := range grid[i] {
			n, unique := nearest(points, i, j)
			if unique {
				grid[i][j] = n.id
				_, ok := counts[n.id]
				if !ok {
					counts[n.id] = 1
				} else {
					counts[n.id] = counts[n.id] + 1
				}
			}
		}
	}

	removeUnbounded(grid, counts)
	return counts
}

func highestValue(counts map[int]int) int {
	biggest := 0
	for _, v := range counts {
		if v > biggest {
			biggest = v
		}
	}
	return biggest
}

func main() {
	points := points()
	x, y := max(points)
	counts := calculate(points, x, y)
	biggest := highestValue(counts)
	fmt.Println(biggest)
}
