"""
Singly linked list with insert, delete, and reverse.
Each node holds a value and points to the next node.
"""

class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def insert(self, value, position=None):
        """Insert a value. If no position given, add at the end."""
        new_node = Node(value)

        # inserting at the start
        if position == 0 or self.head is None:
            new_node.next = self.head
            self.head = new_node
            return

        # walk to the position before where we want to insert
        current = self.head
        index = 0
        while current.next is not None and (position is None or index < position - 1):
            current = current.next
            index += 1

        new_node.next = current.next
        current.next = new_node

    def delete(self, position):
        """Delete the node at the given position. Returns the deleted value."""
        if self.head is None:
            return None

        # deleting the head node
        if position == 0:
            val = self.head.value
            self.head = self.head.next
            return val

        # walk to the node just before the one we want to delete
        current = self.head
        for _ in range(position - 1):
            if current.next is None:
                return None  # position out of range
            current = current.next

        if current.next is None:
            return None

        val = current.next.value
        current.next = current.next.next
        return val

    def reverse(self):
        """Reverse the list in place by flipping all the next pointers."""
        prev = None
        current = self.head
        while current is not None:
            next_node = current.next  # save next
            current.next = prev       # flip pointer
            prev = current            # move prev forward
            current = next_node       # move current forward
        self.head = prev

    def to_list(self):
        """Convert the linked list to a Python list for easy inspection."""
        result = []
        current = self.head
        while current is not None:
            result.append(current.value)
            current = current.next
        return result

    def length(self):
        return len(self.to_list())

    def __repr__(self):
        return " -> ".join(str(v) for v in self.to_list()) + " -> None"
