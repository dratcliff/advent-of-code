package main

import (
	"fmt"
	"math/big"
	"time"
)

func partTwo() {
	start := time.Now()
	var numbers [1000001]*int32
	starting := []int32{3, 8, 9, 1, 2, 5, 4, 6, 7}

	for i := 0; i < 8; i++ {
		numbers[starting[i]] = &starting[i+1]
	}

	for i := 10; i < 1000000; i++ {
		j := int32(i + 1)
		numbers[i] = &j
	}
	numbers[1_000_000] = &starting[0]
	ten := int32(10)
	numbers[7] = &ten

	currentLabel := int32(3)
	currentPtr := numbers[currentLabel]
	var first, second, third, fourth, next int32
	for i := 0; i < 10_000_000; i++ {
		first = *currentPtr
		second = *numbers[first]
		third = *numbers[second]
		fourth = *numbers[third]
		next = currentLabel - 1
		// fmt.Println(currentLabel, first, second, third, next)
		for next == first || next == second || next == third {
			next--
		}
		if next == 0 {
			next = 1_000_000
		}
		numbers[currentLabel] = numbers[third]
		currentLabel = *numbers[third]
		numbers[third] = numbers[next]
		numbers[next] = currentPtr

		currentPtr = numbers[fourth]

	}
	var z1 big.Int
	var z2 big.Int
	z1.SetInt64(int64(*numbers[1]))
	z2.SetInt64(int64(*numbers[*numbers[1]]))

	var prod big.Int
	answer := prod.Mul(&z1, &z2)
	fmt.Println(answer)
	end := time.Now().Sub(start)
	fmt.Println("That took", end.Milliseconds(), "milliseconds")
}

func main() {
	partTwo()
}
