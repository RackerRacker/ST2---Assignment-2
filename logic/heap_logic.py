"""
Max-Heap implementation.
Parent is always larger than its children.
Insert uses sift-up, extract-max uses sift-down.
"""

class MaxHeap:
    def __init__(self):
        self.heap = []

    def insert(self, value):
        """Add a value and sift it up to maintain heap property."""
        self.heap.append(value)
        self._sift_up(len(self.heap) - 1)

    def extract_max(self):
        """Remove and return the largest value (root). Returns None if empty."""
        if not self.heap:
            return None
        if len(self.heap) == 1:
            return self.heap.pop()
        # swap root with last, remove last, then sift down the new root
        max_val = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._sift_down(0)
        return max_val

    def peek(self):
        """Look at the max without removing it."""
        return self.heap[0] if self.heap else None

    def _sift_up(self, i):
        """Bubble the element at index i up until heap property is satisfied."""
        while i > 0:
            parent = (i - 1) // 2
            if self.heap[i] > self.heap[parent]:
                self.heap[i], self.heap[parent] = self.heap[parent], self.heap[i]
                i = parent
            else:
                break

    def _sift_down(self, i):
        """Push the element at index i down until heap property is satisfied."""
        n = len(self.heap)
        while True:
            largest = i
            left = 2 * i + 1
            right = 2 * i + 2
            if left < n and self.heap[left] > self.heap[largest]:
                largest = left
            if right < n and self.heap[right] > self.heap[largest]:
                largest = right
            if largest != i:
                self.heap[i], self.heap[largest] = self.heap[largest], self.heap[i]
                i = largest
            else:
                break

    def size(self):
        return len(self.heap)

    def is_empty(self):
        return len(self.heap) == 0

    def parent_idx(self, i):
        return (i - 1) // 2 if i > 0 else None

    def left_idx(self, i):
        idx = 2 * i + 1
        return idx if idx < len(self.heap) else None

    def right_idx(self, i):
        idx = 2 * i + 2
        return idx if idx < len(self.heap) else None
