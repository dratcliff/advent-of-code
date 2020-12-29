package main

import (
	"strconv"

	"github.com/golang-collections/collections/stack"
	// "github.com/twmb/algoimpl/go/graph"
	"fmt"

	"github.com/twmb/algoimpl/go/graph"
)

func Vacuum() {
	s := SingleLineFileToString("resources/17.txt")
	software := StringToIntArray(s)
	amp := NewAmplifier(0, software, -1)
	r := amp.process()
	o := r.outputs
	for _, v := range o {
		fmt.Printf("%v", string(v))
	}

	grid := make([][]int, 40)
	for i, _ := range grid {
		grid[i] = make([]int, 48)
	}

	for i, v := range o {
		grid[i/48][i%48] = v
	}

	sum := 0
	for i := range grid {
		for j, w := range grid[i] {
			if string(w) == "^" {
				fmt.Println("starting position", i, j)
			}
			if w == 35 {
				if i > 0 && i < 39 && j > 0 && j < 47 {
					if grid[i-1][j] == 35 && grid[i+1][j] == 35 &&
						grid[i][j-1] == 35 && grid[i][j+1] == 35 {
						sum = sum + (i * j)
						// fmt.Println(i, j)
					}
				}
			}
		}
	}
	// fmt.Println(sum)
}

func Vacuum2() {
	s := SingleLineFileToString("resources/17.txt")
	software := StringToIntArray(s)
	amp := NewAmplifier(0, software, -1)
	r := amp.process()
	o := r.outputs
	for _, v := range o {
		fmt.Printf("%v", string(v))
	}

	grid := make([][]int, 40)
	for i, _ := range grid {
		grid[i] = make([]int, 48)
	}

	for i, v := range o {
		grid[i/48][i%48] = v
	}

	points := make([]Point, 0)

	// sum := 0
	for i := range grid {
		for j, w := range grid[i] {
			if string(w) == "^" {
				fmt.Println("starting position", i, j)
				grid[i][j] = 35
				points = append(points, Point{j, i})
			}
			vertical := 0
			horizontal := 0
			if w == 35 {
				if i-1 >= 0 {
					if grid[i-1][j] == 35 {
						vertical = vertical + 1
					}
				}
				if i+1 <= 39 {
					if grid[i+1][j] == 35 {
						vertical = vertical + 1
					}
				}
				if j-1 >= 0 {
					if grid[i][j-1] == 35 {
						horizontal = horizontal + 1
					}
				}
				if j+1 <= 47 {
					if grid[i][j+1] == 35 {
						horizontal = horizontal + 1
					}
				}
				if (horizontal > 0 && vertical > 0 || horizontal+vertical == 1) && horizontal+vertical != 4 {
					points = append(points, Point{j, i})
					fmt.Println(j, i, horizontal, vertical, string(grid[i][j]), string(w))
				}
			}
		}
	}

	potential := make(map[Point][]Point, 0)
	for _, p := range points {
		for _, q := range points {
			if p.X == q.X || p.Y == q.Y {
				if _, ok := potential[p]; ok {
					potential[p] = append(potential[p], q)
				} else {
					potential[p] = []Point{q}
				}
			}
		}
	}

	actual := make(map[Point][]Point, 0)
	for k, v := range potential {
		for _, w := range v {
			connected := true
			if k.X == w.X {
				if k.Y < w.Y {
					for i := k.Y + 1; i < w.Y; i = i + 1 {
						if grid[i][k.X] != 35 {
							connected = false
						}
					}
				} else {
					for i := k.Y - 1; i > w.Y; i = i - 1 {
						if grid[i][k.X] != 35 {
							connected = false
						}
					}
				}
			} else {
				if k.X < w.X {
					for i := k.X + 1; i < w.X; i = i + 1 {
						if grid[k.Y][i] != 35 {
							connected = false
						}
					}
				} else {
					for i := k.X - 1; i > w.X; i = i - 1 {
						if grid[k.Y][i] != 35 {
							connected = false
						}
					}
				}
			}
			if k.X == 18 && k.Y == 14 {
				fmt.Println("18, 14", w, connected)
			}
			if connected && k != w {
				fmt.Println(k, w, connected)
				if _, ok := actual[k]; ok {
					actual[k] = append(actual[k], w)
				} else {
					actual[k] = []Point{w}
				}
			}
		}
	}

	// actual = maxActual

	g := graph.New(graph.Undirected)
	nodesToPoints := make(map[graph.Node]Point, 0)
	pointsToNodes := make(map[Point]graph.Node, 0)
	for k, v := range actual {
		n := g.MakeNode()
		nodesToPoints[n] = k
		pointsToNodes[k] = n
		for _, x := range v {
			if x.X != k.X && x.Y != k.Y {
				panic("what")
			}
		}
	}

	for k, v := range actual {
		for _, w := range v {
			nk := pointsToNodes[k]
			nw := pointsToNodes[w]
			fmt.Println("k,w", k, w, nk, nw)
			g.MakeEdge(nk, nw)
		}
	}

	/*
			Algorithm for undirected graphs:

		    Start with an empty stack and an empty circuit (eulerian path).
		    - If all vertices have even degree - choose any of them.
		    - If there are exactly 2 vertices having an odd degree - choose one of them.
		    - Otherwise no euler circuit or path exists.
			If current vertex has no neighbors - add it to circuit, remove the last vertex from the stack
			and set it as the current one. Otherwise (in case it has neighbors) - add the vertex to the stack,
			take any of its neighbors, remove the edge between selected neighbor and that vertex, and set that neighbor as the current vertex.
		    Repeat step 2 until the current vertex has no more neighbors and the stack is empty.


		    Note that obtained circuit will be in reverse order - from end vertex to start vertex.

	*/

	stack := stack.New()
	circuit := make([]Point, 0)
	instructions := []string{}

	current := pointsToNodes[Point{6, 14}]
	currentPoint := Point{6, 14}
	nextPoint := currentPoint
	currentDirection := Up
	nextDirection := Up

	fmt.Println("start", current, len(pointsToNodes))

	for {
		neighbors := g.Neighbors(current)
		fmt.Println(currentPoint, len(neighbors))
		if neighbors == nil || len(neighbors) == 0 {

			circuit = append(circuit, nodesToPoints[current])
			if stack.Len() == 0 {
				break
			}
			current = stack.Pop().(graph.Node)
			currentPoint = nodesToPoints[current]
		} else {
			stack.Push(current)
			// c := nodesToPoints[current]
			// fmt.Println(c)
			var next graph.Node
			for _, v := range neighbors {
				next = v
				nextPoint = nodesToPoints[next]
				// fmt.Println("next is", nextPoint, len(neighbors))
				if nextPoint.X > currentPoint.X {
					switch currentDirection {
					case Up, Down:
						nextDirection = Right
						break
					default:
						continue
					}
				} else if nextPoint.X < currentPoint.X {
					switch currentDirection {
					case Up, Down:
						nextDirection = Left
						break
					default:
						continue
					}
				} else if nextPoint.Y < currentPoint.Y {
					switch currentDirection {
					case Left, Right:
						nextDirection = Up
						break
					default:
						continue
					}
				} else if nextPoint.Y > currentPoint.Y {
					switch currentDirection {
					case Left, Right:
						nextDirection = Down
						break
					default:
						continue
					}
				} else {
					panic("what!")
				}
			}
			// fmt.Println(currentPoint, nextPoint, currentDirection, nextDirection)

			g.RemoveEdge(next, current)
			g.RemoveEdge(current, next)
			current = next
			currentDirection = nextDirection
			currentPoint = nodesToPoints[current]
		}

	}

	fmt.Println(len(circuit))
	for k, v := range circuit {
		fmt.Println(k, v)
	}

	for i := len(circuit)/2 - 1; i >= 0; i-- {
		opp := len(circuit) - 1 - i
		circuit[i], circuit[opp] = circuit[opp], circuit[i]
	}

	currentDirection = Up

	for k, v := range circuit {
		if k+1 < len(circuit) {
			currentPoint := v
			nextPoint := circuit[k+1]
			if nextPoint.X > currentPoint.X {
				nextDirection = Right
			}
			if nextPoint.X < currentPoint.X {
				nextDirection = Left
			}
			if nextPoint.Y < currentPoint.Y {
				nextDirection = Up
			}
			if nextPoint.Y > currentPoint.Y {
				nextDirection = Down
			}
			distance := (currentPoint.X - nextPoint.X) + (currentPoint.Y - nextPoint.Y)
			if distance < 0 {
				distance = distance * -1
			}
			distanceString := strconv.Itoa(distance)
			switch currentDirection {
			case Up:
				if nextDirection == Right {
					instructions = append(instructions, ",R,"+distanceString)
				} else {
					instructions = append(instructions, ",L,"+distanceString)
				}
			case Down:
				if nextDirection == Right {
					instructions = append(instructions, ",L,"+distanceString)
				} else {
					instructions = append(instructions, ",R,"+distanceString)
				}
			case Left:
				if nextDirection == Up {
					instructions = append(instructions, ",R,"+distanceString)
				} else {
					instructions = append(instructions, ",L,"+distanceString)
				}
			case Right:
				if nextDirection == Up {
					instructions = append(instructions, ",L,"+distanceString)
				} else {
					instructions = append(instructions, ",R,"+distanceString)
				}
			}
			// fmt.Println(currentPoint, nextPoint, currentDirection, nextDirection)
			currentDirection = nextDirection
		}
	}

	instructionCounts := make(map[string]map[string]map[string]int, 0)

	for k, v := range instructions {
		if k < len(instructions)-2 {
			if _, ok := instructionCounts[v]; !ok {
				instructionCounts[v] = make(map[string]map[string]int, 0)
				instructionCounts[v][instructions[k+1]] = make(map[string]int, 0)
				instructionCounts[v][instructions[k+1]][instructions[k+2]] = 1
			} else if _, ok := instructionCounts[v][instructions[k+1]]; !ok {
				instructionCounts[v][instructions[k+1]] = make(map[string]int, 0)
				instructionCounts[v][instructions[k+1]][instructions[k+2]] = 1
			} else {
				instructionCounts[v][instructions[k+1]][instructions[k+2]] = instructionCounts[v][instructions[k+1]][instructions[k+1]] + 1
			}
		}
	}

	for k, v := range instructionCounts {
		fmt.Println(k, v)
	}
	for k, v := range instructions {
		fmt.Println(k, v)
	}

	fmt.Println(instructions)
}

func Vacuum3() {
	a := []byte("R,12,L,8,L,4,L,4\n")
	b := []byte("L,8,R,6,L,6\n")
	c := []byte("L,8,L,4,R,12,L,6,L,4\n")
	d := []byte("A,B,A,B,C,A,C,A,C,B\n")
	e := []byte("N\n")

	s := SingleLineFileToString("resources/17.txt")
	software := StringToIntArray(s)
	software[0] = 2
	amp := NewAmplifier(0, software, -1)
	inputs := make([]int, 0)
	for _, x := range d {
		inputs = append(inputs, int(x))
	}
	for _, x := range a {
		inputs = append(inputs, int(x))
	}
	for _, x := range b {
		inputs = append(inputs, int(x))
	}
	for _, x := range c {
		inputs = append(inputs, int(x))
	}
	for _, x := range e {
		inputs = append(inputs, int(x))
	}
	fmt.Println(inputs)

	amp.inputs = inputs
	r := amp.process()

	for _, x := range r.outputs {
		fmt.Printf("%v", string(x))
	}
	fmt.Println(r.outputs)
}
