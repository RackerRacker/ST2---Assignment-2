import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import unittest
from logic.stack import Stack
from logic.queue_ds import Queue
from logic.linked_list import LinkedList
from logic.bst import BST


class TestStack(unittest.TestCase):

    def setUp(self):
        # fresh stack before each test
        self.stack = Stack()

    def test_push_increases_size(self):
        """Pushing items should increase the stack size."""
        self.stack.push(1)
        self.stack.push(2)
        self.assertEqual(self.stack.size(), 2)

    def test_pop_returns_last_pushed(self):
        """LIFO - the last thing pushed should be the first thing popped."""
        self.stack.push(10)
        self.stack.push(20)
        self.stack.push(30)
        self.assertEqual(self.stack.pop(), 30)  # 30 was pushed last

    def test_push_pop_sequence(self):
        """Push 3 items, pop 2 - stack should have 1 item left in correct order."""
        self.stack.push("a")
        self.stack.push("b")
        self.stack.push("c")
        self.stack.pop()   # removes 'c'
        self.stack.pop()   # removes 'b'
        self.assertEqual(self.stack.size(), 1)
        self.assertEqual(self.stack.peek(), "a")

    def test_pop_empty_returns_none(self):
        """Popping from an empty stack should return None, not crash."""
        result = self.stack.pop()
        self.assertIsNone(result)

    def test_is_empty(self):
        """New stack should be empty."""
        self.assertTrue(self.stack.is_empty())
        self.stack.push(99)
        self.assertFalse(self.stack.is_empty())

    def test_peek_does_not_remove(self):
        """Peek should show the top item without removing it."""
        self.stack.push(5)
        self.stack.push(10)
        self.assertEqual(self.stack.peek(), 10)
        self.assertEqual(self.stack.size(), 2)  # still 2 items


class TestQueue(unittest.TestCase):

    def setUp(self):
        self.queue = Queue()

    def test_enqueue_dequeue_fifo(self):
        """Queue is FIFO - first in, first out."""
        self.queue.enqueue(1)
        self.queue.enqueue(2)
        self.queue.enqueue(3)
        self.assertEqual(self.queue.dequeue(), 1)  # 1 was enqueued first
        self.assertEqual(self.queue.dequeue(), 2)

    def test_enqueue_dequeue_four_three(self):
        """Enqueue 4 items, dequeue 3 - FIFO order maintained."""
        for i in range(1, 5):
            self.queue.enqueue(i)
        for expected in [1, 2, 3]:
            self.assertEqual(self.queue.dequeue(), expected)
        self.assertEqual(self.queue.size(), 1)
        self.assertEqual(self.queue.peek(), 4)

    def test_dequeue_empty_returns_none(self):
        """Dequeuing from empty queue should return None."""
        self.assertIsNone(self.queue.dequeue())

    def test_size_tracks_correctly(self):
        """Size should update with enqueue and dequeue."""
        self.queue.enqueue("x")
        self.queue.enqueue("y")
        self.assertEqual(self.queue.size(), 2)
        self.queue.dequeue()
        self.assertEqual(self.queue.size(), 1)

    def test_to_list_order(self):
        """to_list should reflect the queue order front-to-back."""
        self.queue.enqueue("a")
        self.queue.enqueue("b")
        self.queue.enqueue("c")
        self.assertEqual(self.queue.to_list(), ["a", "b", "c"])


class TestLinkedList(unittest.TestCase):

    def setUp(self):
        self.ll = LinkedList()

    def test_insert_at_end(self):
        """Inserting without a position should append to the end."""
        self.ll.insert(1)
        self.ll.insert(2)
        self.ll.insert(3)
        self.assertEqual(self.ll.to_list(), [1, 2, 3])

    def test_insert_at_position(self):
        """Insert node with value 10 at position 2."""
        self.ll.insert(1)
        self.ll.insert(2)
        self.ll.insert(4)
        self.ll.insert(10, position=2)   # 1 -> 2 -> 10 -> 4
        self.assertEqual(self.ll.to_list()[2], 10)

    def test_delete_node(self):
        """Deleting at position 1 should remove the correct node."""
        self.ll.insert(5)
        self.ll.insert(10)
        self.ll.insert(15)
        deleted = self.ll.delete(1)
        self.assertEqual(deleted, 10)
        self.assertEqual(self.ll.to_list(), [5, 15])

    def test_reverse(self):
        """Reversing the list should flip the order."""
        self.ll.insert(1)
        self.ll.insert(2)
        self.ll.insert(3)
        self.ll.reverse()
        self.assertEqual(self.ll.to_list(), [3, 2, 1])

    def test_delete_empty_returns_none(self):
        """Deleting from empty list should return None."""
        self.assertIsNone(self.ll.delete(0))


class TestBST(unittest.TestCase):

    def setUp(self):
        self.bst = BST()

    def test_inorder_gives_sorted(self):
        """Inorder traversal of a BST always gives sorted order."""
        for val in [50, 30, 70]:
            self.bst.insert(val)
        self.assertEqual(self.bst.inorder(), [30, 50, 70])

    def test_bst_insert_and_inorder_traversal(self):
        """Insert [50, 30, 70] and verify inorder traversal is 30, 50, 70."""
        self.bst.insert(50)
        self.bst.insert(30)
        self.bst.insert(70)
        self.assertEqual(self.bst.inorder(), [30, 50, 70])

    def test_preorder(self):
        """Preorder visits root first."""
        for val in [50, 30, 70]:
            self.bst.insert(val)
        pre = self.bst.preorder()
        self.assertEqual(pre[0], 50)  # root should be first

    def test_postorder(self):
        """Postorder visits root last."""
        for val in [50, 30, 70]:
            self.bst.insert(val)
        post = self.bst.postorder()
        self.assertEqual(post[-1], 50)  # root should be last

    def test_search_found(self):
        """Search should find values that were inserted."""
        self.bst.insert(50)
        self.bst.insert(25)
        self.assertTrue(self.bst.search(25))

    def test_search_not_found(self):
        """Search should return False for values not in the tree."""
        self.bst.insert(50)
        self.assertFalse(self.bst.search(99))

    def test_duplicates_ignored(self):
        """Inserting the same value twice should not add duplicates."""
        self.bst.insert(10)
        self.bst.insert(10)
        self.assertEqual(self.bst.inorder(), [10])


if __name__ == "__main__":
    unittest.main(verbosity=2)
