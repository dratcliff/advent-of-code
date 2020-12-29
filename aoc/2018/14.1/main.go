package main

import "container/list"
import "fmt"

func printList(l *list.List) {
	for e := l.Front(); e != nil; e = e.Next() {
		fmt.Print(e.Value)
	}
	fmt.Println()
}

/*
To create new recipes, the two Elves combine their current recipes. This creates new recipes from the digits of the sum of the current recipes' scores. With the current recipes' scores of 3 and 7, their sum is 10, and so two new recipes would be created: the first with score 1 and the second with score 0. If the current recipes' scores were 2 and 3, the sum, 5, would only create one recipe (with a score of 5) with its single digit.

The new recipes are added to the end of the scoreboard in the order they are created. So, after the first round, the scoreboard is 3, 7, 1, 0.

After all new recipes are added to the scoreboard, each Elf picks a new current recipe. To do this, the Elf steps forward through the scoreboard a number of recipes equal to 1 plus the score of their current recipe. So, after the first round, the first Elf moves forward 1 + 3 = 4 times, while the second Elf moves forward 1 + 7 = 8 times. If they run out of recipes, they loop back around to the beginning. After the first round, both Elves happen to loop around until they land on the same recipe that they had in the beginning; in general, they will move to different recipes.


*/
func main() {
	list := list.New()
	firstElf := list.PushFront(3)
	secondElf := list.PushBack(7)
	for i := 0; i < 20000000; i++ {
		fv := firstElf.Value.(int)
		sv := secondElf.Value.(int)
		if sv < 0 {
			sv = 0
		}
		sum := fv + sv
		firstElfValue, secondElfValue := 0, 0
		if sum > 9 {
			firstElfValue = 1
			secondElfValue = sum - 10
		} else {
			firstElfValue = sum
			secondElfValue = -1
		}
		list.PushBack(firstElfValue)
		if secondElfValue != -1 {
			list.PushBack(secondElfValue)
		}

		for i := 0; i <= fv; i++ {
			firstElf = firstElf.Next()
			if firstElf == nil {
				firstElf = list.Front()
			}
		}

		for i := 0; i <= sv; i++ {
			secondElf = secondElf.Next()
			if secondElf == nil {
				secondElf = list.Front()
			}
		}
	}

	i := 0
	e := list.Front()
	for {
		if e == nil {
			break
		}
		if e.Value.(int) == 5 {
			e = e.Next()
			i++
			if e == nil {
				break
			}
			if e.Value.(int) == 9 {
				e = e.Next()
				i++
				if e == nil {
					break
				}
				if e.Value.(int) == 8 {
					e = e.Next()
					i++
					if e == nil {
						break
					}
					if e.Value.(int) == 7 {
						e = e.Next()
						i++
						if e == nil {
							break
						}
						if e.Value.(int) == 0 {
							e = e.Next()
							i++
							if e == nil {
								break
							}
							if e.Value.(int) == 1 {
								fmt.Println(i - 5)
							}
						}
					}
				}
			}
		} else {
			i++
			e = e.Next()
		}
	}
}
