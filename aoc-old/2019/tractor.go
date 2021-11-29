package main

func getAmp(x, y int, software []int) *Amplifier {
	amp := NewAmplifier(0, software, -1)
	amp.inputs = []int{x, y}
	return amp
}

func Tractor() (int, int) {
	s := SingleLineFileToString("resources/19.txt")
	software := StringToIntArray(s)
	x, y := 1, 100
	for {
		amp := getAmp(x, y, software)
		r := amp.process()
		if r.outputs[0] == 1 {
			amp = getAmp(x+99, y-99, software)
			r = amp.process()
			if r.outputs[0] == 1 {
				return x, y - 99
			} else {
				y = y + 1
			}
		} else {
			x = x + 1
		}
		if x > 10000 || y > 10000 {
			break
		}
	}
	return -1, -1
}
