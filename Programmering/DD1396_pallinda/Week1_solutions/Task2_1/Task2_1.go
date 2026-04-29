package main

import (
	"fmt"
)

func Solver(x float64) float64 {
	var z float64 = 3

	for i := 0; i < 100; i++ {
		z = z - ((z*z*z - x) / (3 * z * z))
	}
	return z
}

func main() {
	fmt.Println(Solver(26))
}
