package main

import "fmt"

type Direction int

const (
	Up Direction = iota
	Down
	Left
	Right
)

type PaintColor int

const (
	White PaintColor = iota
	Black
)

type RobotLocation struct {
	Position    Point
	Orientation Direction
}

func (r *RobotLocation) turn(d Direction) {
	switch r.Orientation {
	case Up:
		if d == Left {
			r.Position.X = r.Position.X - 1
			r.Orientation = Left
		} else {
			r.Position.X = r.Position.X + 1
			r.Orientation = Right
		}
	case Down:
		if d == Left {
			r.Position.X = r.Position.X + 1
			r.Orientation = Right
		} else {
			r.Position.X = r.Position.X - 1
			r.Orientation = Left
		}
	case Left:
		if d == Left {
			r.Position.Y = r.Position.Y - 1
			r.Orientation = Down
		} else {
			r.Position.Y = r.Position.Y + 1
			r.Orientation = Up
		}
	case Right:
		if d == Left {
			r.Position.Y = r.Position.Y + 1
			r.Orientation = Up
		} else {
			r.Position.Y = r.Position.Y - 1
			r.Orientation = Down
		}
	}
}

func sizeX(tiles map[Point]PaintColor) (int, int) {
	size := 0
	min := 0
	for v := range tiles {
		if v.X > size {
			size = v.X
		}
		if v.X < min {
			min = v.X
		}
	}
	return size, min
}

func sizeY(tiles map[Point]PaintColor) (int, int) {
	size := 0
	min := 0

	for v := range tiles {
		if v.Y > size {
			size = v.Y
		}
		if v.Y < min {
			min = v.Y
		}
	}
	return size, min
}

func run() {
	s := SingleLineFileToString("resources/11.txt")
	program := StringToIntArray(s)
	amp := NewAmplifier(0, program, -1)
	amp.waiting = true

	onBlack := 0

	onWhite := 1

	amp.setSingleInput(onWhite)
	paintedTiles := make(map[Point]PaintColor)
	loc := RobotLocation{Point{0, 0}, Up}
	i := 0
	for {
		r := amp.process()
		i = i + 1
		colorOutput := r.outputs[0]
		if colorOutput == 0 {
			paintedTiles[loc.Position] = Black
		} else {
			paintedTiles[loc.Position] = White
		}
		directionOutput := r.outputs[1]
		if directionOutput == 0 {
			loc.turn(Left)
		} else {
			loc.turn(Right)
		}

		if val, ok := paintedTiles[loc.Position]; ok {
			if val == Black {
				amp.setSingleInput(onBlack)
			} else {
				amp.setSingleInput(onWhite)
			}
		} else {
			amp.setSingleInput(onBlack)
		}
		if r.index == -1 {
			break
		}
	}

	maxx, minx := sizeX(paintedTiles)
	maxy, miny := sizeY(paintedTiles)

	grid := make([][]int, maxy-miny+1)
	for i := range grid {
		grid[i] = make([]int, maxx-minx+1)
	}

	for k, v := range paintedTiles {
		i := 0
		if v == White {
			i = 1
		}
		grid[k.Y-miny][k.X-minx] = i
	}

	for i := len(grid) - 1; i >= 0; i = i - 1 {
		for j := 0; j < len(grid[i]); j = j + 1 {
			if grid[i][j] == 0 {
				fmt.Printf("%s", " ")
			} else {
				fmt.Printf("%s", "\u2588")
			}
		}
		fmt.Printf("%v", "\n")
	}
}
