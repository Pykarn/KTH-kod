package main

import (
	"fmt"
	"sync"
)

var a = 0

func addThousand(a *int, inc int, wg *sync.WaitGroup) {
	i := 0
	for i < 10000 {
		*a += inc
		i++
	}
	wg.Done()
}

func main() {
	wg := new(sync.WaitGroup)
	wg.Add(2)

	go addThousand(&a, 1, wg)
	go addThousand(&a, -1, wg)

	wg.Wait()

	// Vi vill få 0 utskrivet, men ibland får vi inte 0 utskrivet, varför då?
	fmt.Print(a, "\n")
}
