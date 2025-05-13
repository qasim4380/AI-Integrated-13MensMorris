import pygame
import math
import sys
from backend import (
    board,
    pos_map,
    adjacency_map,
    mill_lines,
    move_piece,
    check_mill,
    get_all_moves,
    minimax,
)

# Colors
BG_COLOR       = (181, 101, 29)
LINE_COLOR = (255, 255, 255)
HIGHLIGHT_COL = (255, 255, 0)
WHITE_PIECE    = (255, 255, 255)
BLACK_PIECE    = ( 30,  30,  30)
VALID_MOVE_COL = (0, 255, 0)

# Pygame init
pygame.init()
WINDOW_SIZE = 750
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Thirteen Men’s Morris")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 32)

# Game state
turn         = 1         # 1 = human (X), 3 = AI (O)
phase        = "placing" # "placing" or "moving"
placed       = 0
removed1     = 0  # pieces removed from AI (O)
removed2     = 0  # pieces removed from human (X)
selected     = None
valid_moves  = []
capture_mode = False
to_remove    = []


def to_screen(rc):
    """Convert (row, col) in 15×13 to screen pixels."""
    r, c = rc
    x = int(c / (13 - 1) * (WINDOW_SIZE - 60) + 30)
    y = int(r / (15 - 1) * (WINDOW_SIZE - 110) + 30)
    return x, y


def draw_board():
    screen.fill(BG_COLOR)
    
    # Draw connections
    for pos1 in adjacency_map:
        for pos2 in adjacency_map[pos1]:
            x1, y1 = to_screen(pos_map[pos1])
            x2, y2 = to_screen(pos_map[pos2])
            pygame.draw.line(screen, LINE_COLOR, (x1, y1), (x2, y2), 2)
    
    # Draw hex cells
    for pos, (r, c) in pos_map.items():
        x, y = to_screen((r, c))
        draw_hexagon(x, y, 20, LINE_COLOR)


def draw_pieces():
    for pos, (r, c) in pos_map.items():
        val = board[r][c]
        if val != 0:
            x, y = to_screen((r, c))
            if val == 1:  # Human player
                color = BLACK_PIECE
            elif val == 3:  # AI opponent
                color = (255, 0, 0)  # RED for AI
            pygame.draw.circle(screen, color, (x, y), 15)

    # Highlight selected and valid moves
    if selected is not None:
        x, y = to_screen(pos_map[selected])
        pygame.draw.circle(screen, VALID_MOVE_COL, (x, y), 20, 3)

    for mv in valid_moves:
        x, y = to_screen(pos_map[mv])
        pygame.draw.circle(screen, VALID_MOVE_COL, (x, y), 20, 3)

    for rem in to_remove:
        x, y = to_screen(pos_map[rem])
        pygame.draw.circle(screen, HIGHLIGHT_COL, (x, y), 20, 3)


def draw_hexagon(x, y, size, color):
    points = []
    for i in range(6):
        angle = math.radians(60 * i - 30)
        dx = x + size * math.cos(angle)
        dy = y + size * math.sin(angle)
        points.append((dx, dy))
    pygame.draw.polygon(screen, color, points, width=2)


def draw_status():
    pygame.draw.rect(screen, (220, 220, 220), (0, WINDOW_SIZE - 50, WINDOW_SIZE, 50))

    if capture_mode:
        msg = "Capture Mode: Select an opponent's piece to remove"
    elif phase == "placing":
        msg = f"Phase: Placing | Turn: You (X)" if turn == 1 else f"Phase: Placing | Turn: AI (O)"
    else:
        msg = f"Phase: Moving | Turn: You (X)" if turn == 1 else f"Phase: Moving | Turn: AI (O)"

    msg += f" | Captured Pieces - You: {removed2}  AI: {removed1}"

    text = font.render(msg, True, (10, 10, 10))
    screen.blit(text, (10, WINDOW_SIZE - 45))


def check_winner():
    if phase != "moving":
        return None  # Don't check win conditions during placing

    # If AI has less than 3 pieces, human wins
    if sum(cell == 3 for row in board for cell in row) < 3:
        return 1

    # If Human has less than 3 pieces, AI wins
    if sum(cell == 1 for row in board for cell in row) < 3:
        return 3

    # No valid moves left
    if not get_all_moves(board, turn):
        return 4 - turn

    return None


def pos_from_mouse(mx, my):
    for pos, rc in pos_map.items():
        x, y = to_screen(rc)
        if (mx - x)**2 + (my - y)**2 <= 15**2:
            return pos
    return None


def start_capture(player):
    global capture_mode, to_remove
    capture_mode = True
    opp = 3 if player == 1 else 1
    removable = [p for p,(r,c) in pos_map.items()
                 if board[r][c] == opp and not check_mill(p, opp)]
    to_remove = removable or [p for p,(r,c) in pos_map.items() if board[r][c] == opp]


def main():
    global turn, phase, placed, selected, valid_moves, capture_mode, to_remove, removed1, removed2
    running = True
    winner = None
    while running:
        clock.tick(30)

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False

            elif ev.type == pygame.MOUSEBUTTONDOWN and not winner:
                px, py = ev.pos
                p_clicked = pos_from_mouse(px, py)
                if p_clicked is None:
                    continue

                # Capture removal
                if capture_mode:
                    if p_clicked in to_remove:
                        r, c = pos_map[p_clicked]
                        board[r][c] = 0
                        if turn == 1:
                            removed1 += 1
                        else:
                            removed2 += 1
                        capture_mode = False
                        to_remove = []
                        selected = None
                        valid_moves = []
                    continue

                # Placing phase
                if placed < 26:
                    r, c = pos_map[p_clicked]
                    if board[r][c] == 0:
                        board[r][c] = turn
                        placed += 1
                        if check_mill(p_clicked, turn):
                            start_capture(turn)
                            continue
                        turn = 4 - turn
                    continue

                # Switch to moving phase
                if phase == "placing" and placed >= 26:
                    phase = "moving"

                # Movement: select source
                if selected is None:
                    r, c = pos_map[p_clicked]
                    if board[r][c] == turn:
                        selected = p_clicked
                        valid_moves = [dst for src,dst in get_all_moves(board, turn)
                                       if src == selected]
                    continue

                # Movement: execute
                if p_clicked in valid_moves:
                    # Allow jump if the human player has 3 pieces
                    human_pieces_left = sum(1 for row in board for cell in row if cell == 1)
                    allow_jump = human_pieces_left == 3  # Allow jump if human player has 3 pieces
                    moved = move_piece(selected, p_clicked, turn, allow_jump=allow_jump)
                    if moved:
                        if check_mill(p_clicked, turn):
                            start_capture(turn)
                        else:
                            turn = 4 - turn
                    selected = None
                    valid_moves = []
                    continue

                # Reset selection
                selected = None
                valid_moves = []

        # AI turn
        if turn == 3 and not winner:
            if capture_mode:
                # AI removes a human piece
                if to_remove:
                    rem = to_remove[0]  # Selects first available piece
                    r, c = pos_map[rem]
                    board[r][c] = 0
                    removed2 += 1  # Human's pieces removed count
                    capture_mode = False
                    to_remove = []
                    turn = 1  # Switch to human's turn
            else:
                if placed < 26:
                    # Placing phase
                    placed_piece = False
                    for p, (r, c) in pos_map.items():
                        if board[r][c] == 0:
                            board[r][c] = 3
                            placed += 1
                            placed_piece = True
                            if check_mill(p, 3):
                                start_capture(3)
                            break
                    # Only switch turn if no capture was initiated
                    if placed_piece and not capture_mode:
                        turn = 4 - turn
                else:
                    # Moving phase
                    ai_pieces_left = sum(1 for row in board for cell in row if cell == 3)
                    allow_jump = ai_pieces_left == 3  # Allow jump if AI has 3 pieces
                    _, mv = minimax(board, 2, float('-inf'), float('inf'), True, pos_map, adjacency_map)
                    if mv:
                        f, t = mv
                        moved = move_piece(f, t, 3, allow_jump=allow_jump)
                        if moved:
                            if check_mill(t, 3):
                                start_capture(3)
                            else:
                                turn = 4 - turn

        # Check winner
        if not winner:
            winner = check_winner()

        # Render
        draw_board()
        draw_pieces()
        draw_status()
        if winner:
            msg = "X Wins!" if winner == 1 else "O Wins!"
            txt = font.render(msg, True, (200, 0, 0))
            screen.blit(txt, (WINDOW_SIZE//2 - 50, WINDOW_SIZE//2 - 16))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
