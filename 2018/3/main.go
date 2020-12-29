package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
)

type claim struct {
	claimId             string
	startInchesFromTop  int
	startInchesFromLeft int
	width               int
	height              int
}

func claims() []claim {
	file, err := os.Open("input.txt")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	claims := make([]claim, 0)
	for scanner.Scan() {
		line := scanner.Text()
		records := strings.Split(line, " ")
		claimId := strings.SplitAfter(records[0], "#")[1]
		startPositions := strings.Split(records[2], ",")
		startTop := strings.Replace(startPositions[1], ":", "", -1)
		iStartTop, _ := strconv.Atoi(startTop)
		startLeft := startPositions[0]
		iStartLeft, _ := strconv.Atoi(startLeft)
		dimensions := strings.Split(records[3], "x")
		width, _ := strconv.Atoi(dimensions[0])
		height, _ := strconv.Atoi(dimensions[1])
		c := claim{claimId: claimId,
			startInchesFromTop:  iStartTop,
			startInchesFromLeft: iStartLeft,
			width:               width,
			height:              height}
		claims = append(claims, c)
	}
	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}
	return claims
}

func findOverlappingClaimCount(claims []claim) {
	fabric := make([][]int, 1000)
	for i, _ := range fabric {
		fabric[i] = make([]int, 1000)
	}

	for i, _ := range claims {
		c := claims[i]
		t := c.startInchesFromTop
		l := c.startInchesFromLeft
		w := c.width
		h := c.height

		for x := 0; x < w; x++ {
			for y := 0; y < h; y++ {
				fabric[l+x][y+t] = fabric[l+x][y+t] + 1
			}
		}
	}

	sum := 0
	for x := range fabric {
		for y := range fabric[x] {
			if fabric[x][y] > 1 {
				sum = sum + 1
			}
		}
	}
	fmt.Println(sum)
}

func main() {
	claims := claims()
	findOverlappingClaimCount(claims)
}
