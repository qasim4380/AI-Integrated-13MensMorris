import copy

ROWS, COLS = 15, 13
board = [
    [2, 2, 2, 2, 2, 2, 0, 2, 2, 2, 2, 2, 2],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [2, 2, 2, 2, 2, 2, 0, 2, 2, 2, 2, 2, 2],
    [2, 2, 2, 0, 2, 2, 2, 2, 2, 0, 2, 2, 2],
    [2, 2, 2, 2, 0, 2, 0, 2, 0, 2, 2, 2, 2],
    [2, 2, 2, 2, 2, 0, 2, 0, 2, 2, 2, 2, 2],
    [0, 2, 0, 2, 0, 2, 2, 2, 0, 2, 0, 2, 0],
    [0, 2, 0, 2, 0, 2, 2, 2, 0, 2, 0, 2, 0],
    [0, 2, 0, 2, 0, 2, 2, 2, 0, 2, 0, 2, 0],
    [2, 2, 2, 2, 2, 0, 2, 0, 2, 2, 2, 2, 2],
    [2, 2, 2, 2, 0, 2, 0, 2, 0, 2, 2, 2, 2],
    [2, 2, 2, 0, 2, 2, 2, 2, 2, 0, 2, 2, 2],
    [2, 2, 2, 2, 2, 2, 0, 2, 2, 2, 2, 2, 2],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [2, 2, 2, 2, 2, 2, 0, 2, 2, 2, 2, 2, 2]
]

pos_map = {
    1: (0, 6), 2: (2, 6), 3: (3, 3), 4: (3, 9),
    5: (4, 4), 6: (4, 6), 7: (4, 8), 8: (5, 5), 9: (5, 7),
    10: (6, 0), 11: (6, 2), 12: (6, 4), 13: (6, 8), 14: (6, 10), 15: (6, 12),
    16: (7, 0), 17: (7, 2), 18: (7, 4), 19: (7, 8), 20: (7, 10), 21: (7, 12),
    22: (8, 0), 23: (8, 2), 24: (8, 4), 25: (8, 8), 26: (8, 10), 27: (8, 12),
    28: (9, 5), 29: (9, 7), 30: (10, 4), 31: (10, 6), 32: (10, 8),
    33: (11, 3), 34: (11, 9), 35: (12, 6), 36: (14, 6)
}

adjacency_map = {
    1: [3, 4], 2: [5, 7], 3: [1, 5, 10], 4: [1, 7, 15],
    5: [2, 3, 8, 11], 6: [8, 9], 7: [2, 4, 9, 14],
    8: [5, 6, 12], 9: [6, 7, 13], 10: [3, 16], 11: [5, 17],
    12: [8, 18], 13: [9, 19], 14: [7, 20], 15: [4, 21],
    16: [10, 17, 22], 17: [11, 16, 18, 23], 18: [12, 17, 24],
    19: [13, 20, 25], 20: [14, 19, 21, 26], 21: [15, 20, 27],
    22: [16, 33], 23: [17, 30], 24: [18, 28],
    25: [19, 29], 26: [20, 32], 27: [21, 34],
    28: [24, 30, 31], 29: [25, 31, 32], 30: [23, 28, 32, 35],
    31: [28, 29], 32: [26, 29, 34, 35], 33: [22, 30, 36], 34: [27, 32, 36],
    35: [30, 32], 36: [33, 34]
}

mill_lines = [
    [1, 3, 10], [10, 16, 22], [22, 33, 36], [27, 34, 36], [15, 21, 27],
    [1, 4, 15], [2, 5, 11], [11, 17, 23], [23, 30, 35], [26, 32, 35],
    [14, 20, 26], [2, 7, 14], [6, 8, 12], [12, 18, 24], [24, 28, 31],
    [25, 29, 31], [13, 19, 25], [6, 9, 13], [3, 5, 8], [16, 17, 18],
    [28, 30, 33], [29, 32, 34], [19, 20, 21], [4, 7, 9]
]

def print_board():
    print("\nCurrent Board:")
    for row in board:
        for cell in row:
            print("." if cell == 0 else "X" if cell == 1 else "O" if cell == 3 else " ", end="")
        print()

def check_mill(pos, player):
    for line in mill_lines:
        if pos in line:
            if all(board[pos_map[p][0]][pos_map[p][1]] == player for p in line):
                return True
    return False

def move_piece(from_pos, to_pos, player, allow_jump=False):
    if from_pos not in pos_map or to_pos not in pos_map:
        return False
    fx, fy = pos_map[from_pos]
    tx, ty = pos_map[to_pos]
    if board[fx][fy] != player or board[tx][ty] != 0:
        return False
    if not allow_jump and to_pos not in adjacency_map[from_pos]:
        return False
    board[fx][fy] = 0
    board[tx][ty] = player
    return True


def get_all_moves(b, player):
    moves = []
    player_positions = [pos for pos in pos_map if b[pos_map[pos][0]][pos_map[pos][1]] == player]
    
    # If player has only 3 pieces, allow jumping to any empty position
    allow_jump = len(player_positions) == 3

    for pos in player_positions:
        if allow_jump:
            for dest in pos_map:
                x, y = pos_map[dest]
                if b[x][y] == 0:
                    moves.append((pos, dest))
        else:
            for adj in adjacency_map.get(pos, []):
                ax, ay = pos_map[adj]
                if b[ax][ay] == 0:
                    moves.append((pos, adj))
    return moves


def evaluate(b):
    def count_mills(player):
        return sum(
            all(b[pos_map[p][0]][pos_map[p][1]] == player for p in line)
            for line in mill_lines
        )

    def mobility(player):
        return len(get_all_moves(b, player))

    def piece_count(player):
        return sum(1 for pos in pos_map if b[pos_map[pos][0]][pos_map[pos][1]] == player)

    p1_pieces = piece_count(1)
    p2_pieces = piece_count(3)
    p1_mills = count_mills(1)
    p2_mills = count_mills(3)
    p1_moves = mobility(1)
    p2_moves = mobility(3)

    # Weighted score: feel free to adjust these weights
    return (
        (p2_pieces - p1_pieces) * 10 +      # more pieces = stronger
        (p2_mills - p1_mills) * 15 +        # mills are more valuable
        (p2_moves - p1_moves) * 2           # mobility matters too
    )


def minimax(b, depth, alpha, beta, maximizing, pos_map, adjacency_map):
    if depth == 0:
        return evaluate(b), None

    player = 3 if maximizing else 1
    best_move = None

    for move in get_all_moves(b, player):
        new_b = copy.deepcopy(b)
        fx, fy = pos_map[move[0]]
        tx, ty = pos_map[move[1]]
        new_b[fx][fy], new_b[tx][ty] = 0, player

        val, _ = minimax(new_b, depth - 1, alpha, beta, not maximizing, pos_map, adjacency_map)

        if maximizing:
            if val > alpha:
                alpha = val
                best_move = move
            if alpha >= beta:
                break  # β cut-off
        else:
            if val < beta:
                beta = val
                best_move = move
            if beta <= alpha:
                break  # α cut-off

    return (alpha if maximizing else beta), best_move


def main():
    p1_pieces, p2_pieces = 13, 13
    p1_removed = p2_removed = 0
    total_placed = 0
    turn = 1
    print_board()

    while p1_removed < 11 and p2_removed < 11:
        if total_placed < 26:
            if turn == 1:
                pos = int(input(f"\nPlayer 1 (X), enter position (1-36): "))
            else:
                print("\nAI (O) is thinking for placement...")
                pos = next((p for p in pos_map if board[pos_map[p][0]][pos_map[p][1]] == 0), None)

            if pos not in pos_map:
                print("Invalid position.")
                continue
            x, y = pos_map[pos]
            if board[x][y] != 0:
                print("Position already occupied.")
                continue
            board[x][y] = 1 if turn == 1 else 3
            total_placed += 1
            print_board()

            if check_mill(pos, board[x][y]):
                if turn == 1:
                    rem = int(input("Mill formed! Remove one of AI's pieces: "))
                else:
                    rem = next((p for p in pos_map if board[pos_map[p][0]][pos_map[p][1]] == 1), None)

                if rem in pos_map:
                    rx, ry = pos_map[rem]
                    if board[rx][ry] == (3 if turn == 1 else 1):
                        board[rx][ry] = 0
                        if turn == 1:
                            p2_removed += 1
                        else:
                            p1_removed += 1

        else:
            print(f"\nMovement phase. Player {'1 (X)' if turn == 1 else '2 (O)'}, move your piece.")
            if turn == 1:
                from_pos = int(input("Enter position to move from: "))
                to_pos = int(input("Enter position to move to: "))
                p1_pieces_on_board = sum(1 for pos in pos_map if board[pos_map[pos][0]][pos_map[pos][1]] == 1)
                allow_jump = p1_pieces_on_board == 3
                if not move_piece(from_pos, to_pos, 1, allow_jump):
                    print("Invalid move. Try again.")
                    continue
                moved_pos = to_pos

            else:
                p2_pieces_on_board = sum(1 for pos in pos_map if board[pos_map[pos][0]][pos_map[pos][1]] == 3)
                allow_jump = p2_pieces_on_board == 3
                _, move = minimax(board, 2, float('-inf'), float('inf'), True, pos_map, adjacency_map)
                if move:
                    from_pos, to_pos = move
                    move_piece(from_pos, to_pos, 3, allow_jump)
                    print(f"AI moved from {from_pos} to {to_pos}")
                    moved_pos = to_pos
                else:
                    print("AI has no valid moves.")
                    break
            print_board()

            if check_mill(moved_pos, 1 if turn == 1 else 3):
                if turn == 1:
                    rem = int(input("Mill formed! Remove one of opponent's pieces: "))
                else:
                    rem = next((p for p in pos_map if board[pos_map[p][0]][pos_map[p][1]] == 1), None)
                if rem in pos_map:
                    rx, ry = pos_map[rem]
                    if board[rx][ry] == (3 if turn == 1 else 1):
                        board[rx][ry] = 0
                        if turn == 1:
                            p2_removed += 1
                        else:
                            p1_removed += 1

        if p1_removed >= 11:
            print("Player 2 (O) wins!")
            break
        elif p2_removed >= 11:
            print("Player 1 (X) wins!")
            break

        turn = 3 - turn

if __name__ == "__main__":
    main()
