from piece import Piece
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
try:    
    import core.rules # type: ignore
except ImportError:
    print("Rules module not found. Please ensure that rules.py is in the same directory as king.py.")
class king(Piece):
    def __init__(self, color, name = "king", position = None):
        super().__init__(color, name, position)  # Initialize the base class with color, name, and position
        self.value = 1000  # Assign a high value to the king
        self.vectors = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]  # All possible moves for a king
    
    def get_possible_moves(self, board_present):
        possible_moves = []
        for vector in self.vectors:
                row, col = self.position
                d_row, d_col = vector
                n_row, n_col = row + d_row, col + d_col
                n_position = (n_row, n_col)
                if not core.rules.isPathBlocked(board_present, vector, self.position, status = True):
                    possible_moves.append(vector)
                if core.rules.isinBoard(board_present, n_row, n_col) and core.rules.isPathBlocked(board_present, vector, self.position, status = True) and self.is_enemy(board_present, n_position):
                    possible_moves.append(vector)
        return possible_moves
    
    def __str__(self):
        return "K" if self.color == "white" else "k"
    def __repr__(self):
        return self.__str__()
def main():
    row, col = 0,0 
    king_piece = king("white", position=(row, col))
    king_piece_1 = king("black", position=(row+1, col))
    board_test = [[0 for _ in range(8)] for _ in range(8)]
    board_test[row][col] = king_piece
    board_test[row+1][col] = king_piece_1
    
    board_test[2][4] = 2
    possible_moves = board_test[row][col].get_possible_moves(board_test)
    for move in possible_moves:
        new_row = row + move[0]
        new_col = col + move[1]
        board_test[new_row][new_col] = 1  # Mark possible moves with 1
    for row in board_test:
        print(row)

if __name__ == "__main__":
    main()
