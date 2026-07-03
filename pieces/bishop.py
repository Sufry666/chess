from piece import Piece
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
try:    
    import core.rules # type: ignore
except ImportError:
    print("Rules module not found. Please ensure that rules.py is in the same directory as bishop.py.")
class bishop(Piece):
    def __init__(self, color, name = "bishop", position = None, ):
        super().__init__(color, name, position)  # Initialize the base class with color, name, and position
        self.value = 3  # Assign a value to the bishop
        self.vectors = [(1, 1), (1, -1), (-1, 1), (-1, -1)]  # All possible moves for a bishop

    def get_possible_moves(self, board_present):
        possible_moves = []
        for vector in self.vectors:
            while not core.rules.isPathBlocked(board_present, vector, self.position, status=True):
                possible_moves.append(vector)
                vector = (vector[0] + vector[0], vector[1] + vector[1])  # Move further in the same direction
        return possible_moves

    def __str__(self):
        return "B" if self.color == "white" else "b"

    def __repr__(self):
        return self.__str__()

def main():
    row, col = 4, 4
    bishop_piece = bishop("white", position=(row, col))
    board_test = [[0 for _ in range(8)] for _ in range(8)]
    board_test[row][col] = bishop_piece
    board_test[2][2] = 2
    possible_moves = board_test[row][col].get_possible_moves(board_test)
    for move in possible_moves:
        new_row = row + move[0]
        new_col = col + move[1]
        board_test[new_row][new_col] = 1  # Mark possible moves with 1
    for row in board_test:
        print(row)
if __name__ == "__main__":
    main()