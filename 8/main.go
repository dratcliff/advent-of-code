package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
)

type node struct {
	parent     *node
	children   []*node
	noChildren int
	noMetadata int
	metadata   []int
}

func intRecords() []int {
	file, err := os.Open("input.txt")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	var records []string
	for scanner.Scan() {
		line := scanner.Text()
		records = strings.Split(line, " ")
	}

	intRecords := make([]int, 0)
	for _, e := range records {
		i, _ := strconv.Atoi(e)
		intRecords = append(intRecords, i)
	}

	return intRecords
}

type recordHolder struct {
	recs []int
}

func buildTree(rh *recordHolder) *node {
	records := rh.recs
	nc := records[0]
	nm := records[1]
	children := make([]*node, 0)
	if nc == 0 {
		children := make([]*node, 0)
		md := records[2 : 2+nm]
		records = records[2+nm:]
		rh.recs = records
		return &node{nil, children, nc, nm, md}
	} else {
		parent := &node{nil, children, nc, nm, nil}
		records = rh.recs
		records = records[2:]
		rh.recs = records
		for i := 0; i < nc; i++ {
			parent.children = append(parent.children, buildTree(rh))
		}
		records = rh.recs
		md := records[0:nm]
		records = records[nm:]
		parent.metadata = md
		rh.recs = records
		return parent
	}
}

func sumMetadata(n *node) int {
	sum := 0
	for _, md := range n.metadata {
		sum = sum + md
	}
	for _, c := range n.children {
		sum = sum + sumMetadata(c)
	}
	return sum
}

func main() {
	intRecords := intRecords()
	rh := &recordHolder{intRecords}

	tree := buildTree(rh)
	sum := sumMetadata(tree)
	fmt.Println(sum)
}
