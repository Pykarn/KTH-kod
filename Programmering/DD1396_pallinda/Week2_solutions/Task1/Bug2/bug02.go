package main

import (
	"fmt"
	"time"
)

// This program should go to 11, but it seemingly only prints 1 to 10.
func main() {
	ch := make(chan int)
	wait := make(chan struct{}) //skapa en channel som allt måste vänta på
	go func() {
		Print(ch)
		close(wait) //skickar ut signal, "skakar hand" med <-wait
	}()

	for i := 1; i <= 11; i++ {
		ch <- i
	}
	close(ch)

	<-wait //väntar på att "skaka hand", krävs en signal
	//avslutar inte main tills goroutinen är klar
}

// Print prints all numbers sent on the channel.
// The function returns when the channel is closed.
func Print(ch <-chan int) {
	for n := range ch { // reads from channel until it's closed
		time.Sleep(10 * time.Millisecond) // simulate processing time
		fmt.Println(n)
	}
}
