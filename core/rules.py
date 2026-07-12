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
        
def isChessmate(board_present, king_position, color = None):
    row, col = king_position
    color_team = color if color != None else board_present[row][col].color
    for r_idx, row_cells in enumerate(board_present):
        for c_idx, cell in enumerate(row_cells):
            if cell == 0:
                continue
            piece = cell

            if piece.color != color_team:  # Check if the piece is of the opposite color
                possible_moves = piece.get_possible_moves_origin(board_present)  # Get the possible moves for the piece
                enemy_position = piece.position
                for vector in possible_moves:
                    if enemy_position[0] + vector[0] == row and enemy_position[1] + vector[1] == col:
                        return True  # The king is in checkmate

    return False
def find_piece(board_present, name, color): # 查找指定name和color的棋子的位置 仅支持独一无二的棋子 如果要扩大范围需修改其他地方
    for r_idx, row_cells in enumerate(board_present):
        for c_idx, cell in enumerate(row_cells):
            if cell == 0:
                continue
            piece = cell
            if piece.name == name and piece.color == color:
                return piece.position

def will_be_Chessmate(board, position, vector, color): # 若这样移动会被将军则返回True
    r, c = position
    d_r, d_c = vector
    n_r, n_c = r + d_r, c + d_c
    judge1 = False # 该变量记录将移动的棋子是否为王
    judge2 = False # 该变量记录走后是否被将军
    board_present = [[0 for _ in range(8)] for _ in range(8)]
    for r_idx, row_cells in enumerate(board_present):
        for c_idx, cell in enumerate(row_cells):
            board_present[r_idx][c_idx] = board[r_idx][c_idx]
    if board_present[r][c].name == "king":
        judge1 = True
    temp = board_present[n_r][n_c]
    board_present[n_r][n_c] = board_present[r][c]
    board_present[r][c] = 0
    if color == "black":
        if judge1 == False:
            if isChessmate(board_present, find_piece(board_present, 'king', 'black')):
                judge2 = True
        else:
            if isChessmate(board_present, (n_r, n_c)):
                judge2 = True
    else:
        if judge1 == False:
            if isChessmate(board_present, find_piece(board_present, 'king', 'white')):
                judge2 = True
        else:
            if isChessmate(board_present, (n_r, n_c)):
                judge2 = True
    board_present[r][c] = board_present[n_r][n_c]
    board_present[n_r][n_c] = temp
    return judge2