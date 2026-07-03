def isPathBlocked(board_present, vector, position, status = False):
    row, col = position
    d_row, d_col = vector
    new_row, new_col = row + d_row, col + d_col
     # Initialize status to False, indicating the path is not blocked
    # Check if the new position is within the bounds of the board
    if not isinBoard(board_present, new_row, new_col):
        return True  # Out of bounds is considered blocked

    # Check if the path is blocked by another piece
    if board_present[new_row][new_col] != 0 and status:
        return True  # Path is blocked

    return False  # Path is not blocked

def isinBoard(board_present, n_row, n_col):
    if 0 <= n_row < len(board_present) and 0 <= n_col < len(board_present[0]):
        return True
        
def isChessmate(board_present, king_position):
    row, col = king_position
    for r_idx, row_cells in enumerate(board_present):
        for c_idx, cell in enumerate(row_cells):
            if cell == 0:
                continue
            piece = cell

            if piece.color != board_present[row][col].color:  # Check if the piece is of the opposite color
                possible_moves = piece.get_possible_moves()  # Get the possible moves for the piece
                enemy_position = piece.position
                for vector in possible_moves:
                    if enemy_position[0] + vector[0] == row and enemy_position[1] + vector[1] == col:
                        return True  # The king is in checkmate

    return False

