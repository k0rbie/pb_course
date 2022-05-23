def num_inver(arr: list[16]):
    return inv_merge_sort(arr, 0, len(arr)-1)


def inv_merge_sort(arr, l, r):
    if l == r:
        return 0
    m = r + l >> 1
    sw1 = inv_merge_sort(arr, l, m)
    sw2 = inv_merge_sort(arr, m+1, r)
    arr[l:r+1], swap_count = merge(arr, l, m, r)
    return sw1 + sw2 + swap_count


def merge(arr, l1, r1, r2):
    i1 = l1
    i2 = r1 + 1
    new_arr = []
    swap_count = 0
    while i1 <= r1 and i2 <= r2:
        if arr[i1] <= arr[i2]:
            new_arr.append(arr[i1])
            i1 += 1
        else:
            new_arr.append(arr[i2])
            i2 += 1
            swap_count += r1 - i1 + 1
    new_arr += arr[i1:r1+1] + arr[i2:r2+1]
    return new_arr, swap_count

