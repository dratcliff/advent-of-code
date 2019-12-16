package main

import (
	"fmt"

	"github.com/twmb/algoimpl/go/graph"
)

type PointDiscovery interface {
	Point() Point
	Discovered() bool
}

type PD struct {
	p          Point
	discovered bool
}

func (pd PD) Point() Point {
	return pd.p
}

func (pd PD) Discovered() bool {
	return pd.discovered
}

func initGraph(g *graph.Graph, queue []graph.Node) ([]graph.Node, graph.Node) {
	root := g.MakeNode()
	*root.Value = PD{Point{0, 0}, true}
	r1 := g.MakeNode()
	*r1.Value = PD{Point{1, 0}, false}
	g.MakeEdge(root, r1)
	r2 := g.MakeNode()
	*r2.Value = PD{Point{-1, 0}, false}
	g.MakeEdge(root, r2)
	r3 := g.MakeNode()
	*r3.Value = PD{Point{0, -1}, false}
	g.MakeEdge(root, r3)
	r4 := g.MakeNode()
	*r4.Value = PD{Point{0, 1}, false}
	g.MakeEdge(root, r4)

	queue = append(queue, r1)
	queue = append(queue, r2)
	queue = append(queue, r3)
	queue = append(queue, r4)

	return queue, root
}

func Repair() {

	g := graph.New(graph.Undirected)
	queue := make([]graph.Node, 0)
	queue, root := initGraph(g, queue)
	if len(queue) == 0 {
		fmt.Println("Queue is empty !")
	}

	s := SingleLineFileToString("15.txt")
	j := StringToIntArray(s)
	input := 1
	count := 0
	amp := NewAmplifier(input, j, -1)

	currentNode := root
	lastInput := -1
	for {
		if len(queue) == 0 {
			break
		}
		nextNode := queue[0]
		queue = queue[1:]

		nextPoint := getPoint(nextNode)
		path := getPath(g, currentNode, nextPoint)

		for _, p := range path.Path {
			startPoint := getPoint(p.Start)
			endPoint := getPoint(p.End)
			nextInput := getNextInput(startPoint, endPoint)
			// fmt.Println("input is", nextInput)
			amp.setSingleInput(nextInput)
			r := amp.process()
			if len(r.outputs) == 0 {
				panic("no output")
			}
			if r.outputs[0] == 0 {
				g.RemoveNode(&p.End)
				// fmt.Println("can't move")
			}
			if r.outputs[0] == 1 {
				lastInput = nextInput
				currentNode = p.End
			}
			if r.outputs[0] == 2 {
				path := getPath(g, root, getPoint(p.End))
				fmt.Println("Length was", len(path.Path))
				fmt.Println(nextPoint.Point())
				search := g.DijkstraSearch(p.End)
				max := 0
				for _, s := range search {
					if len(s.Path) > max {
						max = len(s.Path)
					}
				}
				fmt.Println("max is", max)
				lastInput = nextInput
				currentNode = p.End
			}
			// fmt.Println("output", r.outputs)
		}
		if currentNode == nextNode {
			// fmt.Println("looks like we made it", nextPoint.Point())
			if lastInput != 1 {
				toDiscover := g.MakeNode()
				*toDiscover.Value = PD{Point{nextPoint.Point().X, nextPoint.Point().Y - 1}, false}
				g.MakeEdge(currentNode, toDiscover)
				queue = append(queue, toDiscover)
			}
			if lastInput != 2 {
				toDiscover := g.MakeNode()
				*toDiscover.Value = PD{Point{nextPoint.Point().X, nextPoint.Point().Y + 1}, false}
				g.MakeEdge(currentNode, toDiscover)
				queue = append(queue, toDiscover)
			}
			if lastInput != 3 {
				toDiscover := g.MakeNode()
				*toDiscover.Value = PD{Point{nextPoint.Point().X + 1, nextPoint.Point().Y}, false}
				g.MakeEdge(currentNode, toDiscover)
				queue = append(queue, toDiscover)
			}
			if lastInput != 4 {
				toDiscover := g.MakeNode()
				*toDiscover.Value = PD{Point{nextPoint.Point().X - 1, nextPoint.Point().Y}, false}
				g.MakeEdge(currentNode, toDiscover)
				queue = append(queue, toDiscover)
			}

		} else {
			// fmt.Println("Didn't make it", nextPoint.Point())
		}
	}
	fmt.Println("count", count)
}

func getNextInput(startPoint PointDiscovery, endPoint PointDiscovery) int {
	dx := endPoint.Point().X - startPoint.Point().X
	dy := endPoint.Point().Y - startPoint.Point().Y

	if dx == 1 {
		return 4
	}
	if dx == -1 {
		return 3
	}
	if dy == 1 {
		return 1
	}
	if dy == -1 {
		return 2
	}
	panic("Can't handle that direction")
}

func getPath(g *graph.Graph, currentNode graph.Node, dest PointDiscovery) graph.Path {
	paths := g.DijkstraSearch(currentNode)
	// fmt.Println("Paths length", len(paths))
	var path graph.Path
	for _, p := range paths {
		if len(p.Path) == 0 {
			continue
		}
		// fmt.Println("Path length", len(p.Path))
		endNode := p.Path[len(p.Path)-1]
		endPoint := getPoint(endNode.End)
		if endPoint.Point().X == dest.Point().X && endPoint.Point().Y == dest.Point().Y {
			path = p
		}
	}
	return path
}

func getPoint(n graph.Node) PointDiscovery {
	value := n.Value
	vp := *value
	p := vp.(PointDiscovery)
	return p
}
