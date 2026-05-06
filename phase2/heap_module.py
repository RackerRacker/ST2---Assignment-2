"""
Phase 2: Max-Heap Visualiser
- Insert values and watch them bubble up
- Extract max and watch the heap reorganise itself
The heap is drawn as a binary tree so you can see the parent-child relationships.
"""

import pygame
from utils import *
from logic.heap_logic import MaxHeap


def heap_module(screen, clock):
    """Heap visualiser with insert and extract-max animation."""
    pygame.display.set_caption("Heap Visualiser")
    font_big = pygame.font.SysFont("Arial", 26, bold=True)
    font = pygame.font.SysFont("Arial", 20)
    small = pygame.font.SysFont("Arial", 16)

    heap = MaxHeap()
    message = "Insert values. The max is always at the top (root)."
    input_text = ""
    input_active = False

    # step-by-step animation state
    highlight_idx = -1       # which node to highlight during insert/extract
    last_extracted = None    # remember what we just pulled out

    input_box = pygame.Rect(100, 578, 100, 30)
    ins_btn   = pygame.Rect(210, 578, 80, 30)
    ext_btn   = pygame.Rect(300, 578, 130, 30)
    clr_btn   = pygame.Rect(440, 578, 70, 30)

    def draw_heap_tree():
        """
        Draw the heap as a tree. The array index tells us parent-child relationships:
        - parent of i is at (i-1)//2
        - children of i are at 2i+1 and 2i+2
        """
        if not heap.heap:
            draw_text(screen, font, "Heap is empty - insert some values!", (WIDTH//2 - 170, 300), GRAY)
            return

        # calculate positions for each node
        positions = {}
        n = len(heap.heap)
        # position each level, spreading nodes horizontally
        level_gap = 90
        for i in range(n):
            level = i.bit_length() - 1   # which depth level is this node on?
            # count how many nodes are on this level
            level_start = 2 ** level - 1
            level_end = min(2 ** (level + 1) - 2, n - 1)
            nodes_on_level = level_end - level_start + 1
            pos_in_level = i - level_start
            # spread across width
            total_w = WIDTH - 100
            spacing = total_w / (nodes_on_level + 1)
            x = int(50 + spacing * (pos_in_level + 1))
            y = 110 + level * level_gap
            positions[i] = (x, y)

        radius = 24

        # draw edges first
        for i in range(1, n):
            parent = (i - 1) // 2
            if parent in positions and i in positions:
                pygame.draw.line(screen, GRAY, positions[parent], positions[i], 2)

        # draw nodes
        for i, val in enumerate(heap.heap):
            x, y = positions[i]
            color = ORANGE if i == 0 else (TEAL if i == highlight_idx else PURPLE)
            pygame.draw.circle(screen, color, (x, y), radius)
            lbl = font.render(str(val), True, BTN_TXT)
            screen.blit(lbl, lbl.get_rect(center=(x, y)))

            # label the root
            if i == 0:
                draw_text(screen, small, "MAX", (x - 14, y - radius - 16), ORANGE)

    while True:
        screen.fill(BG)
        draw_title(screen, font_big, "Max-Heap Visualiser")
        mouse = pygame.mouse.get_pos()
        back_rect = draw_back_button(screen, font, mouse)

        draw_text(screen, small, message, (10, 50), YELLOW)
        draw_text(screen, small, "Parent >= both children always. Root = maximum element.", (10, 68), GRAY)
        draw_text(screen, font, f"Size: {heap.size()}   |   Max: {heap.peek()}", (10, 90), TEXT_COL)

        if last_extracted is not None:
            draw_text(screen, font, f"Last extracted: {last_extracted}", (500, 90), ORANGE)

        draw_heap_tree()

        # draw array representation at the bottom
        draw_text(screen, small, "Array: " + str(heap.heap), (10, 545), TEAL)

        col = TEAL if input_active else GRAY
        pygame.draw.rect(screen, col, input_box, 2, border_radius=4)
        draw_text(screen, font, input_text or "value", (input_box.x + 5, input_box.y + 4),
                  TEXT_COL if input_text else GRAY)
        draw_button(screen, font, "Insert", ins_btn, mouse, GREEN, GREEN_HOVER)
        draw_button(screen, font, "Extract Max", ext_btn, mouse, ORANGE, (255, 200, 100))
        draw_button(screen, font, "Clear", clr_btn, mouse, RED, RED_HOVER)

        pygame.display.flip()

        for event in pygame.event.get():
            handle_quit(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                input_active = input_box.collidepoint(event.pos)
                if back_rect.collidepoint(event.pos):
                    return
                if ins_btn.collidepoint(event.pos):
                    if input_text.strip().lstrip('-').isdigit():
                        val = int(input_text.strip())
                        heap.insert(val)
                        highlight_idx = len(heap.heap) - 1
                        message = f"Inserted {val}. Sifted up to maintain heap property."
                        input_text = ""
                    else:
                        message = "Please enter a valid integer."
                if ext_btn.collidepoint(event.pos):
                    val = heap.extract_max()
                    if val is not None:
                        last_extracted = val
                        highlight_idx = 0
                        message = f"Extracted max: {val}. Root replaced and sifted down."
                    else:
                        message = "Heap is empty - nothing to extract!"
                if clr_btn.collidepoint(event.pos):
                    heap = MaxHeap()
                    last_extracted = None
                    highlight_idx = -1
                    message = "Heap cleared."

            if event.type == pygame.KEYDOWN and input_active:
                if event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif len(input_text) < 5:
                    input_text += event.unicode

        clock.tick(FPS)
