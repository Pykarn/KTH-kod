package main

import "fmt"

func fibonacci() func() int {
	n0 := 0
	n1 := 1
	return func() int {
		//temp variabel n som sparar "första" värdet
		n := n0
		//n0 tilldelas n1 värdet och blir "nya" n1
		n0 = n1
		//n1 tilldelas värdet enligt fibonacci-sekvensen n(i+2) = n(i+1) + n(i)
		n1 = (n + n1)

		return n
	}

}

//0 1 1 2 3 5 8 13 21 34

func main() {
	fib := fibonacci()
	for i := 0; i < 10; i++ {
		fmt.Println(fib())
	}
}
