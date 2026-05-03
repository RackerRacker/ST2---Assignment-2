"""
Queue (FIFO) data structure.
Enqueue adds to the back, dequeue removes from the front.
"""
from collections import deque

class Queue:
    def __init__(self):
        # deque is efficient for adding/removing from both ends
        self.items = deque()

    def enqueue(self, item):
        """Add an item to the back of the queue."""
        self.items.append(item)

    def dequeue(self):
        """Remove and return the front item. Returns None if empty."""
        if self.is_empty():
            return None
        return self.items.popleft()

    def peek(self):
        """Look at the front item without removing it."""
        if self.is_empty():
            return None
        return self.items[0]

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

    def to_list(self):
        """Return items as a regular list (front to back)."""
        return list(self.items)

    def __repr__(self):
        return f"Queue({list(self.items)})"
