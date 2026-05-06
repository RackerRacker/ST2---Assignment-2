"""
Graph represented as an adjacency list.
Supports BFS and DFS traversals, both as step generators for animation.
"""

class Graph:
    def __init__(self):
        # adjacency list - dict of node: list of neighbours
        self.adj = {}

    def add_node(self, node):
        if node not in self.adj:
            self.adj[node] = []

    def add_edge(self, u, v):
        """Add an undirected edge between u and v."""
        self.add_node(u)
        self.add_node(v)
        if v not in self.adj[u]:
            self.adj[u].append(v)
        if u not in self.adj[v]:
            self.adj[v].append(u)

    def nodes(self):
        return list(self.adj.keys())

    def neighbours(self, node):
        return self.adj.get(node, [])

    def bfs_steps(self, start):
        """
        BFS - explore neighbours level by level (breadth first).
        Yields the current visited list and queue at each step.
        """
        if start not in self.adj:
            return
        visited = set([start])
        queue = [start]
        order = []
        while queue:
            node = queue.pop(0)
            order.append(node)
            # yield so the visualiser can draw this step
            yield list(order), node, list(queue), set(visited)
            for neighbour in sorted(self.adj[node]):
                if neighbour not in visited:
                    visited.add(neighbour)
                    queue.append(neighbour)
        yield list(order), None, [], set(visited)

    def dfs_steps(self, start):
        """
        DFS - go as deep as possible before backtracking (depth first).
        Uses a stack instead of a queue.
        """
        if start not in self.adj:
            return
        visited = set()
        stack = [start]
        order = []
        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                order.append(node)
                yield list(order), node, list(stack), set(visited)
                # push neighbours in reverse so we visit them in order
                for neighbour in reversed(sorted(self.adj[node])):
                    if neighbour not in visited:
                        stack.append(neighbour)
        yield list(order), None, [], set(visited)
