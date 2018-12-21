package main

import (
	"testing"
)

/*
 |
 v
 |
*/
func TestDetermineTrackType(t *testing.T) {
	tr, cr := build("short.txt")
	determineTrackType(tr, cr)
}
