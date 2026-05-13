import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import unittest
from logic.sorting import bubble_sort_steps, selection_sort_steps, merge_sort_steps
from logic.graph import Graph
from logic.heap_logic import MaxHeap


def _run_sort(gen):
    arr = []
    for step in gen:
        arr = step[0]   # first element is always the current array state
    return arr


class TestBubbleSort(unittest.TestCase):

    def test_sorts_correctly(self):
        """Bubble sort should sort [5,3,8,1,2] to [1,2,3,5,8]."""
        arr = [5, 3, 8, 1, 2]
        result = _run_sort(bubble_sort_steps(arr))
        self.assertEqual(result, sorted(arr))

    def test_already_sorted(self):
        """Already sorted arrays should stay the same."""
        arr = [1, 2, 3, 4, 5]
        result = _run_sort(bubble_sort_steps(arr))
        self.assertEqual(result, [1, 2, 3, 4, 5])

    def test_single_element(self):
        """Single-element array should be unchanged."""
        result = _run_sort(bubble_sort_steps([42]))
        self.assertEqual(result, [42])

    def test_reverse_sorted(self):
        """Worst case - reverse sorted input."""
        arr = [5, 4, 3, 2, 1]
        result = _run_sort(bubble_sort_steps(arr))
        self.assertEqual(result, [1, 2, 3, 4, 5])

    def test_steps_yield_compare_or_swap(self):
        """Every step should have action 'compare', 'swap', or 'done'."""
        for arr, i1, i2, action in bubble_sort_steps([3, 1, 2]):
            self.assertIn(action, ('compare', 'swap', 'done'))


class TestSelectionSort(unittest.TestCase):

    def test_sorts_correctly(self):
        """Selection sort should produce the same sorted result."""
        arr = [64, 25, 12, 22, 11]
        result = _run_sort(selection_sort_steps(arr))
        self.assertEqual(result, sorted(arr))

    def test_highlights_during_compare(self):
        """
        During a compare step, the two indices being compared
        should be valid array positions.
        """
        arr = [3, 1, 4, 1, 5]
        for state, i1, i2, action in selection_sort_steps(arr):
            if action == 'compare':
                self.assertGreaterEqual(i1, 0)
                self.assertGreaterEqual(i2, 0)
                self.assertLess(i1, len(state))
                self.assertLess(i2, len(state))


class TestMergeSort(unittest.TestCase):

    def test_sorts_correctly(self):
        """Merge sort should correctly sort any array."""
        arr = [38, 27, 43, 3, 9, 82, 10]
        result = _run_sort(merge_sort_steps(arr))
        self.assertEqual(result, sorted(arr))

    def test_empty_array(self):
        """Empty array should return empty."""
        result = _run_sort(merge_sort_steps([]))
        self.assertEqual(result, [])

    def test_original_not_mutated(self):
        """The original array should not be changed by the generator."""
        arr = [5, 3, 1]
        original = arr.copy()
        _run_sort(merge_sort_steps(arr))
        self.assertEqual(arr, original)


class TestGraph(unittest.TestCase):

    def setUp(self):
        """Build a simple graph:  A-B-C-D  with A-C shortcut."""
        self.g = Graph()
        self.g.add_edge('A', 'B')
        self.g.add_edge('B', 'C')
        self.g.add_edge('C', 'D')
        self.g.add_edge('A', 'C')

    def test_bfs_visits_all_nodes(self):
        """BFS from A should eventually visit all reachable nodes."""
        order = []
        for visited, current, queue, visited_set in self.g.bfs_steps('A'):
            order = visited
        self.assertEqual(sorted(order), ['A', 'B', 'C', 'D'])

    def test_bfs_visits_in_correct_order(self):
        """BFS from A should visit A first (it's the start)."""
        first_order = None
        for visited, current, queue, visited_set in self.g.bfs_steps('A'):
            first_order = visited
            break
        self.assertEqual(first_order[0], 'A')

    def test_dfs_visits_all_nodes(self):
        """DFS from A should also visit all nodes."""
        order = []
        for visited, current, stack, visited_set in self.g.dfs_steps('A'):
            order = visited
        self.assertEqual(sorted(order), ['A', 'B', 'C', 'D'])

    def test_dfs_order_matches_expected(self):
        """DFS from A - A should be the first visited."""
        first = None
        for visited, current, stack, visited_set in self.g.dfs_steps('A'):
            first = visited[0]
            break
        self.assertEqual(first, 'A')

    def test_add_and_check_edge(self):
        """Adding an edge should make both nodes neighbours of each other."""
        self.g.add_edge('X', 'Y')
        self.assertIn('Y', self.g.neighbours('X'))
        self.assertIn('X', self.g.neighbours('Y'))

    def test_no_duplicate_edges(self):
        """Adding the same edge twice should not create duplicates."""
        self.g.add_edge('A', 'B')  # already exists
        neighbours = self.g.neighbours('A')
        self.assertEqual(neighbours.count('B'), 1)


class TestHeap(unittest.TestCase):

    def setUp(self):
        self.heap = MaxHeap()

    def test_insert_and_peek_max(self):
        """After inserting values the root (peek) should always be the max."""
        for val in [10, 40, 30, 20]:
            self.heap.insert(val)
        self.assertEqual(self.heap.peek(), 40)

    def test_extract_max_order(self):
        """Extracting max repeatedly should give values in descending order."""
        for val in [5, 20, 10, 15]:
            self.heap.insert(val)
        extracted = [self.heap.extract_max() for _ in range(4)]
        self.assertEqual(extracted, [20, 15, 10, 5])

    def test_heap_property_maintained(self):
        """After every insert, the parent should be >= its children."""
        for val in [3, 9, 2, 6, 5, 1, 7]:
            self.heap.insert(val)
        h = self.heap.heap
        for i in range(1, len(h)):
            parent = (i - 1) // 2
            self.assertGreaterEqual(h[parent], h[i],
                msg=f"Heap property violated: h[{parent}]={h[parent]} < h[{i}]={h[i]}")

    def test_extract_from_empty(self):
        """Extracting from an empty heap should return None."""
        self.assertIsNone(self.heap.extract_max())

    def test_size_decreases_after_extract(self):
        """Size should go down by one each time we extract."""
        self.heap.insert(1)
        self.heap.insert(2)
        self.heap.extract_max()
        self.assertEqual(self.heap.size(), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
