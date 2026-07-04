from piece import Piece
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
try:    
    import core.rules # type: ignore
except ImportError:
    print("Rules module not found. Please ensure that rules.py is in the same directory as pawn.py.")
class pawn(Piece):
    def __init__(self, color, name = "pawn", position = None):
        super().__init__(color, name, position)
        self.value = 1
        self.vectors_1 = [(1, 0)]
        self.vectors_2 = [(2, 0)]
        self.vectors_3 = [(1, -1), (1, 1)]
        self.direction = -1 if color == 'white' else 1
        self.init_position = position
    
    def get_possible_moves(self, board_present):
        possible_moves = []
        for vector in self.vectors_1:
            if not core.rules.isPathBlocked(board_present, (vector[0] * self.direction, vector[1]), self.position, status=True):
                possible_moves.append((vector[0] * self.direction, vector[1]))
                for vector in self.vectors_2:
                    if self.position == self.init_position and (not core.rules.isPathBlocked(board_present, (vector[0] * self.direction, vector[1]), self.position, status=True)):
                        possible_moves.append((vector[0] * self.direction, vector[1]))
        for vector in self.vectors_3:
            n_r, n_c = vector[0] * self.direction + self.position[0], vector[1] + self.position[1]
            if core.rules.isPathBlocked(board_present, (self.direction * vector[0], vector[1]), self.position, status=True) and core.rules.isinBoard(board_present, n_r, n_c) and self.is_enemy(board_present, (n_r, n_c)):
                possible_moves.append((self.direction * vector[0], vector[1]))
        return possible_moves
    
    def __str__(self):
        return "P" if self.color == "white" else "p"

    def __repr__(self):
        return self.__str__()
    
def main():
    row, col = 5, 5
    pawn_piece = pawn("white", position=(6, 4))
    pawn_piece1 = pawn("black", position=(1, 3))
    board_test = [[0 for _ in range(8)] for _ in range(8)]
    board_test[1][3] = pawn_piece1
    board_test[3][3] = pawn_piece
    pawn_piece1.position = (1, 3)
    possible_moves = board_test[1][3].get_possible_moves(board_test)
    for move in possible_moves:
        new_row = 1 + move[0]
        new_col = 3 + move[1]
        board_test[new_row][new_col] = 1
    for row in board_test:
        print(row)
if __name__ == "__main__":
    main()