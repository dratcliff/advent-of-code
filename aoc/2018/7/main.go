package main

import (
	"bufio"
	"errors"
	"fmt"
	"log"
	"os"
	"sort"
	"strings"
)

type vertexSet struct {
	vertices map[vertex]bool
}

func (v *vertexSet) add(_vertex vertex) {
	v.vertices[_vertex] = true
}

func (v *vertexSet) delete(_v *vertex) {
	for k, _ := range v.vertices {
		if k.name == _v.name {
			delete(v.vertices, k)
		}
	}
}

func (v *vertexSet) size() int {
	return len(v.vertices)
}

func newVertexSet() vertexSet {
	m := make(map[vertex]bool, 0)
	v := vertexSet{m}
	return v
}

type vertex struct {
	name       string
	inVertices *vertexSet
}

func (v *vertex) inDegree() int {
	return v.inVertices.size()
}

type graph struct {
	vertices map[string]*vertex
}

func (g *graph) getVertex(name string) (*vertex, bool) {
	v, ok := g.vertices[name]
	return v, ok
}

func (g *graph) addVertex(name string) {
	_, ok := g.vertices[name]
	if !ok {
		o := newVertexSet()
		v := &vertex{name: name, inVertices: &o}
		g.vertices[name] = v
	}
}

func (g *graph) removeVertex(v *vertex) {
	delete(g.vertices, v.name)
}

func (g *graph) addEdge(from string, to string) error {
	f, ok := g.vertices[from]
	if !ok {
		return errors.New(from + " not found")
	}
	t, ok := g.vertices[to]
	if !ok {
		return errors.New(to + " not found")
	}
	f.inVertices.add(*t)
	return nil
}

func (g *graph) removeEdge(from *vertex, to *vertex) {
	v, ok := g.vertices[from.name]
	if ok {
		v.inVertices.delete(to)
	}
}

func rules() graph {
	file, err := os.Open("sorted_cleaned_input.txt")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	m := make(map[string]*vertex, 0)
	rules := graph{m}
	for scanner.Scan() {
		rec := scanner.Text()
		recs := strings.Split(rec, " ")
		step := recs[1]
		dependsOn := recs[0]

		rules.addVertex(dependsOn)
		rules.addVertex(step)
		rules.addEdge(step, dependsOn)
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	return rules
}

func nextAvailable(g graph) (*vertex, bool) {
	candidates := make([]string, 0)
	for k, v := range g.vertices {
		if v.inDegree() == 0 {
			candidates = append(candidates, k)
		}
	}
	if len(candidates) == 0 {
		return nil, false
	}
	sort.Strings(candidates)
	return g.getVertex(candidates[0])
}

func markComplete(g graph, completedVertex *vertex) {
	for _, vertex := range g.vertices {
		g.removeEdge(vertex, completedVertex)
	}
	g.removeVertex(completedVertex)
}

func proceed(rules graph) {
	for {
		n, _ := nextAvailable(rules)
		if n == nil {
			break
		}
		markComplete(rules, n)
		fmt.Print(n.name)
	}
	fmt.Println()
}

func main() {
	rules := rules()
	proceed(rules)
}
