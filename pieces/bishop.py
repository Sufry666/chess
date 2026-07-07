import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
try:    
    from pieces.piece import Piece # type: ignore
    import core.rules # type: ignore
    import utils.helper as helper # type: ignore
    import config # type: ignore
except ImportError as e:
    print(f"{e}. Please check bishop.py.")
class bishop(Piece):
    def __init__(self, color, name = "bishop", position = None, ):
        super().__init__(color, name, position)  # Initialize the base class with color, name, and position
        self.value = 3  # Assign a value to the bishop
        self.vectors = [(1, 1), (1, -1), (-1, 1), (-1, -1)]  # All possible moves for a bishop

    def get_possible_moves(self, board_present):
        possible_moves = []
        for vector in self.vectors:
            vector_ = vector
            while not core.rules.isPathBlocked(board_present, vector, self.position, status=True):
                possible_moves.append(vector)
                vector = (vector[0] + vector_[0], vector[1] + vector_[1])  # Move further in the same direction
            r, c = self.position
            d_r, d_c = vector
            n_r, n_c = r + d_r, c + d_c
            if core.rules.isinBoard(board_present, n_r, n_c) and core.rules.isPathBlocked(board_present, vector, self.position, status=True) and self.is_enemy(board_present, (n_r, n_c)):
                possible_moves.append(vector)
        return possible_moves
    def get_image_path(self):
        root_dir = helper.get_root_dir()
        if self.color == "white":
            image_path = root_dir / config.WHITE_BISHOP_PIECE_IMAGE_PATH
            return image_path
        else:
            image_path = root_dir / config.BLACK_BISHOP_PIECE_IMAGE_PATH
            return image_path
    def __str__(self):
        return "B" if self.color == "white" else "b"

    def __repr__(self):
        return self.__str__()

def main():
    row, col = 5, 5
    bishop_piece = bishop("white", position=(row, col))
    bishop_piece1 = bishop("black", position=(row+1, col+1))
    board_test = [[0 for _ in range(8)] for _ in range(8)]
    board_test[row][col] = bishop_piece
    board_test[row+1][col+1] = bishop_piece1
    possible_moves = board_test[row][col].get_possible_moves(board_test)
    for move in possible_moves:
        new_row = row + move[0]
        new_col = col + move[1]
        board_test[new_row][new_col] = 1  # Mark possible moves with 1
    for row in board_test:
        print(row)
if __name__ == "__main__":
    main()