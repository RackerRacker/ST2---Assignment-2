"""
Stack (LIFO) data structure.
Push adds to the top, pop removes from the top.
"""

class Stack:
    def __init__(self):
        # using a list internally - the end is the "top"
        self.items = []

    def push(self, item):
        """Add an item to the top of the stack."""
        self.items.append(item)

    def pop(self):
        """Remove and return the top item. Returns None if empty."""
        if self.is_empty():
            return None
        return self.items.pop()

    def peek(self):
        """Look at the top item without removing it."""
        if self.is_empty():
            return None
        return self.items[-1]

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

    def __repr__(self):
        return f"Stack({self.items})"
