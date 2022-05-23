from random import sample


def main():
    n = 9
    arr = sample(range(1, n+1), n)
    sorted_arr = bubble_sort(arr.copy())
    print(f"{arr}")
    print(f"{sorted_arr}")
    print(sum([abs(i-j) for (i, j) in zip(arr, sorted_arr)]))


def bubble_sort(arr):
    length = len(arr)
    count = 0
    for i in range(length-1):
        for j in range(length - i - 1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                count += 1
    print(f"{count=}")
    return arr


if __name__ == '__main__':
    main()
