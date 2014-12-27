package silly

import (
	"time"
)

func SleepSort(toBeOrdered []int) []int {
	channel := make(chan int)

	for _, element := range toBeOrdered {
		go func(e int) {
			time.Sleep(time.Duration(e) * time.Millisecond)
			channel <- e
		}(element)
	}

	ordered := make([]int, len(toBeOrdered))
	for i := range toBeOrdered {
		ordered[i] = <-channel
	}

	return ordered
}
