package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
)

type lightPoint struct {
	x  int
	y  int
	xv int
	yv int
}

func points() []*lightPoint {
	file, err := os.Open("input.txt")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	lps := make([]*lightPoint, 0)
	for scanner.Scan() {
		line := scanner.Text()
		position := strings.Split(line, "<")[1]
		position = strings.Split(position, ">")[0]
		xpos := strings.Split(position, ",")[0]
		xpos = strings.Replace(xpos, " ", "", -1)
		x, _ := strconv.Atoi(xpos)
		ypos := strings.Split(position, ",")[1]
		ypos = strings.Replace(ypos, " ", "", -1)
		y, _ := strconv.Atoi(ypos)

		velocity := strings.Split(line, ">")[1]
		velocity = strings.Split(velocity, "<")[1]
		velocity = strings.Replace(velocity, " ", "", -1)
		xvel := strings.Split(velocity, ",")[0]
		yvel := strings.Split(velocity, ",")[1]
		xv, _ := strconv.Atoi(xvel)
		yv, _ := strconv.Atoi(yvel)
		lp := &lightPoint{x, y, xv, yv}
		lps = append(lps, lp)
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}
	return lps
}

func printGraphical(lps []*lightPoint, maxx int, maxy int, xoff int, yoff int) {
	grid := make([][]bool, maxy-yoff+1)
	for k, _ := range grid {
		grid[k] = make([]bool, maxx-xoff+1)
	}
	for _, v := range lps {
		grid[v.y-yoff][v.x-xoff] = true
	}

	for x, _ := range grid {
		for y, _ := range grid[x] {
			ok := grid[x][y]
			if ok {
				fmt.Print("X")
			} else {
				fmt.Print(".")
			}
		}
		fmt.Println()
	}
}

func max(lps []*lightPoint) (int, int) {
	maxx := 0
	maxy := 0
	for _, v := range lps {
		if v.x > maxx {
			maxx = v.x
		}
		if v.y > maxy {
			maxy = v.y
		}
	}
	return maxx, maxy
}

func min(lps []*lightPoint) (int, int) {
	minx := 999999
	miny := 999999
	for _, v := range lps {
		if v.x < minx {
			minx = v.x
		}
		if v.y < miny {
			miny = v.y
		}
	}
	return minx, miny
}

func printMsgWithSmallestArea(lps []*lightPoint) {
	minxd := 999999
	minyd := 999999

	for i := 0; i < 11000; i++ {
		for _, v := range lps {
			v.x = v.x + v.xv
			v.y = v.y + v.yv
		}
		minx, miny := min(lps)
		maxx, maxy := max(lps)
		if minx > 0 && miny > 0 {
			xd := maxx - minx
			yd := maxy - miny
			if xd < minxd && yd < minyd {
				minxd = xd
				minyd = yd
				print("\033[H\033[2J")
				printGraphical(lps, maxx, maxy, minx, miny)
			}
		}
	}

}

func main() {
	lps := points()
	printMsgWithSmallestArea(lps)
}
