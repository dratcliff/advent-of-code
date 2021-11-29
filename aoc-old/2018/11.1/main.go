package main

import (
	"fmt"
)

/*
- Find the fuel cell's rack ID, which is its X coordinate plus 10.
- Begin with a power level of the rack ID times the Y coordinate.
- Increase the power level by the value of the grid serial number (your puzzle input).
- Set the power level to itself multiplied by the rack ID.
- Keep only the hundreds digit of the power level (so 12345 becomes 3; numbers with no hundreds digit become 0).
- Subtract 5 from the power level.

power level of 3,5 with serial number 8 should be 4
*/
func grid(size int) [][]int {
	grid := make([][]int, size)
	for x, _ := range grid {
		grid[x] = make([]int, size)
	}
	return grid
}

func getPowerLevel(xCoord int, yCoord int, serialNumber int) int {
	rackId := xCoord + 10
	powerLevel := rackId * yCoord
	powerLevel = powerLevel + serialNumber
	powerLevel = powerLevel * rackId
	if powerLevel < 100 {
		powerLevel = 0
	} else {
		powerLevel = (powerLevel / 100) % 10
	}
	powerLevel = powerLevel - 5
	return powerLevel
}

func test() {
	fmt.Println(getPowerLevel(3, 5, 8))
	fmt.Println(getPowerLevel(122, 79, 57))
	fmt.Println(getPowerLevel(217, 196, 39))
	fmt.Println(getPowerLevel(101, 153, 71))
}

func run(squareSize int, startingX int, startingY int) (int, int, int) {
	max := 0
	topLeftX := 0
	topLeftY := 0
	serialNumber := 1133
	for x := startingX; x < 302-squareSize; x++ {
		for y := startingY; y < 302-squareSize; y++ {
			total := 0
			k := 0
			for i := 0; i < squareSize; i++ {
				for j := 0; j < squareSize; j++ {
					p := getPowerLevel(x+i, y+j, serialNumber)
					total = total + p
				}

				k++
			}
			if total > max {
				max = total
				topLeftX = x
				topLeftY = y
			}
		}
	}
	return max, topLeftX, topLeftY
}

func main() {
	for i := 1; i <= 300; i++ {
		max, x, y := run(i, 1, 1)
		fmt.Println(max, x, y, i)
	}
}
