package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
)

func readFile() []string {
	file, err := os.Open("input_sorted.txt")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	lines := make([]string, 0)

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		lines = append(lines, scanner.Text())
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}
	return lines
}

func accumulateSleepTime(lines []string) map[string][]int {
	/*
		example entry:
		[1518-11-22 00:00] Guard #1699 begins shift
		[1518-11-22 00:28] falls asleep
		[1518-11-22 00:43] wakes up
	*/
	guardTimes := make(map[string][]int, 0)
	guard := ""
	sleepMinStart := 0
	sleepMinStop := 0

	for _, v := range lines {
		records := strings.Split(v, " ")
		//datePart := strings.Replace(records[0], "[", "", -1)
		timePart := strings.Replace(records[1], "]", "", -1)
		firstWord := records[2]

		if firstWord == "Guard" {
			guard = strings.Replace(records[3], "#", "", -1)
			_, ok := guardTimes[guard]
			if !ok {
				guardTimes[guard] = make([]int, 0)
			}
		} else {
			minutes, _ := strconv.Atoi(strings.Split(timePart, ":")[1])
			if firstWord == "falls" {
				sleepMinStart = minutes
			}
			if firstWord == "wakes" {
				sleepMinStop = minutes
				for i := sleepMinStart; i < sleepMinStop; i++ {
					guardTimes[guard] = append(guardTimes[guard], i)
				}
			}
		}
	}
	return guardTimes
}

func mode(ints []int) (int, int) {
	counts := make(map[int]int, 0)
	for _, v := range ints {
		_, ok := counts[v]
		if !ok {
			counts[v] = 0
		}
		counts[v] = counts[v] + 1
	}

	mode := 0
	occurs := 0
	for k, v := range counts {
		if v > occurs {
			mode = k
			occurs = v
		}
	}
	return mode, occurs
}

func main() {
	lines := readFile()
	guardTimes := accumulateSleepTime(lines)
	maxOccurs := 0
	guard := ""
	minute := 0

	for k, v := range guardTimes {
		mode, occurs := mode(v)
		if occurs > maxOccurs {
			maxOccurs = occurs
			guard = k
			minute = mode
		}
	}
	guardId, _ := strconv.Atoi(guard)
	fmt.Println(guardId * minute)
}
