"""
utils.py - shared helper stuff used by all the modules
colors, button drawing, text drawing, input boxes - all in one place
"""

import pygame
import sys

# screen dimensions - all modules use this
WIDTH = 900
HEIGHT = 650
FPS = 60

# color palette - dark theme, consistent across all modules
BG = (30, 30, 46)
TEXT_COL = (205, 214, 244)
TITLE_COL = (203, 166, 247)
BTN  = (137, 180, 250)
BTN_HOVER = (180, 190, 255)
BTN_TXT = (30, 30, 46)
RED = (243, 139, 168)
RED_HOVER = (255, 160, 180)
GREEN = (166, 227, 161)
GREEN_HOVER = (150, 200, 150)
YELLOW = (249, 226, 175)
ORANGE = (250, 179, 135)
BLUE = (137, 180, 250)
PURPLE = (203, 166, 247)
TEAL = (148, 226, 213)
GRAY = (100, 100, 120)
DARK_GRAY   = (49, 50, 68)
SURFACE     = (49, 50, 68)


def draw_button(screen, font, text, rect, mouse_pos, color=None, hover=None):
    """Draw a button and return True if mouse is hovering."""
    if color is None:
        color = BTN
    if hover is None:
        hover = BTN_HOVER
    c = hover if rect.collidepoint(mouse_pos) else color
    pygame.draw.rect(screen, c, rect, border_radius=6)
    label = font.render(text, True, BTN_TXT)
    screen.blit(label, label.get_rect(center=rect.center))
    return rect.collidepoint(mouse_pos)


def draw_back_button(screen, font, mouse_pos):
    """Back button top left corner."""
    rect = pygame.Rect(10, 10, 90, 34)
    draw_button(screen, font, "< Back", rect, mouse_pos, RED, RED_HOVER)
    return rect


def draw_title(screen, font, text):
    """Centered title at top of screen."""
    title = font.render(text, True, TITLE_COL)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 12))


def draw_text(screen, font, text, pos, color=None):
    """Draw text at position."""
    if color is None:
        color = TEXT_COL
    t = font.render(text, True, color)
    screen.blit(t, pos)
    return t.get_rect(topleft=pos)


def draw_panel(screen, rect, color=None):
    """Draw a rounded panel/card."""
    if color is None:
        color = SURFACE
    pygame.draw.rect(screen, color, rect, border_radius=8)


def handle_quit(event):
    """Exit the app if the window was closed."""
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
