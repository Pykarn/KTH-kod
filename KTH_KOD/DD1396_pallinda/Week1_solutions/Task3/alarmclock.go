package main

import (
	"fmt"
	"time"
)

func Remind(text string, delay time.Duration) {
	for {
		time.Sleep(delay)
		tid_nu := time.Now().Format("15:04:05")
		fmt.Println("The time is " + tid_nu + ": " + text)
	}
}

func main() {

	go Remind("Time to eat", 10*time.Second)
	go Remind("Time to work", 30*time.Second)
	go Remind("Time to sleep", 60*time.Second)

	select {}
	//var input string
	//fmt.Scanln(&input)
}
