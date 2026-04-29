package main

import (
	"fmt"
	"math/rand"
	"time"
)

func quickSort(arr []int, low, high int) []int {
	if low < high {
		var pivot int
		arr, pivot = partition(arr, low, high)
		arr = quickSort(arr, low, pivot-1)
		arr = quickSort(arr, pivot+1, high)
	}
	return arr
}

func partition(arr []int, low, high int) ([]int, int) {
	pivot := arr[high]
	i := low
	for j := low; j < high; j++ {
		if arr[j] < pivot {
			arr[i], arr[j] = arr[j], arr[i]
			i++
		}
	}
	arr[i], arr[high] = arr[high], arr[i]
	return arr, i
}

// mainfunktion för att debugga
func main() {
	rand.Seed(time.Now().Unix())
	// skapa en array med slumpvalda tal av storlek 10000
	arr := rand.Perm(1000)
	fmt.Println("Börjar sortera...")
	start := time.Now()
	quickSort(arr, 0, len(arr)-1)
	duration := time.Since(start)
	fmt.Println("Klar! Sorteringen tog: ", duration.Microseconds(), " Mikrosekunder")
}
