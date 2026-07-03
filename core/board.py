class Board:
    def __init__(self, board_list = None, size = 8):  # Default size is 8 for an 8x8 board
        self.size = size
        self.board = board_list if board_list is not None else [[0 for _ in range(size)] for _ in range(size)]
    def return_update_board(self, piece, vector):
        row = piece.position[0] + vector[0]
        col = piece.position[1] + vector[1]
        self.board[row][col] = piece
        self.board[piece.position[0]][piece.position[1]] = 0
        piece.position = (row, col)  # Update the piece's position
        return self.board

