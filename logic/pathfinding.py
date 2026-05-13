"""
Dijkstra's and A* pathfinding on a grid.
Both return step-by-step info so the visualiser can animate the search.
"""

import heapq


def dijkstra_steps(grid, start, end):
    """
    Dijkstra's algorithm - finds shortest path by always expanding
    the cheapest unvisited node. Works on any weighted graph.
    Note that for the grid: 0 = open, 1 = wall
    """
    rows, cols = len(grid), len(grid[0])
    dist = {start: 0}
    prev = {}
    pq = [(0, start)]   # (cost, node)
    visited = set()

    while pq:
        cost, node = heapq.heappop(pq)
        if node in visited:
            continue
        visited.add(node)

        yield visited.copy(), node, None  # let the visualiser draw this step

        if node == end:
            # reconstruct the path by walking back through prev
            path = []
            cur = end
            while cur in prev:
                path.append(cur)
                cur = prev[cur]
            path.append(start)
            path.reverse()
            yield visited.copy(), node, path
            return

        r, c = node
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 0:
                neighbour = (nr, nc)
                new_cost = cost + 1
                if new_cost < dist.get(neighbour, float('inf')):
                    dist[neighbour] = new_cost
                    prev[neighbour] = node
                    heapq.heappush(pq, (new_cost, neighbour))

    yield visited.copy(), None, None  # no path found


def astar_steps(grid, start, end):
    """
    A* - like Dijkstra but uses a heuristic to guide the search toward the goal.
    Uses Manhattan distance as the heuristic (good for grids without diagonals).
    """
    rows, cols = len(grid), len(grid[0])

    def heuristic(a, b):
        # Manhattan distance: absolute difference in row + col
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    open_set = [(heuristic(start, end), 0, start)]
    g_score = {start: 0}
    prev = {}
    visited = set()

    while open_set:
        f, g, node = heapq.heappop(open_set)
        if node in visited:
            continue
        visited.add(node)

        yield visited.copy(), node, None

        if node == end:
            path = []
            cur = end
            while cur in prev:
                path.append(cur)
                cur = prev[cur]
            path.append(start)
            path.reverse()
            yield visited.copy(), node, path
            return

        r, c = node
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 0:
                neighbour = (nr, nc)
                tentative_g = g_score[node] + 1
                if tentative_g < g_score.get(neighbour, float('inf')):
                    g_score[neighbour] = tentative_g
                    prev[neighbour] = node
                    f_score = tentative_g + heuristic(neighbour, end)
                    heapq.heappush(open_set, (f_score, tentative_g, neighbour))

    yield visited.copy(), None, None


def dp_grid_paths(grid):
    """
    Count paths from top-left to bottom-right moving only right or down.
    Obstacles (1s) block movement. Returns the dp table for visualisation.
    """
    rows, cols = len(grid), len(grid[0])
    dp = [[0] * cols for _ in range(rows)]

    # starting cell - 1 way to be here (as long as it's not a wall)
    if grid[0][0] == 0:
        dp[0][0] = 1

    # fill first row - can only come from the left
    for c in range(1, cols):
        if grid[0][c] == 0:
            dp[0][c] = dp[0][c - 1]

    # fill first col - can only come from above
    for r in range(1, rows):
        if grid[r][0] == 0:
            dp[r][0] = dp[r - 1][0]

    # fill the rest - can come from left or above
    for r in range(1, rows):
        for c in range(1, cols):
            if grid[r][c] == 0:
                dp[r][c] = dp[r - 1][c] + dp[r][c - 1]

    return dp
