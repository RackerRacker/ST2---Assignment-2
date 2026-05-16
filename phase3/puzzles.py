"""
Phase 3: Puzzle Challenges
"""

import pygame
from utils import *
from logic.pathfinding import dijkstra_steps, astar_steps, dp_grid_paths
from logic.heap_logic import MaxHeap


def puzzles_module(screen, clock):
    """Puzzle menu - let the user pick which puzzle to try."""
    pygame.display.set_caption("Puzzle Challenges")
    font_big = pygame.font.SysFont("Arial", 26, bold=True)
    font = pygame.font.SysFont("Arial", 20)

    options = ["Pathfinding Puzzle (A* / Dijkstra)", "Event Queue Simulator", "DP Grid Path Counter"]
    rects = [pygame.Rect(WIDTH // 2 - 210, 160 + i * 110, 420, 60) for i in range(3)]

    while True:
        screen.fill(BG)
        draw_title(screen, font_big, "Puzzle Challenges")
        mouse = pygame.mouse.get_pos()
        back_rect = draw_back_button(screen, font, mouse)
        draw_text(screen, font, "Pick a puzzle to solve:", (WIDTH//2 - 130, 115), YELLOW)

        for text, rect in zip(options, rects):
            draw_button(screen, font_big, text, rect, mouse)

        pygame.display.flip()

        for event in pygame.event.get():
            handle_quit(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(event.pos):
                    return
                for i, rect in enumerate(rects):
                    if rect.collidepoint(event.pos):
                        if i == 0:
                            _pathfinding_puzzle(screen, clock)
                        elif i == 1:
                            _event_queue_puzzle(screen, clock)
                        elif i == 2:
                            _dp_grid_puzzle(screen, clock)

        clock.tick(FPS)


# ─── Pathfinding Puzzle 

def _pathfinding_puzzle(screen, clock):
    """
    Grid pathfinding puzzle.
    Left-click to toggle walls, then pick an algorithm to find the path.
    Green cell = start, Red cell = end.
    """
    font_big = pygame.font.SysFont("Arial", 24, bold=True)
    font = pygame.font.SysFont("Arial", 18)
    small = pygame.font.SysFont("Arial", 15)

    ROWS, COLS = 18, 24
    CELL = 28
    GRID_X = (WIDTH - COLS * CELL) // 2
    GRID_Y = 70

    # 0 = open, 1 = wall
    grid = [[0] * COLS for _ in range(ROWS)]
    start = (0, 0)
    end = (ROWS - 1, COLS - 1)

    # animation state
    visited = set()
    path = None
    search_gen = None
    animating = False
    done = False
    algorithm = "A*"
    message = "Left-click to draw walls. Pick algorithm then press Run."

    alg_btn = pygame.Rect(10, 580, 100, 28)
    run_btn = pygame.Rect(120, 580, 80, 28)
    clear_btn = pygame.Rect(210, 580, 80, 28)
    step_delay = 25
    last_step = 0

    def cell_from_mouse(pos):
        """Convert mouse pixel position to grid cell (row, col)."""
        mx, my = pos
        col = (mx - GRID_X) // CELL
        row = (my - GRID_Y) // CELL
        if 0 <= row < ROWS and 0 <= col < COLS:
            return (row, col)
        return None

    painting = False   # True while the mouse button is held for wall-drawing

    while True:
        now = pygame.time.get_ticks()
        mouse = pygame.mouse.get_pos()

        # advance the search animation
        if animating and not done and now - last_step > step_delay:
            try:
                result = next(search_gen)
                visited, current, path = result
                if path is not None or current is None:
                    done = True
                    animating = False
                    if path:
                        message = f"Path found! Length: {len(path)} cells."
                    else:
                        message = "No path exists - the goal is blocked!"
            except StopIteration:
                done = True
                animating = False
            last_step = now

        screen.fill(BG)
        draw_title(screen, font_big, "Pathfinding Puzzle")
        back_rect = draw_back_button(screen, font, mouse)
        draw_text(screen, small, message, (10, 48), YELLOW)

        # draw the grid
        for r in range(ROWS):
            for c in range(COLS):
                x = GRID_X + c * CELL
                y = GRID_Y + r * CELL
                cell = (r, c)

                if cell == start:
                    color = GREEN
                elif cell == end:
                    color = RED
                elif path and cell in path:
                    color = YELLOW     # final path
                elif cell in visited:
                    color = (80, 130, 180)   # explored cells
                elif grid[r][c] == 1:
                    color = DARK_GRAY  # wall
                else:
                    color = BG

                pygame.draw.rect(screen, color, (x + 1, y + 1, CELL - 2, CELL - 2), border_radius=2)

        # grid outline
        pygame.draw.rect(screen, GRAY, (GRID_X, GRID_Y, COLS * CELL, ROWS * CELL), 1)

        draw_button(screen, small, f"Alg: {algorithm}", alg_btn, mouse, PURPLE, (220, 190, 255))
        draw_button(screen, small, "Run", run_btn, mouse, GREEN, GREEN_HOVER)
        draw_button(screen, small, "Clear", clear_btn, mouse, RED, RED_HOVER)

        draw_text(screen, small, "S=start  E=end  Dark=wall  Blue=explored  Yellow=path", (310, 583), GRAY)

        pygame.display.flip()

        for event in pygame.event.get():
            handle_quit(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(event.pos):
                    return
                if alg_btn.collidepoint(event.pos):
                    algorithm = "Dijkstra" if algorithm == "A*" else "A*"
                    message = f"Algorithm switched to {algorithm}."
                if run_btn.collidepoint(event.pos):
                    visited = set()
                    path = None
                    done = False
                    if algorithm == "A*":
                        search_gen = astar_steps(grid, start, end)
                    else:
                        search_gen = dijkstra_steps(grid, start, end)
                    animating = True
                    message = f"Running {algorithm}..."
                if clear_btn.collidepoint(event.pos):
                    grid = [[0] * COLS for _ in range(ROWS)]
                    visited = set()
                    path = None
                    animating = False
                    done = False
                    search_gen = None
                    message = "Grid cleared. Draw some walls and run again."
                cell = cell_from_mouse(event.pos)
                if cell and cell != start and cell != end and not animating:
                    painting = True
                    grid[cell[0]][cell[1]] ^= 1   # toggle wall

            if event.type == pygame.MOUSEBUTTONUP:
                painting = False

            if event.type == pygame.MOUSEMOTION and painting:
                cell = cell_from_mouse(event.pos)
                if cell and cell != start and cell != end and not animating:
                    grid[cell[0]][cell[1]] = 1   # draw wall while dragging

        clock.tick(FPS)


# ─── Event Queue Simulator

def _event_queue_puzzle(screen, clock):
    """
    Priority queue / heap-based event scheduler.
    Add events with a priority. The heap always processes the highest-priority one first.
    """
    font_big = pygame.font.SysFont("Arial", 24, bold=True)
    font = pygame.font.SysFont("Arial", 18)
    small = pygame.font.SysFont("Arial", 15)

    heap = MaxHeap()
    processed = []   
    message = "Add events with a priority. Higher priority = processed first."


    event_names = {}
    event_list = []    # list of (priority, name) for display

    name_text = ""
    pri_text = ""
    name_active = pri_active = False

    name_box = pygame.Rect(60, 578, 140, 28)
    pri_box  = pygame.Rect(235, 578, 60, 28)
    add_btn  = pygame.Rect(305, 578, 80, 28)
    proc_btn = pygame.Rect(395, 578, 140, 28)
    clr_btn  = pygame.Rect(545, 578, 70, 28)

    while True:
        screen.fill(BG)
        draw_title(screen, font_big, "Event Queue Simulator (Max-Heap)")
        mouse = pygame.mouse.get_pos()
        back_rect = draw_back_button(screen, font, mouse)

        draw_text(screen, small, message, (10, 48), YELLOW)
        draw_text(screen, small, "Think of it like a hospital triage - higher priority patients go first.", (10, 65), GRAY)

        # draw the pending event queue (heap order)
        draw_text(screen, font, "Pending Events (heap):", (30, 100), TEAL)
        pygame.draw.rect(screen, SURFACE, (20, 120, 380, 400), border_radius=6)

        for i, (pri, name) in enumerate(event_list):
            y = 130 + i * 38
            if y > 490:
                break
            color = ORANGE if i == 0 else BLUE
            pygame.draw.rect(screen, color, (30, y, 360, 32), border_radius=4)
            label = f"[Priority {pri:>3}]  {name}"
            draw_text(screen, font, label, (40, y + 6), BTN_TXT)

        # draw the processed events log
        draw_text(screen, font, "Processed:", (450, 100), GREEN)
        pygame.draw.rect(screen, SURFACE, (440, 120, 400, 400), border_radius=6)
        for i, (pri, name) in enumerate(reversed(processed[-10:])):
            y = 130 + i * 38
            draw_text(screen, small, f"✓ [{pri}] {name}", (455, y + 8), GREEN)

        # controls
        draw_text(screen, small, "Name:", (name_box.x - 38, name_box.y + 7), GRAY)
        col = TEAL if name_active else GRAY
        pygame.draw.rect(screen, col, name_box, 2, border_radius=4)
        draw_text(screen, font, name_text or "event name", (name_box.x + 4, name_box.y + 4),
                  TEXT_COL if name_text else GRAY)

        draw_text(screen, small, "Pri:", (pri_box.x - 26, pri_box.y + 7), GRAY)
        col = TEAL if pri_active else GRAY
        pygame.draw.rect(screen, col, pri_box, 2, border_radius=4)
        draw_text(screen, font, pri_text or "0-99", (pri_box.x + 4, pri_box.y + 4),
                  TEXT_COL if pri_text else GRAY)

        draw_button(screen, small, "Add Event", add_btn, mouse, GREEN, GREEN_HOVER)
        draw_button(screen, small, "Process Next", proc_btn, mouse, ORANGE, (255, 200, 100))
        draw_button(screen, small, "Clear", clr_btn, mouse, RED, RED_HOVER)

        pygame.display.flip()

        for event in pygame.event.get():
            handle_quit(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                name_active = name_box.collidepoint(event.pos)
                pri_active = pri_box.collidepoint(event.pos)
                if back_rect.collidepoint(event.pos):
                    return
                if add_btn.collidepoint(event.pos):
                    if name_text.strip() and pri_text.strip().isdigit():
                        pri = int(pri_text.strip())
                        name = name_text.strip()
                        heap.insert(pri)
                        event_list.append((pri, name))
                        # keep event_list sorted by priority descending for display
                        event_list.sort(key=lambda x: -x[0])
                        message = f"Added event '{name}' with priority {pri}."
                        name_text = ""
                        pri_text = ""
                    else:
                        message = "Enter both a name and a numeric priority."
                if proc_btn.collidepoint(event.pos):
                    if event_list:
                        max_pri = heap.extract_max()
                        # find the event with that priority in our list
                        for j, (pri, name) in enumerate(event_list):
                            if pri == max_pri:
                                processed.append((pri, name))
                                event_list.pop(j)
                                message = f"Processed '{name}' (priority {pri})."
                                break
                    else:
                        message = "No events in the queue!"
                if clr_btn.collidepoint(event.pos):
                    heap = MaxHeap()
                    event_list = []
                    processed = []
                    message = "Queue cleared."

            if event.type == pygame.KEYDOWN:
                if name_active:
                    if event.key == pygame.K_BACKSPACE:
                        name_text = name_text[:-1]
                    elif len(name_text) < 20:
                        name_text += event.unicode
                if pri_active:
                    if event.key == pygame.K_BACKSPACE:
                        pri_text = pri_text[:-1]
                    elif event.unicode.isdigit() and len(pri_text) < 3:
                        pri_text += event.unicode

        clock.tick(FPS)


# ─── DP Grid Puzzle

def _dp_grid_puzzle(screen, clock):
    """
    Dynamic programming grid path counter.
    Click cells to toggle obstacles, then count the number of paths
    from top-left to bottom-right moving only right or down.
    """
    font_big = pygame.font.SysFont("Arial", 24, bold=True)
    font = pygame.font.SysFont("Arial", 18)
    small = pygame.font.SysFont("Arial", 15)

    ROWS, COLS = 7, 10
    CELL = 55
    GRID_X = (WIDTH - COLS * CELL) // 2
    GRID_Y = 80

    grid = [[0] * COLS for _ in range(ROWS)]
    dp = None
    message = "Click cells to add obstacles. Press 'Count Paths' to run DP."

    count_btn = pygame.Rect(WIDTH // 2 - 80, 578, 160, 28)
    clr_btn   = pygame.Rect(WIDTH // 2 + 90, 578, 70, 28)

    def cell_from_mouse(pos):
        mx, my = pos
        col = (mx - GRID_X) // CELL
        row = (my - GRID_Y) // CELL
        if 0 <= row < ROWS and 0 <= col < COLS:
            return (row, col)
        return None

    while True:
        screen.fill(BG)
        draw_title(screen, font_big, "DP Grid Path Counter")
        mouse = pygame.mouse.get_pos()
        back_rect = draw_back_button(screen, font, mouse)

        draw_text(screen, small, message, (10, 48), YELLOW)
        draw_text(screen, small, "Count paths from S (top-left) to E (bottom-right). Can only move right or down.", (10, 65), GRAY)

        # draw grid
        for r in range(ROWS):
            for c in range(COLS):
                x = GRID_X + c * CELL
                y = GRID_Y + r * CELL
                is_start = (r == 0 and c == 0)
                is_end = (r == ROWS - 1 and c == COLS - 1)

                if is_start:
                    color = GREEN
                elif is_end:
                    color = RED
                elif grid[r][c] == 1:
                    color = ORANGE
                else:
                    color = SURFACE

                pygame.draw.rect(screen, color, (x + 2, y + 2, CELL - 4, CELL - 4), border_radius=4)

                # show DP count inside each open cell
                if dp is not None and grid[r][c] == 0 and not is_start and not is_end:
                    val = dp[r][c]
                    count_lbl = small.render(str(val) if val > 0 else "0", True,
                                            YELLOW if val > 0 else GRAY)
                    screen.blit(count_lbl, count_lbl.get_rect(center=(x + CELL // 2, y + CELL // 2)))

                # start/end labels
                if is_start:
                    draw_text(screen, small, "S", (x + CELL // 2 - 5, y + CELL // 2 - 8), BTN_TXT)
                if is_end:
                    draw_text(screen, small, "E", (x + CELL // 2 - 5, y + CELL // 2 - 8), BTN_TXT)

                # grid line
                pygame.draw.rect(screen, GRAY, (x, y, CELL, CELL), 1)

        draw_button(screen, font, "Count Paths", count_btn, mouse, PURPLE, (220, 190, 255))
        draw_button(screen, font, "Clear", clr_btn, mouse, RED, RED_HOVER)

        pygame.display.flip()

        for event in pygame.event.get():
            handle_quit(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(event.pos):
                    return
                if count_btn.collidepoint(event.pos):
                    dp = dp_grid_paths(grid)
                    total = dp[ROWS - 1][COLS - 1]
                    message = f"Total paths from S to E: {total}. Numbers show paths reaching each cell."
                if clr_btn.collidepoint(event.pos):
                    grid = [[0] * COLS for _ in range(ROWS)]
                    dp = None
                    message = "Grid cleared. Click cells to add obstacles."

                # toggle obstacles (not start or end)
                cell = cell_from_mouse(event.pos)
                if cell and cell != (0, 0) and cell != (ROWS - 1, COLS - 1):
                    r, c = cell
                    grid[r][c] ^= 1
                    dp = None   # reset result when grid changes

        clock.tick(FPS)
