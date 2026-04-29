// Stefan Nilsson 2013-03-13

// This program implements an ELIZA-like oracle (en.wikipedia.org/wiki/ELIZA).
package main

import (
	"bufio"
	"fmt"
	"math/rand"
	"os"
	"strings"
	"time"
)

const (
	star   = "Pythia"
	venue  = "Delphi"
	prompt = "> "
)

func main() {
	fmt.Printf("Welcome to %s, the oracle at %s.\n", star, venue)
	fmt.Println("Your questions will be answered in due time.")

	questions := Oracle()
	reader := bufio.NewReader(os.Stdin)
	for {
		fmt.Print(prompt)
		line, _ := reader.ReadString('\n')
		line = strings.TrimSpace(line)
		if line == "" {
			continue
		}
		fmt.Printf("%s heard: %s\n", star, line)
		questions <- line // The channel doesn't block.
	}
}

// Oracle returns a channel on which you can send your questions to the oracle.
// You may send as many questions as you like on this channel, it never blocks.
// The answers arrive on stdout, but only when the oracle so decides.
// The oracle also prints sporadic prophecies to stdout even without being asked.
func Oracle() chan<- string {
	questions := make(chan string)
	// TODO: Answer questions.
	// TODO: Make prophecies.
	// TODO: Print answers.
	answers := make(chan string)

	go func() {
		for i := range questions {
			go makeanswer(i, answers)
		}
	}()

	go func() {
		predictions := []string{
			"Tjenare",
			"Hejdå",
			"Hallå",
			"Hejsansvejsan",
		}
		for {
			time.Sleep(time.Duration(15+rand.Intn(5)) * time.Second)
			random := predictions[rand.Intn(len(predictions))]
			prophecy(random, answers)
		}
	}()

	go func() {
		for i := range answers {
			printanswer(i)
		}
	}()
	return questions
}

func makeanswer(question string, answer chan<- string) {
	time.Sleep(time.Duration(rand.Intn(2)) * time.Second)

	q := strings.ToLower(question) //gör allt lowercase

	if strings.Contains(q, "life") {
		answer <- "Ah, life... "
		return
	}

	if strings.Contains(q, "death") {
		answer <- "Death is inevitable... "
		return
	}

	if len(question)%2 == 0 {
		answer <- "Yes"
	} else {
		answer <- "No"
	}
}

func printanswer(answer string) {
	for _, letter := range answer {
		fmt.Printf("%c", letter)
		time.Sleep(150 * time.Millisecond)
	}
	fmt.Println()
	fmt.Printf("%s", prompt)

}

// This is the oracle's secret algorithm.
// It waits for a while and then sends a message on the answer channel.
// TODO: make it better.
func prophecy(question string, answer chan<- string) {
	// Keep them waiting. Pythia, the original oracle at Delphi,
	// only gave prophecies on the seventh day of each month.
	time.Sleep(time.Duration(2+rand.Intn(3)) * time.Second)

	// Find the longest word.
	longestWord := ""
	words := strings.Fields(question) // Fields extracts the words into a slice.
	for _, w := range words {
		if len(w) > len(longestWord) {
			longestWord = w
		}
	}

	// Cook up some pointless nonsense.
	nonsense := []string{
		"The moon is dark.",
		"The sun is bright.",
	}
	answer <- longestWord + "... " + nonsense[rand.Intn(len(nonsense))]
}
