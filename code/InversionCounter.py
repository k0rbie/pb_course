class InversionCounter:
    def __init__(self, arr):
        self.__arr = arr

    def num_inver(self):
        return self.__inv_merge_sort(0, len(self.__arr) - 1)

    def __inv_merge_sort(self, l, r):
        if l == r:
            return 0
        m = r + l >> 1
        sw1 = self.__inv_merge_sort(l, m)
        sw2 = self.__inv_merge_sort(m + 1, r)
        swap_count = self.__merge(l, m, r)
        return sw1 + sw2 + swap_count

    def __merge(self, l1, r1, r2):
        i1 = l1
        i2 = r1 + 1
        new_arr = []
        swap_count = 0
        while i1 <= r1 and i2 <= r2:
            if self.__arr[i1] <= self.__arr[i2]:
                new_arr.append(self.__arr[i1])
                i1 += 1
            else:
                new_arr.append(self.__arr[i2])
                i2 += 1
                swap_count += r1 - i1 + 1
        self.__arr[l1:r2 + 1] = new_arr + self.__arr[i1:r1 + 1] + self.__arr[i2:r2 + 1]
        return swap_count
