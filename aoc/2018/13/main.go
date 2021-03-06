package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"sort"
)

type currentState struct {
	allCarts     *carts
	allTracks    *tracks
	crashPresent bool
}

type cart struct {
	currentDirection string
	intersections    int
}

type coordinate struct {
	trackType string
}

type point struct {
	x int
	y int
}

type tracks map[int]map[int]coordinate
type carts map[int]map[int]cart

func build(filename string) currentState {
	file, err := os.Open(filename)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	tracks := make(tracks, 0)
	carts := make(carts, 0)
	i := 0
	for scanner.Scan() {
		line := scanner.Text()
		tracks[i] = make(map[int]coordinate, 0)
		for k, l := range line {
			value := string(l)
			direction := ""
			var c coordinate
			if value == "^" || value == "v" || value == ">" || value == "<" {
				ct := cart{value, 0}
				_, ok := carts[i]
				if !ok {
					carts[i] = make(map[int]cart, 0)
				}
				carts[i][k] = ct
				if value == "^" || value == "v" {
					// this is a hack, but the sample data doesn't require us to
					// worry about corners :)
					direction = "|"
				} else {
					direction = "-"
				}
				c = coordinate{direction}
			}
			if value == "\\" || value == "/" || value == "|" ||
				value == " " || value == "-" || value == "+" {
				c = coordinate{value}
			}

			tracks[i][k] = c
		}
		i++
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}
	return currentState{&carts, &tracks, false}
}

func boundaries(t tracks) (int, int) {
	x, y := 0, 0
	for k, _ := range t {
		if k > y {
			y = k
		}
		for j, _ := range t[k] {
			if j > x {
				x = j
			}
		}
	}
	return x, y
}

func moveLeft(cs currentState, x int, y int) currentState {
	ct := *cs.allCarts
	t := *cs.allTracks
	currentCart := ct[y][x]

	c, ok := ct[y][x-1]
	if ok {
		cs.crashPresent = true
		delete(ct[y], x-1)
		c.currentDirection = "X"
		ct[y][x-1] = c
		return cs
	}
	delete(ct[y], x)
	nextTrack := t[y][x-1]
	if nextTrack.trackType == "-" {
		currentCart.currentDirection = "<"
	} else if nextTrack.trackType == "/" {
		currentCart.currentDirection = "v"
	} else if nextTrack.trackType == "\\" {
		currentCart.currentDirection = "^"
	} else if nextTrack.trackType == "+" {
		direction := currentCart.intersections % 3
		if direction == 0 {
			currentCart.currentDirection = "v"
		} else if direction == 1 {
			currentCart.currentDirection = "<"
		} else {
			currentCart.currentDirection = "^"
		}
		currentCart.intersections = currentCart.intersections + 1
	}
	ct[y][x-1] = currentCart
	return cs

}

func moveRight(cs currentState, x int, y int) currentState {
	ct := *cs.allCarts
	t := *cs.allTracks
	currentCart := ct[y][x]

	c, ok := ct[y][x+1]
	if ok {
		cs.crashPresent = true
		delete(ct[y], x)
		c.currentDirection = "X"
		ct[y][x+1] = c
		return cs
	}
	delete(ct[y], x)
	nextTrack := t[y][x+1]
	if nextTrack.trackType == "-" {
		currentCart.currentDirection = ">"
	} else if nextTrack.trackType == "/" {
		currentCart.currentDirection = "^"
	} else if nextTrack.trackType == "\\" {
		currentCart.currentDirection = "v"
	} else if nextTrack.trackType == "+" {
		direction := currentCart.intersections % 3
		if direction == 0 {
			currentCart.currentDirection = "^"
		} else if direction == 1 {
			currentCart.currentDirection = ">"
		} else {
			currentCart.currentDirection = "v"
		}
		currentCart.intersections = currentCart.intersections + 1
	}

	ct[y][x+1] = currentCart
	return cs

}

func moveDown(cs currentState, x int, y int) currentState {
	ct := *cs.allCarts
	t := *cs.allTracks
	currentCart := ct[y][x]

	c, ok := ct[y+1][x]
	if ok {
		cs.crashPresent = true
		delete(ct[y], x)
		c.currentDirection = "X"
		ct[y+1][x] = c
		return cs
	}
	delete(ct[y], x)
	nextTrack := t[y+1][x]
	if nextTrack.trackType == "|" {
		currentCart.currentDirection = "v"
	} else if nextTrack.trackType == "/" {
		currentCart.currentDirection = "<"
	} else if nextTrack.trackType == "\\" {
		currentCart.currentDirection = ">"
	} else if nextTrack.trackType == "+" {
		direction := currentCart.intersections % 3
		if direction == 0 {
			currentCart.currentDirection = ">"
		} else if direction == 1 {
			currentCart.currentDirection = "v"
		} else {
			currentCart.currentDirection = "<"
		}
		currentCart.intersections = currentCart.intersections + 1
	}

	_, ok = ct[y+1]
	if !ok {
		ct[y+1] = make(map[int]cart, 0)
	}
	ct[y+1][x] = currentCart
	return cs

}

func moveUp(cs currentState, x int, y int) currentState {
	ct := *cs.allCarts
	t := *cs.allTracks
	currentCart := ct[y][x]

	c, ok := ct[y-1][x]
	if ok {
		cs.crashPresent = true
		delete(ct[y], x)
		c.currentDirection = "X"
		ct[y-1][x] = c
		return cs
	}
	delete(ct[y], x)
	nextTrack := t[y-1][x]
	if nextTrack.trackType == "|" {
		currentCart.currentDirection = "^"
	} else if nextTrack.trackType == "/" {
		currentCart.currentDirection = ">"
	} else if nextTrack.trackType == "\\" {
		currentCart.currentDirection = "<"
	} else if nextTrack.trackType == "+" {
		direction := currentCart.intersections % 3
		if direction == 0 {
			currentCart.currentDirection = "<"
		} else if direction == 1 {
			currentCart.currentDirection = "^"
		} else {
			currentCart.currentDirection = ">"
		}
		currentCart.intersections = currentCart.intersections + 1
	}

	_, ok = ct[y-1]
	if !ok {
		ct[y-1] = make(map[int]cart, 0)
	}
	ct[y-1][x] = currentCart
	return cs

}

func cartPoints(cs currentState) []point {
	points := make([]point, 0)
	ct := *cs.allCarts
	for y, _ := range ct {
		for x, _ := range ct[y] {
			points = append(points, point{x, y})
		}
	}
	return points
}

func tick(cs currentState) currentState {
	ct := *cs.allCarts
	points := cartPoints(cs)
	sort.SliceStable(points, func(i, j int) bool {
		return points[i].y < points[j].y && points[i].x < points[j].x
	})
	for _, p := range points {
		currentCart := ct[p.y][p.x]
		cd := currentCart.currentDirection
		if cd == "v" {
			cs = moveDown(cs, p.x, p.y)
		} else if cd == "^" {
			cs = moveUp(cs, p.x, p.y)
		} else if cd == ">" {
			cs = moveRight(cs, p.x, p.y)
		} else if cd == "<" {
			cs = moveLeft(cs, p.x, p.y)
		}
		if cs.crashPresent {
			return cs
		}
	}
	return cs
}

func printTracks(cs currentState) {
	tr := *cs.allTracks
	ct := *cs.allCarts
	x, y := boundaries(tr)
	for i := 0; i <= y; i++ {
		for j := 0; j <= x; j++ {
			c, ok := ct[i][j]
			if ok {
				fmt.Print(c.currentDirection)
			} else {
				fmt.Print(tr[i][j].trackType)
			}
		}
		fmt.Println()
	}

}

func main() {
	cs := build("input.txt")
	for {
		if cs.crashPresent {
			break
		}
		cs = tick(cs)
	}
	x, y := boundaries(*cs.allTracks)
	ct := *cs.allCarts
	for i := 0; i < y; i++ {
		for j := 0; j < x; j++ {
			c, ok := ct[i][j]
			if ok && c.currentDirection == "X" {
				fmt.Println("crash at", j, ",", i)
			}
		}
	}
}
