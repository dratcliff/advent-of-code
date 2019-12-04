package main

import (
	"strconv"
	"strings"
)

func IsValidPassword(digits int) bool {
	return HasDoubleOccurrence(digits) && IsNonDecreasing(digits)
}

func IsValidPasswordPartTwo(digits int) bool {
	return HasDoubleOccurrencePartTwo(digits) && IsNonDecreasing(digits)
}

func HasDoubleOccurrence(digits int) bool {
	s := strconv.Itoa(digits)
	for _, v := range s {
		occurs := strings.Count(s, string(v)+string(v))
		if occurs >= 1 {
			return true
		}
	}
	return false
}

func HasDoubleOccurrencePartTwo(digits int) bool {
	s := strconv.Itoa(digits)
	for _, v := range s {
		occurs := strings.Count(s, string(v)+string(v))
		if occurs == 1 {
			occurs = strings.Count(s, string(v)+string(v)+string(v))
			if occurs == 0 {
				return true
			}
		}
	}
	return false
}

func IsNonDecreasing(digits int) bool {
	s := strconv.Itoa(digits)
	current, _ := strconv.Atoi(string(s[0]))
	for _, v := range s {
		next, _ := strconv.Atoi(string(v))
		if next < current {
			return false
		}
		current = next
	}
	return true
}
