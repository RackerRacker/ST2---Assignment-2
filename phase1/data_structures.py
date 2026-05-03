"""
Phase 1: Data Structures Playground
- Stack with push/pop
- Queue with enqueue/dequeue
- Linked List with insert/delete/reverse
- BST with insert and traversal display
"""

import pygame
from utils import *
from logic.stack import Stack
from logic.queue_ds import Queue
from logic.linked_list import LinkedList
from logic.bst import BST


def data_structures_module(screen, clock):
    """Main entry point - lets the user pick a sub-module."""
    pygame.display.set_caption("Data Structures Playground")
    font_big = pygame.font.SysFont("Arial", 26, bold=True)
    font = pygame.font.SysFont("Arial", 20)

    # sub-module buttons
    options = ["Stack", "Queue", "Linked List", "BST"]
    rects = [pygame.Rect(WIDTH // 2 - 120, 150 + i * 90, 240, 55) for i, _ in enumerate(options)]

    while True:
        screen.fill(BG)
        draw_title(screen, font_big, "Data Structures Playground")
        mouse = pygame.mouse.get_pos()
        back_rect = draw_back_button(screen, font, mouse)

        draw_text(screen, font, "Pick a data structure to explore:", (WIDTH//2 - 180, 110), YELLOW)

        for i, (text, rect) in enumerate(zip(options, rects)):
            draw_button(screen, font_big, text, rect, mouse)

        pygame.display.flip()

        for event in pygame.event.get():
            handle_quit(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(event.pos):
                    return  # go back to main menu
                for i, rect in enumerate(rects):
                    if rect.collidepoint(event.pos):
                        if options[i] == "Stack":
                            _stack_screen(screen, clock)
                        elif options[i] == "Queue":
                            _queue_screen(screen, clock)
                        elif options[i] == "Linked List":
                            _linked_list_screen(screen, clock)
                        elif options[i] == "BST":
                            _bst_screen(screen, clock)

        clock.tick(FPS)


# ─── Stack

def _stack_screen(screen, clock):
    """Stack visualiser - push and pop values with buttons."""
    font_big = pygame.font.SysFont("Arial", 26, bold=True)
    font = pygame.font.SysFont("Arial", 20)
    small = pygame.font.SysFont("Arial", 16)

    stack = Stack()
    message = "Use Push to add, Pop to remove the top item."
    input_text = ""
    input_active = False

    input_box = pygame.Rect(120, 580, 120, 32)
    push_btn = pygame.Rect(255, 580, 80, 32)
    pop_btn = pygame.Rect(345, 580, 80, 32)
    clear_btn = pygame.Rect(435, 580, 80, 32)

    while True:
        screen.fill(BG)
        draw_title(screen, font_big, "Stack Visualiser (LIFO)")
        mouse = pygame.mouse.get_pos()
        back_rect = draw_back_button(screen, font, mouse)

        # instructions
        draw_text(screen, small, message, (10, 50), YELLOW)
        draw_text(screen, small, "LIFO - Last In, First Out. Pop always removes the top.", (10, 68), GRAY)

        # draw the stack as stacked rectangles
        item_h = 44
        stack_x = WIDTH // 2 - 80
        base_y = 550
        for i, val in enumerate(stack.items):
            y = base_y - (i + 1) * item_h
            color = TEAL if i == len(stack.items) - 1 else BLUE
            pygame.draw.rect(screen, color, (stack_x, y, 160, item_h - 4), border_radius=4)
            lbl = font.render(str(val), True, BTN_TXT)
            screen.blit(lbl, lbl.get_rect(center=(stack_x + 80, y + 20)))

        # label the top
        if not stack.is_empty():
            draw_text(screen, small, "<-- TOP", (stack_x + 168, base_y - len(stack.items) * item_h + 12), ORANGE)

        draw_text(screen, font, f"Size: {stack.size()}", (10, 90), TEXT_COL)

        # input box
        col = TEAL if input_active else GRAY
        pygame.draw.rect(screen, col, input_box, 2, border_radius=4)
        draw_text(screen, font, input_text or "value", (input_box.x + 5, input_box.y + 6),
                  TEXT_COL if input_text else GRAY)
        draw_button(screen, font, "Push", push_btn, mouse, GREEN, GREEN_HOVER)
        draw_button(screen, font, "Pop",  pop_btn, mouse)
        draw_button(screen, font, "Clear", clear_btn, mouse, RED, RED_HOVER)

        pygame.display.flip()

        for event in pygame.event.get():
            handle_quit(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                input_active = input_box.collidepoint(event.pos)
                if back_rect.collidepoint(event.pos):
                    return
                if push_btn.collidepoint(event.pos):
                    if input_text.strip():
                        # try to push as int, otherwise keep as string
                        try:
                            stack.push(int(input_text.strip()))
                        except ValueError:
                            stack.push(input_text.strip())
                        message = f"Pushed '{input_text.strip()}' onto the stack."
                        input_text = ""
                    else:
                        message = "Type a value first!"
                if pop_btn.collidepoint(event.pos):
                    val = stack.pop()
                    message = f"Popped '{val}' from the stack." if val is not None else "Stack is empty!"
                if clear_btn.collidepoint(event.pos):
                    stack = Stack()
                    message = "Stack cleared."

            if event.type == pygame.KEYDOWN and input_active:
                if event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.key == pygame.K_RETURN:
                    pass  # push on enter handled by button logic
                elif len(input_text) < 8:
                    input_text += event.unicode

        clock.tick(FPS)


# ─── Queue 

def _queue_screen(screen, clock):
    """Queue visualiser - enqueue at back, dequeue from front."""
    font_big = pygame.font.SysFont("Arial", 26, bold=True)
    font = pygame.font.SysFont("Arial", 20)
    small = pygame.font.SysFont("Arial", 16)

    q = Queue()
    message = "FIFO - First In, First Out."
    input_text = ""
    input_active = False

    input_box   = pygame.Rect(100, 580, 120, 32)
    enq_btn     = pygame.Rect(230, 580, 110, 32)
    deq_btn     = pygame.Rect(350, 580, 110, 32)
    clear_btn   = pygame.Rect(470, 580, 80, 32)

    while True:
        screen.fill(BG)
        draw_title(screen, font_big, "Queue Visualiser (FIFO)")
        mouse = pygame.mouse.get_pos()
        back_rect = draw_back_button(screen, font, mouse)

        draw_text(screen, small, message, (10, 50), YELLOW)
        draw_text(screen, small, "Enqueue adds to BACK. Dequeue removes from FRONT.", (10, 68), GRAY)

        # draw queue horizontally
        items = q.to_list()
        box_w = 70
        box_h = 50
        start_x = 60
        y = 270
        for i, val in enumerate(items):
            x = start_x + i * (box_w + 6)
            color = GREEN if i == 0 else (BLUE if i < len(items) - 1 else TEAL)
            pygame.draw.rect(screen, color, (x, y, box_w, box_h), border_radius=4)
            lbl = font.render(str(val), True, BTN_TXT)
            screen.blit(lbl, lbl.get_rect(center=(x + box_w // 2, y + box_h // 2)))

        if items:
            draw_text(screen, small, "FRONT", (start_x, y + box_h + 4), GREEN)
            draw_text(screen, small, "BACK", (start_x + (len(items) - 1) * (box_w + 6), y + box_h + 4), TEAL)

        draw_text(screen, font, f"Size: {q.size()}", (10, 90), TEXT_COL)

        col = TEAL if input_active else GRAY
        pygame.draw.rect(screen, col, input_box, 2, border_radius=4)
        draw_text(screen, font, input_text or "value", (input_box.x + 5, input_box.y + 6),
                  TEXT_COL if input_text else GRAY)
        draw_button(screen, font, "Enqueue", enq_btn, mouse, GREEN, GREEN_HOVER)
        draw_button(screen, font, "Dequeue", deq_btn, mouse)
        draw_button(screen, font, "Clear", clear_btn, mouse, RED, RED_HOVER)

        pygame.display.flip()

        for event in pygame.event.get():
            handle_quit(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                input_active = input_box.collidepoint(event.pos)
                if back_rect.collidepoint(event.pos):
                    return
                if enq_btn.collidepoint(event.pos):
                    if input_text.strip():
                        try:
                            q.enqueue(int(input_text.strip()))
                        except ValueError:
                            q.enqueue(input_text.strip())
                        message = f"Enqueued '{input_text.strip()}' to the back."
                        input_text = ""
                    else:
                        message = "Enter a value first!"
                if deq_btn.collidepoint(event.pos):
                    val = q.dequeue()
                    message = f"Dequeued '{val}' from the front." if val is not None else "Queue is empty!"
                if clear_btn.collidepoint(event.pos):
                    q = Queue()
                    message = "Queue cleared."

            if event.type == pygame.KEYDOWN and input_active:
                if event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif len(input_text) < 8:
                    input_text += event.unicode

        clock.tick(FPS)


# ─── Linked List

def _linked_list_screen(screen, clock):
    """Linked list visualiser with insert, delete, and reverse."""
    font_big = pygame.font.SysFont("Arial", 26, bold=True)
    font = pygame.font.SysFont("Arial", 20)
    small = pygame.font.SysFont("Arial", 16)

    ll = LinkedList()
    message = "Insert, delete, or reverse the linked list."
    val_text = ""
    pos_text = ""
    val_active = pos_active = False

    val_box = pygame.Rect(60, 575, 90, 30)
    pos_box = pygame.Rect(190, 575, 60, 30)
    ins_btn = pygame.Rect(257, 575, 80, 30)
    del_btn = pygame.Rect(345, 575, 80, 30)
    rev_btn = pygame.Rect(435, 575, 90, 30)
    clr_btn = pygame.Rect(535, 575, 70, 30)

    while True:
        screen.fill(BG)
        draw_title(screen, font_big, "Linked List Visualiser")
        mouse = pygame.mouse.get_pos()
        back_rect = draw_back_button(screen, font, mouse)

        draw_text(screen, small, message, (10, 50), YELLOW)
        draw_text(screen, small, "Each node points to the next. Last node points to None.", (10, 68), GRAY)

        # draw the list as connected boxes with arrows
        items = ll.to_list()
        node_w, node_h = 68, 40
        gap = 36
        start_x = 30
        y = 260

        for i, val in enumerate(items):
            x = start_x + i * (node_w + gap)
            pygame.draw.rect(screen, BLUE, (x, y, node_w, node_h), border_radius=4)
            lbl = font.render(str(val), True, BTN_TXT)
            screen.blit(lbl, lbl.get_rect(center=(x + node_w // 2, y + node_h // 2)))
            # draw arrow to next node
            if i < len(items) - 1:
                arrow_x = x + node_w + 2
                arrow_mid = y + node_h // 2
                pygame.draw.line(screen, ORANGE, (arrow_x, arrow_mid), (arrow_x + gap - 4, arrow_mid), 2)
                # arrowhead
                pygame.draw.polygon(screen, ORANGE, [
                    (arrow_x + gap - 4, arrow_mid),
                    (arrow_x + gap - 10, arrow_mid - 4),
                    (arrow_x + gap - 10, arrow_mid + 4)
                ])

        # "None" label at the end
        if items:
            end_x = start_x + len(items) * (node_w + gap)
            draw_text(screen, small, "-> None", (end_x - 30, y + 12), GRAY)

        draw_text(screen, font, f"Length: {ll.length()}", (10, 90), TEXT_COL)

        # controls
        draw_text(screen, small, "Val:", (val_box.x - 30, val_box.y + 6), GRAY)
        col = TEAL if val_active else GRAY
        pygame.draw.rect(screen, col, val_box, 2, border_radius=4)
        draw_text(screen, font, val_text or "val", (val_box.x + 4, val_box.y + 4),
                  TEXT_COL if val_text else GRAY)

        draw_text(screen, small, "Pos:", (pos_box.x - 30, pos_box.y + 6), GRAY)
        col = TEAL if pos_active else GRAY
        pygame.draw.rect(screen, col, pos_box, 2, border_radius=4)
        draw_text(screen, small, pos_text or "end", (pos_box.x + 4, pos_box.y + 8),
                  TEXT_COL if pos_text else GRAY)

        draw_button(screen, small, "Insert", ins_btn, mouse, GREEN, GREEN_HOVER)
        draw_button(screen, small, "Delete", del_btn, mouse, RED, RED_HOVER)
        draw_button(screen, small, "Reverse", rev_btn, mouse, ORANGE, (255, 200, 100))
        draw_button(screen, small, "Clear", clr_btn, mouse)

        pygame.display.flip()

        for event in pygame.event.get():
            handle_quit(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                val_active = val_box.collidepoint(event.pos)
                pos_active = pos_box.collidepoint(event.pos)
                if back_rect.collidepoint(event.pos):
                    return
                if ins_btn.collidepoint(event.pos):
                    if val_text.strip():
                        pos = int(pos_text) if pos_text.strip().isdigit() else None
                        try:
                            ll.insert(int(val_text.strip()), pos)
                        except ValueError:
                            ll.insert(val_text.strip(), pos)
                        message = f"Inserted '{val_text}' at position {pos if pos is not None else 'end'}."
                        val_text = ""
                    else:
                        message = "Enter a value to insert!"
                if del_btn.collidepoint(event.pos):
                    pos = int(pos_text) if pos_text.strip().isdigit() else 0
                    val = ll.delete(pos)
                    message = f"Deleted '{val}' from position {pos}." if val is not None else "Nothing to delete there."
                if rev_btn.collidepoint(event.pos):
                    ll.reverse()
                    message = "List reversed!"
                if clr_btn.collidepoint(event.pos):
                    ll = LinkedList()
                    message = "List cleared."

            if event.type == pygame.KEYDOWN:
                if val_active:
                    if event.key == pygame.K_BACKSPACE:
                        val_text = val_text[:-1]
                    elif len(val_text) < 6:
                        val_text += event.unicode
                if pos_active:
                    if event.key == pygame.K_BACKSPACE:
                        pos_text = pos_text[:-1]
                    elif event.unicode.isdigit() and len(pos_text) < 3:
                        pos_text += event.unicode

        clock.tick(FPS)


# ─── BST 

def _bst_screen(screen, clock):
    """BST visualiser - insert values and display traversal results."""
    font_big = pygame.font.SysFont("Arial", 26, bold=True)
    font = pygame.font.SysFont("Arial", 20)
    small = pygame.font.SysFont("Arial", 16)

    tree = BST()
    message = "Insert values to build the BST. Left < Root < Right."
    input_text = ""
    input_active = False
    traversal_result = ""

    input_box = pygame.Rect(80, 578, 100, 30)
    ins_btn   = pygame.Rect(190, 578, 80, 30)
    io_btn    = pygame.Rect(280, 578, 90, 30)
    pre_btn   = pygame.Rect(380, 578, 90, 30)
    post_btn  = pygame.Rect(480, 578, 90, 30)
    clr_btn   = pygame.Rect(580, 578, 70, 30)

    def draw_tree_node(node, x, y, gap):
        """Recursively draw the BST. gap shrinks as we go deeper."""
        if node is None:
            return
        radius = 22
        pygame.draw.circle(screen, PURPLE, (x, y), radius)
        lbl = font.render(str(node.value), True, BTN_TXT)
        screen.blit(lbl, lbl.get_rect(center=(x, y)))

        if node.left:
            lx = x - gap
            ly = y + 70
            pygame.draw.line(screen, GRAY, (x, y + radius), (lx, ly - radius), 2)
            draw_tree_node(node.left, lx, ly, gap // 2)
        if node.right:
            rx = x + gap
            ry = y + 70
            pygame.draw.line(screen, GRAY, (x, y + radius), (rx, ry - radius), 2)
            draw_tree_node(node.right, rx, ry, gap // 2)

    while True:
        screen.fill(BG)
        draw_title(screen, font_big, "Binary Search Tree Visualiser")
        mouse = pygame.mouse.get_pos()
        back_rect = draw_back_button(screen, font, mouse)

        draw_text(screen, small, message, (10, 50), YELLOW)

        # draw the tree centered
        draw_tree_node(tree.root, WIDTH // 2, 120, 180)

        if traversal_result:
            draw_text(screen, small, "Traversal: " + traversal_result, (10, 90), TEAL)

        # input + buttons
        col = TEAL if input_active else GRAY
        pygame.draw.rect(screen, col, input_box, 2, border_radius=4)
        draw_text(screen, font, input_text or "value", (input_box.x + 5, input_box.y + 4),
                  TEXT_COL if input_text else GRAY)
        draw_button(screen, small, "Insert", ins_btn, mouse, GREEN, GREEN_HOVER)
        draw_button(screen, small, "Inorder", io_btn, mouse)
        draw_button(screen, small, "Preorder", pre_btn, mouse)
        draw_button(screen, small, "Postorder", post_btn, mouse)
        draw_button(screen, small, "Clear", clr_btn, mouse, RED, RED_HOVER)

        pygame.display.flip()

        for event in pygame.event.get():
            handle_quit(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                input_active = input_box.collidepoint(event.pos)
                if back_rect.collidepoint(event.pos):
                    return
                if ins_btn.collidepoint(event.pos):
                    if input_text.strip().lstrip('-').isdigit():
                        tree.insert(int(input_text.strip()))
                        message = f"Inserted {input_text.strip()} into the BST."
                        input_text = ""
                    else:
                        message = "Please enter a valid integer."
                if io_btn.collidepoint(event.pos):
                    traversal_result = str(tree.inorder()) + "  (sorted order)"
                if pre_btn.collidepoint(event.pos):
                    traversal_result = str(tree.preorder()) + "  (root first)"
                if post_btn.collidepoint(event.pos):
                    traversal_result = str(tree.postorder()) + "  (root last)"
                if clr_btn.collidepoint(event.pos):
                    tree = BST()
                    traversal_result = ""
                    message = "Tree cleared."

            if event.type == pygame.KEYDOWN and input_active:
                if event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif len(input_text) < 5:
                    input_text += event.unicode

        clock.tick(FPS)
