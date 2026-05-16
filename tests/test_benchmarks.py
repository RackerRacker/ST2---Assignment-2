"""
test_benchmarks.py - Performance benchmarking for all three phases.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import unittest
import time
import random

from logic.stack        import Stack
from logic.queue_ds     import Queue
from logic.linked_list  import LinkedList
from logic.bst          import BST
from logic.sorting      import bubble_sort_steps, selection_sort_steps, merge_sort_steps
from logic.graph        import Graph
from logic.heap_logic   import MaxHeap
from logic.pathfinding  import dijkstra_steps, astar_steps, dp_grid_paths


def time_generator(gen):
    start = time.perf_counter()
    for _ in gen:
        pass
    return time.perf_counter() - start


def time_func(func, *args, **kwargs):
    start = time.perf_counter()
    func(*args, **kwargs)
    return time.perf_counter() - start


def open_grid(rows, cols):
    return [[0] * cols for _ in range(rows)]


# Phase 1 benchmarks - Data Structures

class BenchmarkPhase1(unittest.TestCase):
    """
    Benchmark basic data structure operations at different scales.
    """

    def test_stack_benchmark(self):
        print("\n--- Stack Benchmark ---")
        for n in [100, 1000, 10000]:
            s = Stack()
            start = time.perf_counter()
            for i in range(n):
                s.push(i)
            for i in range(n):
                s.pop()
            elapsed = time.perf_counter() - start
            print(f"  n={n:<6}  push+pop all  ->  {elapsed:.6f}s")
            self.assertLess(elapsed, 5.0, f"Stack too slow at n={n}")

    def test_queue_benchmark(self):
        print("\n--- Queue Benchmark ---")
        for n in [100, 1000, 10000]:
            q = Queue()
            start = time.perf_counter()
            for i in range(n):
                q.enqueue(i)
            for i in range(n):
                q.dequeue()
            elapsed = time.perf_counter() - start
            print(f"  n={n:<6}  enqueue+dequeue all  ->  {elapsed:.6f}s")
            self.assertLess(elapsed, 5.0, f"Queue too slow at n={n}")

    def test_linked_list_benchmark(self):
        print("\n--- Linked List Benchmark ---")
        for n in [100, 500, 1000]:
            ll = LinkedList()
            start = time.perf_counter()
            for i in range(n):
                ll.insert(i)
            ll.reverse()
            elapsed = time.perf_counter() - start
            print(f"  n={n:<6}  insert all + reverse  ->  {elapsed:.6f}s")
            self.assertLess(elapsed, 5.0, f"LinkedList too slow at n={n}")

    def test_bst_benchmark(self):
        print("\n--- BST Benchmark ---")
        for n in [100, 500, 1000]:
            bst = BST()
            values = random.sample(range(n * 10), n)
            start = time.perf_counter()
            for v in values:
                bst.insert(v)
            bst.inorder()
            elapsed = time.perf_counter() - start
            print(f"  n={n:<6}  insert all + inorder  ->  {elapsed:.6f}s")
            self.assertLess(elapsed, 5.0, f"BST too slow at n={n}")


# Phase 2 benchmarks - Sorting, Graph, Heap

class BenchmarkPhase2Sorting(unittest.TestCase):
    """
    Compare sorting algorithm performance at different array sizes.
    Bubble and selection are O(n^2) so they get slower fast.
    Merge sort is O(n log n) so it handles larger inputs well.
    """

    def _run_sort(self, gen):
        for _ in gen:
            pass

    def test_bubble_sort_benchmark(self):
        print("\n--- Bubble Sort Benchmark ---")
        for n in [50, 100, 300]:
            arr = random.sample(range(n * 10), n)
            start = time.perf_counter()
            self._run_sort(bubble_sort_steps(arr))
            elapsed = time.perf_counter() - start
            print(f"  n={n:<5}  ->  {elapsed:.6f}s")
            self.assertLess(elapsed, 10.0, f"Bubble sort too slow at n={n}")

    def test_selection_sort_benchmark(self):
        print("\n--- Selection Sort Benchmark ---")
        for n in [50, 100, 300]:
            arr = random.sample(range(n * 10), n)
            start = time.perf_counter()
            self._run_sort(selection_sort_steps(arr))
            elapsed = time.perf_counter() - start
            print(f"  n={n:<5}  ->  {elapsed:.6f}s")
            self.assertLess(elapsed, 10.0, f"Selection sort too slow at n={n}")

    def test_merge_sort_benchmark(self):
        print("\n--- Merge Sort Benchmark ---")
        for n in [100, 500, 1000]:
            arr = random.sample(range(n * 10), n)
            start = time.perf_counter()
            self._run_sort(merge_sort_steps(arr))
            elapsed = time.perf_counter() - start
            print(f"  n={n:<5}  ->  {elapsed:.6f}s")
            self.assertLess(elapsed, 10.0, f"Merge sort too slow at n={n}")

    def test_sorting_comparison(self):
        n = 200
        arr = random.sample(range(2000), n)

        start = time.perf_counter()
        self._run_sort(bubble_sort_steps(arr[:]))
        bubble_time = time.perf_counter() - start

        start = time.perf_counter()
        self._run_sort(merge_sort_steps(arr[:]))
        merge_time = time.perf_counter() - start

        print(f"\n--- Sorting Comparison n={n} ---")
        print(f"  Bubble Sort  ->  {bubble_time:.6f}s")
        print(f"  Merge Sort   ->  {merge_time:.6f}s")

        # merge sort should win on n=200
        self.assertLess(merge_time, bubble_time,
                        "Merge sort should be faster than bubble sort at n=200")


class BenchmarkPhase2Graph(unittest.TestCase):

    def _build_graph(self, n):
        """Build a connected chain graph: 0-1-2-...-n with some cross edges."""
        g = Graph()
        for i in range(n - 1):
            g.add_edge(str(i), str(i + 1))
        # add some extra edges to make it more interesting
        for i in range(0, n - 2, 3):
            g.add_edge(str(i), str(i + 2))
        return g

    def test_bfs_benchmark(self):
        print("\n--- BFS Benchmark ---")
        for n in [10, 50, 100]:
            g = self._build_graph(n)
            start = time.perf_counter()
            for _ in g.bfs_steps('0'):
                pass
            elapsed = time.perf_counter() - start
            print(f"  nodes={n:<5}  ->  {elapsed:.6f}s")
            self.assertLess(elapsed, 5.0, f"BFS too slow at n={n}")

    def test_dfs_benchmark(self):
        print("\n--- DFS Benchmark ---")
        for n in [10, 50, 100]:
            g = self._build_graph(n)
            start = time.perf_counter()
            for _ in g.dfs_steps('0'):
                pass
            elapsed = time.perf_counter() - start
            print(f"  nodes={n:<5}  ->  {elapsed:.6f}s")
            self.assertLess(elapsed, 5.0, f"DFS too slow at n={n}")

    def test_bfs_vs_dfs_same_result(self):
        """BFS and DFS should visit the same set of nodes, just in different order."""
        g = self._build_graph(20)
        bfs_visited = set()
        dfs_visited = set()
        for visited, *_ in g.bfs_steps('0'):
            bfs_visited = set(visited)
        for visited, *_ in g.dfs_steps('0'):
            dfs_visited = set(visited)
        self.assertEqual(bfs_visited, dfs_visited)


class BenchmarkPhase2Heap(unittest.TestCase):
    """Benchmark MaxHeap insert and extract at different sizes."""

    def test_heap_insert_benchmark(self):
        print("\n--- MaxHeap Insert Benchmark ---")
        for n in [100, 1000, 5000]:
            h = MaxHeap()
            values = random.sample(range(n * 10), n)
            start = time.perf_counter()
            for v in values:
                h.insert(v)
            elapsed = time.perf_counter() - start
            print(f"  n={n:<5}  insert all  ->  {elapsed:.6f}s")
            self.assertLess(elapsed, 5.0, f"Heap insert too slow at n={n}")

    def test_heap_extract_benchmark(self):
        print("\n--- MaxHeap Extract Benchmark ---")
        for n in [100, 1000, 5000]:
            h = MaxHeap()
            for v in random.sample(range(n * 10), n):
                h.insert(v)
            start = time.perf_counter()
            while h.size() > 0:
                h.extract_max()
            elapsed = time.perf_counter() - start
            print(f"  n={n:<5}  extract all  ->  {elapsed:.6f}s")
            self.assertLess(elapsed, 5.0, f"Heap extract too slow at n={n}")


# Phase 3 benchmarks - Pathfinding and DP

class BenchmarkPhase3(unittest.TestCase):
    """
    Benchmark pathfinding algorithms on grids of increasing size.
    A* should generally be faster than Dijkstra because the heuristic
    guides it towards the goal more directly.
    """

    def test_dijkstra_benchmark(self):
        print("\n--- Dijkstra Benchmark ---")
        for size in [5, 10, 20]:
            grid = open_grid(size, size)
            start = time.perf_counter()
            for _ in dijkstra_steps(grid, (0, 0), (size - 1, size - 1)):
                pass
            elapsed = time.perf_counter() - start
            print(f"  grid={size}x{size}  ->  {elapsed:.6f}s")
            self.assertLess(elapsed, 10.0, f"Dijkstra too slow on {size}x{size}")

    def test_astar_benchmark(self):
        print("\n--- A* Benchmark ---")
        for size in [5, 10, 20]:
            grid = open_grid(size, size)
            start = time.perf_counter()
            for _ in astar_steps(grid, (0, 0), (size - 1, size - 1)):
                pass
            elapsed = time.perf_counter() - start
            print(f"  grid={size}x{size}  ->  {elapsed:.6f}s")
            self.assertLess(elapsed, 10.0, f"A* too slow on {size}x{size}")

    def test_astar_faster_than_dijkstra(self):

        size = 15
        grid = open_grid(size, size)

        start = time.perf_counter()
        for _ in dijkstra_steps(grid, (0, 0), (size - 1, size - 1)):
            pass
        dijk_time = time.perf_counter() - start

        start = time.perf_counter()
        for _ in astar_steps(grid, (0, 0), (size - 1, size - 1)):
            pass
        astar_time = time.perf_counter() - start

        print(f"\n--- Pathfinding Comparison {size}x{size} grid ---")
        print(f"  Dijkstra  ->  {dijk_time:.6f}s")
        print(f"  A*        ->  {astar_time:.6f}s")

        # A* should explore fewer nodes and be faster
        self.assertLessEqual(astar_time, dijk_time * 2,
                             "A* should not be significantly slower than Dijkstra")

    def test_dp_grid_benchmark(self):
        print("\n--- DP Grid Path Count Benchmark ---")
        for size in [5, 10, 20, 50]:
            grid = open_grid(size, size)
            start = time.perf_counter()
            dp_grid_paths(grid)
            elapsed = time.perf_counter() - start
            print(f"  grid={size}x{size}  ->  {elapsed:.6f}s")
            self.assertLess(elapsed, 5.0, f"DP grid too slow on {size}x{size}")


if __name__ == "__main__":
    unittest.main(verbosity=2)