"""
Phase 2: Max-Heap Visualiser
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

    # which node to highlight after an insert or extract
    highlight_idx = -1
    last_extracted = None

    input_box = pygame.Rect(100, 578, 100, 30)
    ins_btn   = pygame.Rect(210, 578, 80,  30)
    ext_btn   = pygame.Rect(300, 578, 130, 30)
    clr_btn   = pygame.Rect(440, 578, 70,  30)


    def get_node_pos(index, screen_width):
        """
        Work out where to draw node[index] on screen.
        Each level sits 90px below the previous one.
        Nodes on the same level are spread evenly across the width.
        """
        level = (index + 1).bit_length() - 1        
        nodes_in_level = 2 ** level    
        position_in_level = index - (nodes_in_level - 1)

        x_gap = screen_width // (nodes_in_level + 1)
        x = x_gap * (position_in_level + 1)
        y = 130 + level * 100           
        return x, y

    def draw_heap_tree():
        """
        Draw the heap as a proper tree diagram.
        Parent-child relationships come directly from the array indices.
        """
        if not heap.heap:
            draw_text(screen, font,
                      "Heap is empty - insert some values!",
                      (WIDTH // 2 - 170, 300), GRAY)
            return

        n = len(heap.heap)

        # build positions for every node up front
        positions = {i: get_node_pos(i, WIDTH) for i in range(n)}

        radius = 26

        # draw edges first so nodes sit on top of them
        for i in range(1, n):
            parent = (i - 1) // 2
            pygame.draw.line(screen, GRAY, positions[parent], positions[i], 2)

        # draw each node as a circle with its value inside
        for i, val in enumerate(heap.heap):
            x, y = positions[i]

            if i == 0:
                color = ORANGE          
            elif i == highlight_idx:
                color = TEAL          
            else:
                color = PURPLE

            pygame.draw.circle(screen, color, (x, y), radius)
            lbl = font.render(str(val), True, BTN_TXT)
            screen.blit(lbl, lbl.get_rect(center=(x, y)))

            # small label above the root so it's obvious
            if i == 0:
                draw_text(screen, small, "MAX", (x - 14, y - radius - 18), ORANGE)


    while True:
        screen.fill(BG)
        draw_title(screen, font_big, "Max-Heap Visualiser")
        mouse = pygame.mouse.get_pos()
        back_rect = draw_back_button(screen, font, mouse)

        draw_text(screen, small, message, (10, 50), YELLOW)
        draw_text(screen, small,
                  "Parent >= both children always. Root = maximum element.",
                  (10, 68), GRAY)
        draw_text(screen, font,
                  f"Size: {heap.size()}   |   Max: {heap.peek()}",
                  (10, 90), TEXT_COL)

        if last_extracted is not None:
            draw_text(screen, font,
                      f"Last extracted: {last_extracted}", (500, 90), ORANGE)

        draw_heap_tree()

        # array representation at the bottom so the user can see both views
        draw_text(screen, small, "Array: " + str(heap.heap), (10, 545), TEAL)

        # input box
        col = TEAL if input_active else GRAY
        pygame.draw.rect(screen, col, input_box, 2, border_radius=4)
        draw_text(screen, font,
                  input_text or "value",
                  (input_box.x + 5, input_box.y + 4),
                  TEXT_COL if input_text else GRAY)

        draw_button(screen, font, "Insert",      ins_btn, mouse, GREEN,  GREEN_HOVER)
        draw_button(screen, font, "Extract Max", ext_btn, mouse, ORANGE, (255, 200, 100))
        draw_button(screen, font, "Clear",       clr_btn, mouse, RED,    RED_HOVER)

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