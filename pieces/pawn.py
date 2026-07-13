import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
try:    
    from pieces.piece import Piece # type: ignore
    import core.rules # type: ignore
    import utils.helper as helper # type: ignore
    import config # type: ignore
except ImportError as e:
    print(f"{e}. Please check king.py.")
class pawn(Piece):
    def __init__(self, color, name = "pawn", position = None):
        super().__init__(color, name, position)  # Initialize the base class with color, name, and position
        self.value = 1000
        self.vectors = [(1, 0)]
        self.vectors_ = [(1, 1), (1, -1)]
        self.direction = 1 if self.color == 'black' else -1
        self.row_condition = 4 if self.color == 'black' else 3 #该值表示吃过路兵所需要在的行数
        
    def get_possible_moves_origin(self, board_present):
        possible_moves = []
        for vector in self.vectors:
            vector = (vector[0] * self.direction, vector[1])
            if not core.rules.isPathBlocked(board_present, vector, self.position, True):
                possible_moves.append(vector)
                if self.moved_times == 0:
                    if not core.rules.isPathBlocked(board_present, (2 * self.direction, 0), self.position, True):
                        possible_moves.append((2 * self.direction, 0))
        for vector in self.vectors_:
            vector = (vector[0] * self.direction, vector[1])
            if core.rules.isPathBlocked(board_present, vector, self.position, True):
                r, c = self.position
                d_r, d_c = vector
                n_r, n_c = r + d_r, c + d_c
                if core.rules.isinBoard(board_present, n_r, n_c) and self.is_enemy(board_present, (n_r, n_c)):
                    possible_moves.append(vector)
                    continue
            if self.position[0] == self.row_condition:
                position1 = (self.position[0], self.position[1] - 1)
                position2 = (self.position[0], self.position[1] + 1)
                if core.rules.isinBoard(board_present, self.position[0], self.position[1] - 1) and board_present[self.position[0]][self.position[1] - 1] != 0:
                    if board_present[self.position[0]][self.position[1] - 1].name == "pawn" and board_present[self.position[0]][self.position[1] - 1].is_moved_latest == True and board_present[self.position[0]][self.position[1] - 1].moved_times == 1 and self.is_enemy(board_present, position1) == True:
                        possible_moves.append((1 * self.direction, -1))
                if core.rules.isinBoard(board_present, self.position[0], self.position[1] + 1) and board_present[self.position[0]][self.position[1] + 1] != 0:
                    if board_present[self.position[0]][self.position[1] + 1].name == "pawn" and board_present[self.position[0]][self.position[1] + 1].is_moved_latest == True and board_present[self.position[0]][self.position[1] + 1].moved_times == 1 and self.is_enemy(board_present, position2) == True:
                        possible_moves.append((1 * self.direction, 1))
                        
        return possible_moves
    
    def get_possible_moves(self, board_present):
        vectors = self.get_possible_moves_origin(board_present)
        possible_moves_final = []
        for vector in vectors:
            if not core.rules.will_be_Chessmate(board_present, self.position, vector, self.color):
                possible_moves_final.append(vector)
        return possible_moves_final
    
    def get_image_path(self):
        root_dir = helper.get_root_dir()
        if self.color == "white":
            image_path = root_dir / config.WHITE_PAWN_PIECE_IMAGE_PATH
            return image_path
        else:
            image_path = root_dir / config.BLACK_PAWN_PIECE_IMAGE_PATH
            return image_path
    def __str__(self):
        return "P" if self.color == "white" else "p"
    def __repr__(self):
        return self.__str__()
