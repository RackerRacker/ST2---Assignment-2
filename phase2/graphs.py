"""
Phase 2: Graph Traversal Visualiser
"""

import pygame
import math
from utils import *
from logic.graph import Graph


# preset node positions so the graph looks clean on screen
NODE_POSITIONS = {
    'A': (450, 120),
    'B': (250, 240),
    'C': (650, 240),
    'D': (150, 380),
    'E': (360, 380),
    'F': (560, 380),
    'G': (730, 380),
    'H': (260, 510),
    'I': (480, 510),
}

# edges for the preset graph
EDGES = [
    ('A', 'B'), ('A', 'C'),
    ('B', 'D'), ('B', 'E'),
    ('C', 'F'), ('C', 'G'),
    ('D', 'H'), ('E', 'H'), ('E', 'I'),
    ('F', 'I'),
]


def graphs_module(screen, clock):
    """Main graph visualiser - pick BFS or DFS then click a start node."""
    pygame.display.set_caption("Graph Traversal")
    font_big = pygame.font.SysFont("Arial", 26, bold=True)
    font = pygame.font.SysFont("Arial", 20)
    small = pygame.font.SysFont("Arial", 16)

    # build the graph
    g = Graph()
    for u, v in EDGES:
        g.add_edge(u, v)

    mode = "BFS"  # current algorithm
    visited_order = []
    current_node = None
    traversal_gen = None
    traversal_done = False
    message = "Click a node to start BFS. Press D to switch to DFS."

    bfs_btn = pygame.Rect(10, 580, 80, 32)
    dfs_btn = pygame.Rect(100, 580, 80, 32)
    rst_btn = pygame.Rect(200, 580, 90, 32)

    step_delay = 600   # ms between traversal steps
    last_step = 0

    node_radius = 26
    visited_set = set()

    while True:
        now = pygame.time.get_ticks()
        mouse = pygame.mouse.get_pos()

        # advance traversal one step at a time
        if traversal_gen and not traversal_done and now - last_step > step_delay:
            try:
                visited_order, current_node, _, visited_set = next(traversal_gen)
                last_step = now
            except StopIteration:
                traversal_done = True
                message = f"{mode} complete! Click a node to restart."

        screen.fill(BG)
        draw_title(screen, font_big, f"Graph Traversal - {mode}")
        draw_text(screen, small, message, (10, 50), YELLOW)

        # draw edges first (so they appear behind nodes)
        for u, v in EDGES:
            ux, uy = NODE_POSITIONS[u]
            vx, vy = NODE_POSITIONS[v]
            pygame.draw.line(screen, GRAY, (ux, uy), (vx, vy), 2)

        # draw nodes
        for node, (nx, ny) in NODE_POSITIONS.items():
            if node == current_node:
                color = ORANGE       # currently being processed
            elif node in visited_set:
                color = GREEN        # already visited
            else:
                color = BLUE         # not yet visited

            pygame.draw.circle(screen, color, (nx, ny), node_radius)
            lbl = font.render(node, True, BTN_TXT)
            screen.blit(lbl, lbl.get_rect(center=(nx, ny)))

        # show the visit order so far
        order_str = " -> ".join(visited_order)
        draw_text(screen, small, f"Visit order: {order_str}", (10, 90), TEAL)

        back_rect = draw_back_button(screen, font, mouse)
        draw_button(screen, font, "BFS", bfs_btn, mouse,
                    GREEN if mode == "BFS" else BTN,
                    GREEN_HOVER if mode == "BFS" else BTN_HOVER)
        draw_button(screen, font, "DFS", dfs_btn, mouse,
                    ORANGE if mode == "DFS" else BTN,
                    (255, 200, 100) if mode == "DFS" else BTN_HOVER)
        draw_button(screen, font, "Reset", rst_btn, mouse, RED, RED_HOVER)

        draw_text(screen, small, "Click any node to start traversal from there.", (310, 585), GRAY)

        pygame.display.flip()

        for event in pygame.event.get():
            handle_quit(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    mode = "DFS"
                elif event.key == pygame.K_b:
                    mode = "BFS"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(event.pos):
                    return
                if bfs_btn.collidepoint(event.pos):
                    mode = "BFS"
                    message = "BFS selected. Click a node to start."
                if dfs_btn.collidepoint(event.pos):
                    mode = "DFS"
                    message = "DFS selected. Click a node to start."
                if rst_btn.collidepoint(event.pos):
                    visited_order = []
                    visited_set = set()
                    traversal_gen = None
                    traversal_done = False
                    current_node = None
                    message = "Reset. Click a node to start."

                # check if a node was clicked
                for node, (nx, ny) in NODE_POSITIONS.items():
                    dist = math.hypot(event.pos[0] - nx, event.pos[1] - ny)
                    if dist <= node_radius:
                        visited_order = []
                        visited_set = set()
                        traversal_done = False
                        current_node = None
                        if mode == "BFS":
                            traversal_gen = g.bfs_steps(node)
                        else:
                            traversal_gen = g.dfs_steps(node)
                        message = f"Starting {mode} from node '{node}'..."
                        break

        clock.tick(FPS)
