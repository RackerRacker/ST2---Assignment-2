"""
Sorting algorithms as generators - each step yields the current array state
plus info about which indices are being compared/swapped.
This makes it easy to animate frame by frame in the visualiser.
"""

def bubble_sort_steps(arr):
    """
    Bubble sort - repeatedly compare adjacent pairs and swap if out of order.
    Bigger elements "bubble" to the end with each pass.
    """
    arr = arr.copy()
    n = len(arr)
    for i in range(n):
        for j in range(n - i - 1):
            # comparing j and j+1
            yield arr.copy(), j, j + 1, 'compare'
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                yield arr.copy(), j, j + 1, 'swap'
    yield arr.copy(), -1, -1, 'done'


def selection_sort_steps(arr):
    """
    Selection sort - find the minimum in the unsorted part and put it in place.
    Simple but does a lot of comparisons.
    """
    arr = arr.copy()
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            yield arr.copy(), min_idx, j, 'compare'
            if arr[j] < arr[min_idx]:
                min_idx = j
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            yield arr.copy(), i, min_idx, 'swap'
    yield arr.copy(), -1, -1, 'done'


def merge_sort_steps(arr):
    """
    Merge sort - divide and conquer. Split in half, sort each half, merge.
    Much faster than bubble/selection for large arrays.
    """
    arr = arr.copy()
    steps = []
    _merge_sort(arr, 0, len(arr) - 1, steps)
    for step in steps:
        yield step
    yield arr.copy(), -1, -1, 'done'


def _merge_sort(arr, left, right, steps):
    if left >= right:
        return
    mid = (left + right) // 2
    _merge_sort(arr, left, mid, steps)
    _merge_sort(arr, mid + 1, right, steps)
    _merge(arr, left, mid, right, steps)


def _merge(arr, left, mid, right, steps):
    left_part = arr[left:mid + 1]
    right_part = arr[mid + 1:right + 1]
    i = j = 0
    k = left
    while i < len(left_part) and j < len(right_part):
        steps.append((arr.copy(), left + i, mid + 1 + j, 'compare'))
        if left_part[i] <= right_part[j]:
            arr[k] = left_part[i]
            i += 1
        else:
            arr[k] = right_part[j]
            j += 1
        steps.append((arr.copy(), k, -1, 'place'))
        k += 1
    while i < len(left_part):
        arr[k] = left_part[i]
        steps.append((arr.copy(), k, -1, 'place'))
        i += 1
        k += 1
    while j < len(right_part):
        arr[k] = right_part[j]
        steps.append((arr.copy(), k, -1, 'place'))
        j += 1
        k += 1
