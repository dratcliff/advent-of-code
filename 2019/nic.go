package main

import (
	"container/list"
	"fmt"
)

func NIC() {
	s := SingleLineFileToString("resources/23.txt")
	software := StringToIntArray(s)

	packetQueues := make(map[int]*list.List, 50)
	amps := make(map[int]*Amplifier, 50)
	for i := 0; i < 50; i = i + 1 {
		packetQueues[i] = list.New()
		amp := NewAmplifier(-2, software, -2)
		amp.inputs = []int{i}
		amps[i] = amp
	}

	done := false
	ys := make(map[int]bool, 0)

	for !done {
		tx := 0
		for j, v := range amps {
			r := v.process()
			if len(r.outputs) != 0 {
				for i := 0; i < len(r.outputs); i = i + 3 {
					tx = tx + 1
					packets := packetQueues[r.outputs[i]]
					if packets == nil {
						packets = list.New()
						packetQueues[r.outputs[i]] = packets
					}
					if r.outputs[i] == 255 {
						fmt.Println("pushback")
						packets.PushBack(Point{r.outputs[i+1], r.outputs[i+2]})
					} else {
						packets.PushFront(Point{r.outputs[i+1], r.outputs[i+2]})
					}
				}
			}
			if r.needInput {
				packets := packetQueues[j]
				if packets != nil {
					next := packets.Back()
					if next == nil {
						v.inputs = []int{-1}
					} else {
						nextPoint := next.Value.(Point)
						fmt.Println(nextPoint)
						tx = tx + 1
						v.inputs = []int{nextPoint.X, nextPoint.Y}
						packets.Remove(next)
					}
				}
			}

		}
		if tx == 0 {
			fmt.Println("network idle", packetQueues[255])
			nat := packetQueues[255]
			if nat != nil {
				p := nat.Back().Value.(Point)
				packetQueues[0].PushFront(p)
				if _, ok := ys[p.Y]; !ok {
					ys[p.Y] = true
				} else {
					fmt.Println("Already there", p)
					done = true
				}
			}
		}
	}
}
