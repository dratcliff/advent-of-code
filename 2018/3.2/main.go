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

func printClaimWithoutOverlap(fabric [][][]string) {
	unresolvableClaims := make(map[string]bool, 0)
	for x, _ := range fabric {
		for y, _ := range fabric[x] {
			claims := fabric[x][y]
			if len(claims) > 1 {
				for _, z := range claims {
					unresolvableClaims[z] = true
				}
			}
			if len(claims) == 1 {
				claim := claims[0]
				_, ok := unresolvableClaims[claim]
				if !ok || !unresolvableClaims[claim] {
					unresolvableClaims[claim] = false
				}
			}
		}
	}
	for k, v := range unresolvableClaims {
		if !v {
			fmt.Println(k)
		}
	}
}

func populateFabricReservations(claims []claim) [][][]string {
	fabric := make([][][]string, 1000)
	for i, _ := range fabric {
		fabric[i] = make([][]string, 1000)
		for j, _ := range fabric[i] {
			fabric[i][j] = make([]string, 0)
		}
	}

	for i, _ := range claims {
		c := claims[i]
		t := c.startInchesFromTop
		l := c.startInchesFromLeft
		w := c.width
		h := c.height

		for x := 0; x < w; x++ {
			for y := 0; y < h; y++ {
				fabric[l+x][y+t] = append(fabric[l+x][y+t], c.claimId)
			}
		}
	}
	return fabric
}

func main() {
	claims := claims()
	fabric := populateFabricReservations(claims)
	printClaimWithoutOverlap(fabric)
}
