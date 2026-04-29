package main

import (
	"fmt"
	"strings"
)

func WordCount(s string) map[string]int {
	// You will implement your solution here
	split_string := strings.Fields(s)
	num := len(split_string)

	word_map := make(map[string]int)
	for i := 0; i < num; i++ {

		word_map[split_string[i]]++
	}
	// The current return value is just a hint, you can replace it
	return word_map
}

func main() {
	fmt.Println(WordCount("The quick brown fox jumped over the lazy dog."))
}
