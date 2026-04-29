package main

import (
	"fmt"
	"sync"
	"time"
)

func main() {
	var mu sync.Mutex
	n := 10

	go func() {
		mu.Lock()
		defer mu.Unlock() //gör det i slutet
		if n != 0 {
			fmt.Println("division successful!: ", 10/n)

		}

	}()
	mu.Lock()
	n = 20
	mu.Unlock()
	go func() {
		mu.Lock()
		fmt.Println("n is now 20 and no longer need be used: ", n)
		n = 0
		mu.Unlock()
	}()
	time.Sleep(70 * time.Millisecond)
}
