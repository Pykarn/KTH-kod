package main

import (
	"fmt"
)

func main() {
	wait := make(chan struct{})
	n := 2

	go func() {
		n = n * 2
		n = n * 2
		close(wait)
	}()

	<-wait
	n++
	n = n + 4
	n = n + 1

	fmt.Println(n) // utdata: ???
}
