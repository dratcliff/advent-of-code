package main

import (
	"fmt"
	"testing"
)

func TestTractor(t *testing.T) {
	x, y := Tractor()
	fmt.Println(x*10000 + y)
}
