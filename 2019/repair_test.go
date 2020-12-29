package main

import (
	"fmt"
	"testing"

	"github.com/twmb/algoimpl/go/graph"
)

func TestRepair(t *testing.T) {
	Repair()
}

func TestGraph(t *testing.T) {
	g := graph.New(graph.Undirected)
	a := g.MakeNode()
	*a.Value = Point{0, 0}
	b := g.MakeNode()
	*b.Value = &Point{1, 0}
	c := g.MakeNode()
	*c.Value = &Point{2, 0}
	g.MakeEdge(a, b)
	g.MakeEdge(b, c)
	path := g.DijkstraSearch(c)
	for i, p := range path {
		for _, q := range p.Path {
			fmt.Println(i, *q.Start.Value, *q.End.Value)
		}
	}
}
