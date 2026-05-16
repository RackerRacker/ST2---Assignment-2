"""
main.py - ST2 DSA Explorer and Visualiser
Entry point. Shows the main menu and launches whichever module the user picks.

Run with: python main.py
Requires: pygame  (pip install pygame)
"""

import pygame
import sys

import os
sys.path.insert(0, os.path.dirname(__file__))

from utils import *
from phase1.data_structures import data_structures_module
from phase2.graphs import graphs_module
from phase2.sorting import sorting_module
from phase2.heap_module import heap_module 
from phase3.puzzles import puzzles_module 



def main_menu(screen, clock):
    """
    The main menu. Five buttons, one for each module.
    Returns the name of the module the user clicked.
    """
    pygame.display.set_caption("ST2 DSA Explorer & Visualiser")
    font_big = pygame.font.SysFont("Arial", 32, bold=True)
    font     = pygame.font.SysFont("Arial", 22)
    small    = pygame.font.SysFont("Arial", 16)

    # menu options and their module functions
    entries = [
        ("Phase 1 - Data Structures", data_structures_module, GREEN,   GREEN_HOVER),
        ("Phase 2 - Graphs", graphs_module, BLUE,   BTN_HOVER),
        ("Phase 2 - Sorting", sorting_module, BLUE, BTN_HOVER),
        ("Phase 2 - Heap", heap_module, ORANGE,   (255, 200, 100)),
        ("Phase 3 - Puzzles", puzzles_module, PURPLE, (255, 190, 255))
    ]

    # centered button rectangles
    btn_w, btn_h = 380, 56
    rects = [
        pygame.Rect(WIDTH // 2 - btn_w // 2, 180 + i * 76, btn_w, btn_h)
        for i in range(len(entries))
    ]

    while True:
        screen.fill(BG)
        mouse = pygame.mouse.get_pos()

        # title area
        title = font_big.render("ST2 DSA Explorer & Visualiser", True, TITLE_COL)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 60))
        sub = small.render("Explore data structures and algorithms step by step", True, GRAY)
        screen.blit(sub, (WIDTH // 2 - sub.get_width() // 2, 106))
        pygame.draw.line(screen, GRAY, (80, 140), (WIDTH - 80, 140), 1)

        # draw menu buttons
        for i, (label, _, col, hov) in enumerate(entries):
            draw_button(screen, font, label, rects[i], mouse, col, hov)

        # footer
        footer = small.render("ST2 Assignment 2  |  DSA Visualiser", True, GRAY)
        screen.blit(footer, (WIDTH // 2 - footer.get_width() // 2, HEIGHT - 28))

        pygame.display.flip()

        for event in pygame.event.get():
            handle_quit(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, (_, func, _, _) in enumerate(entries):
                    if rects[i].collidepoint(event.pos):
                        func(screen, clock)

        clock.tick(FPS)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    main_menu(screen, clock)
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
