package main

import "fmt"

// I want this program to print "Hello world!", but it doesn't work.
func main() {
	ch := make(chan string, 1) // skapa buffer storlek 1
	ch <- "Hello world!"       // eller lägga detta i goroutine så att den kan "skicka" och "ta emot" samtidigt
	fmt.Println(<-ch)
}
