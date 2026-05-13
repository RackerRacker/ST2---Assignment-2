import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import unittest
from logic.pathfinding import dijkstra_steps, astar_steps, dp_grid_paths


def _run_pathfinding(gen):
    last_visited = set()
    last_path = None
    for visited, current, path in gen:
        last_visited = visited
        if path is not None:
            last_path = path
    return last_visited, last_path


class TestDijkstra(unittest.TestCase):

    def _open_grid(self, rows, cols):
        """Helper to make a clear grid with no walls."""
        return [[0] * cols for _ in range(rows)]

    def test_finds_path_on_open_grid(self):
        """Dijkstra should find a path on a completely open grid."""
        grid = self._open_grid(5, 5)
        _, path = _run_pathfinding(dijkstra_steps(grid, (0, 0), (4, 4)))
        self.assertIsNotNone(path)
        self.assertEqual(path[0], (0, 0))
        self.assertEqual(path[-1], (4, 4))

    def test_no_path_when_blocked(self):
        """When the goal is completely surrounded by walls, no path should exist."""
        grid = self._open_grid(5, 5)
        # wall off the entire right side so we can't reach (4,4)
        for r in range(5):
            grid[r][4] = 1
        _, path = _run_pathfinding(dijkstra_steps(grid, (0, 0), (4, 4)))
        self.assertIsNone(path)

    def test_path_starts_and_ends_correctly(self):
        """Path should start at start and end at end."""
        grid = self._open_grid(4, 4)
        start, end = (0, 0), (3, 3)
        _, path = _run_pathfinding(dijkstra_steps(grid, start, end))
        self.assertEqual(path[0], start)
        self.assertEqual(path[-1], end)

    def test_path_cells_are_adjacent(self):
        """Every step in the path should be exactly one move away from the previous."""
        grid = self._open_grid(5, 5)
        _, path = _run_pathfinding(dijkstra_steps(grid, (0, 0), (4, 4)))
        for i in range(len(path) - 1):
            r1, c1 = path[i]
            r2, c2 = path[i + 1]
            # each step is 1 row or 1 column apart
            self.assertEqual(abs(r1 - r2) + abs(c1 - c2), 1)

    def test_path_avoids_walls(self):
        """The path should never go through a wall cell."""
        grid = self._open_grid(5, 5)
        grid[2][1] = 1  # put a wall in the middle
        grid[2][2] = 1
        _, path = _run_pathfinding(dijkstra_steps(grid, (0, 0), (4, 4)))
        if path:
            for r, c in path:
                self.assertEqual(grid[r][c], 0, f"Path went through wall at ({r},{c})!")


class TestAStar(unittest.TestCase):

    def _open_grid(self, rows, cols):
        return [[0] * cols for _ in range(rows)]

    def test_finds_same_path_as_dijkstra(self):
        """On an unweighted grid, A* and Dijkstra should find the same path length."""
        grid = self._open_grid(5, 5)
        _, path_dijk = _run_pathfinding(dijkstra_steps(grid, (0, 0), (4, 4)))
        _, path_astar = _run_pathfinding(astar_steps(grid, (0, 0), (4, 4)))
        # both should find a path of the same length for fair comparison
        self.assertEqual(len(path_dijk), len(path_astar))

    def test_no_path_when_blocked(self):
        """A* should also return no path when goal is unreachable."""
        grid = self._open_grid(5, 5)
        for r in range(5):
            grid[r][2] = 1   # vertical wall cutting the grid in half
        _, path = _run_pathfinding(astar_steps(grid, (0, 0), (4, 4)))
        self.assertIsNone(path)

    def test_path_is_correct_length_on_small_grid(self):
        """On a 3x3 open grid, shortest path from (0,0) to (2,2) needs 5 cells."""
        grid = self._open_grid(3, 3)
        _, path = _run_pathfinding(astar_steps(grid, (0, 0), (2, 2)))
        # shortest path = 4 moves = 5 cells (2 right + 2 down + start)
        self.assertEqual(len(path), 5)


class TestDPGridPaths(unittest.TestCase):

    def test_open_grid_path_count(self):
        """On a 3x3 open grid, there are 6 paths from top-left to bottom-right."""
        grid = [[0] * 3 for _ in range(3)]
        dp = dp_grid_paths(grid)
        self.assertEqual(dp[2][2], 6)

    def test_single_cell_grid(self):
        """1x1 grid has exactly 1 path (you're already at the end)."""
        grid = [[0]]
        dp = dp_grid_paths(grid)
        self.assertEqual(dp[0][0], 1)

    def test_wall_blocks_paths(self):
        """Placing a wall should reduce the number of paths."""
        grid_open = [[0] * 3 for _ in range(3)]
        grid_wall = [[0] * 3 for _ in range(3)]
        grid_wall[1][1] = 1   # wall in the center

        dp_open = dp_grid_paths(grid_open)
        dp_wall = dp_grid_paths(grid_wall)

        self.assertGreater(dp_open[2][2], dp_wall[2][2])

    def test_all_walls_except_edges_still_finds_path(self):
        """A path along just the edges should still be counted."""
        grid = [[1] * 4 for _ in range(4)]
        # clear top row and right column, one path around the edge
        for c in range(4):
            grid[0][c] = 0
        for r in range(4):
            grid[r][3] = 0
        dp = dp_grid_paths(grid)
        self.assertEqual(dp[3][3], 1)

    def test_dp_table_shape(self):
        """The returned DP table should have the same dimensions as the grid."""
        grid = [[0] * 5 for _ in range(4)]
        dp = dp_grid_paths(grid)
        self.assertEqual(len(dp), 4)
        self.assertEqual(len(dp[0]), 5)

    def test_no_path_when_fully_blocked(self):
        """If start or first row/col is fully walled off, count should be 0."""
        grid = [[0] * 3 for _ in range(3)]
        grid[0][1] = 1   # block the only path in the first row at col 1
        grid[1][0] = 1   # block the only path in the first col at row 1
        dp = dp_grid_paths(grid)
        # can't reach (2,2) at all
        self.assertEqual(dp[2][2], 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
