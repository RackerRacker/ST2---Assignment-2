"""
Phase 2: Sorting Algorithm Visualiser
"""

import pygame
import random
from utils import *
from logic.sorting import bubble_sort_steps, selection_sort_steps, merge_sort_steps


def sorting_module(screen, clock):
    """Let the user pick a sorting algorithm to visualise."""
    pygame.display.set_caption("Sorting Visualiser")
    font_big = pygame.font.SysFont("Arial", 26, bold=True)
    font = pygame.font.SysFont("Arial", 20)

    options = ["Bubble Sort", "Selection Sort", "Merge Sort"]
    rects = [pygame.Rect(WIDTH // 2 - 130, 170 + i * 100, 260, 55) for i in range(3)]

    while True:
        screen.fill(BG)
        draw_title(screen, font_big, "Sorting Algorithms")
        mouse = pygame.mouse.get_pos()
        back_rect = draw_back_button(screen, font, mouse)
        draw_text(screen, font, "Choose a sorting algorithm to visualise:", (WIDTH//2 - 200, 125), YELLOW)

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
                        _run_sort(screen, clock, options[i])

        clock.tick(FPS)


def _run_sort(screen, clock, algorithm):
    """
    Generic sort runner - generates random bars, then animates the chosen algorithm.
    The user can restart with a new random array or go back.
    """
    font_big = pygame.font.SysFont("Arial", 26, bold=True)
    font = pygame.font.SysFont("Arial", 20)
    small = pygame.font.SysFont("Arial", 16)

    # start with a random array
    arr = [random.randint(10, 200) for _ in range(30)]

    def _make_generator(a):
        """Pick the generator based on the algorithm name."""
        if algorithm == "Bubble Sort":
            return bubble_sort_steps(a)
        elif algorithm == "Selection Sort":
            return selection_sort_steps(a)
        else:
            return merge_sort_steps(a)

    gen = _make_generator(arr)
    current = arr.copy()
    i1, i2 = -1, -1
    action = ""
    running_sort = True  # False once the sort finishes
    step_delay = 30       # milliseconds between steps - lower = faster
    last_step = 0
    message = f"Animating {algorithm}. Press R to randomise, Space to pause."
    paused = False

    restart_btn = pygame.Rect(WIDTH - 130, 580, 120, 32)
    back_rect_pos = pygame.Rect(10, 10, 90, 34)

    # bar dimensions
    bar_w = (WIDTH - 40) // len(arr)
    max_h = 430
    max_val = 200

    while True:
        now = pygame.time.get_ticks()
        mouse = pygame.mouse.get_pos()

        # advance the sort one step at a time
        if running_sort and not paused and now - last_step > step_delay:
            try:
                step = next(gen)
                current, i1, i2, action = step
                if action == 'done':
                    running_sort = False
                    message = f"{algorithm} complete! Press R to try again."
            except StopIteration:
                running_sort = False
                message = f"{algorithm} complete! Press R to try again."
            last_step = now

        # draw
        screen.fill(BG)
        draw_title(screen, font_big, algorithm)
        draw_text(screen, small, message, (10, 50), YELLOW)

        for idx, val in enumerate(current):
            x = 20 + idx * bar_w
            h = int(val / max_val * max_h)
            y = 530 - h

            # color coding: green = swapped, red = being compared, blue = default
            if idx == i1 and action == 'swap':
                color = GREEN
            elif idx == i2 and action == 'swap':
                color = GREEN
            elif idx == i1 or idx == i2:
                color = RED
            else:
                color = BLUE

            pygame.draw.rect(screen, color, (x, y, bar_w - 1, h), border_radius=2)

        # speed control hint
        draw_text(screen, small, "Space = pause  |  R = new array", (10, 610), GRAY)
        draw_button(screen, font, "Restart", restart_btn, mouse, ORANGE, (255, 200, 100))
        back_rect = draw_back_button(screen, font, mouse)

        pygame.display.flip()

        for event in pygame.event.get():
            handle_quit(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                    message = "Paused." if paused else f"Resumed {algorithm}."
                if event.key == pygame.K_r:
                    arr = [random.randint(10, 200) for _ in range(30)]
                    gen = _make_generator(arr)
                    current = arr.copy()
                    running_sort = True
                    paused = False
                    message = f"New array! Animating {algorithm}."
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(event.pos):
                    return
                if restart_btn.collidepoint(event.pos):
                    arr = [random.randint(10, 200) for _ in range(30)]
                    gen = _make_generator(arr)
                    current = arr.copy()
                    running_sort = True
                    paused = False
                    message = f"New array! Animating {algorithm}."

        clock.tick(FPS)
