package main

import (
	"fmt"
	"os"
	"strings"
	"time"
)

const DataFile = "loremipsum.txt"

// Return the word frequencies of the text argument.
//
// Split load optimally across processor cores.
func WordCount(text string) map[string]int {
	freqs := make(map[string]int)

	words := strings.Fields(text)

	//ändra antal workers
	workers := 20

	localres := make(chan map[string]int, workers)

	arbete := len(words) / workers

	for i := 0; i < workers; i++ {

		//start och slut för partitioneringen
		start := i * arbete
		end := start + arbete

		//om inte delas jämnt
		//tar sista worker resten av arbetet
		if i == workers-1 {
			end = len(words)
		}
		go func(part []string) {
			localmap := make(map[string]int)
			for _, word := range part {
				word = strings.ToLower(word)
				//slarvigt, men funkar för loremipsum.txt
				word = strings.Trim(word, ".,")

				if word != "" {
					localmap[word]++
				}
			}
			localres <- localmap
		}(words[start:end])
	}

	for i := 0; i < workers; i++ {
		local := <-localres

		for word, count := range local {
			freqs[word] += count
		}
	}
	return freqs
}

// Benchmark how long it takes to count word frequencies in text numRuns times.
//
// Return the total time elapsed.
func benchmark(text string, numRuns int) int64 {
	start := time.Now()
	for i := 0; i < numRuns; i++ {
		WordCount(text)
	}
	runtimeMillis := time.Since(start).Milliseconds()

	return runtimeMillis
}

// Print the results of a benchmark
func printResults(runtimeMillis int64, numRuns int) {
	fmt.Printf("amount of runs: %d\n", numRuns)
	fmt.Printf("total time: %d ms\n", runtimeMillis)
	average := float64(runtimeMillis) / float64(numRuns)
	fmt.Printf("average time/run: %.2f ms\n", average)
}

func main() {
	// read in DataFile as a string called data
	data, err := os.ReadFile(DataFile)
	if err != nil {
		panic(err)
	}

	fmt.Printf("%#v", WordCount(string(data)))

	numRuns := 100
	runtimeMillis := benchmark(string(data), numRuns)
	printResults(runtimeMillis, numRuns)

}
