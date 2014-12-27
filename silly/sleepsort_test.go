package silly

import "testing"

func TestSorting(t *testing.T) {
	toBeOrdered := []int{5, 6, 32, 1, 9, 0, 10}
	expected := []int{0, 1, 5, 6, 9, 10, 32}

	actual := SleepSort(toBeOrdered)
	if !areEqual(expected, actual) {
		t.Error("Expected ", expected, ", got ", actual)
	}
}

func areEqual(slice1, slice2 []int) bool {
	if len(slice1) != len(slice2) {
		return false
	}

	for i := range slice1 {
		if slice1[i] != slice2[i] {
			return false
		}
	}

	return true
}
