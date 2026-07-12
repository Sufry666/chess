import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
try:
    import config # type: ignore
    import utils.helper as helper # type: ignore
except ImportError as e:
    print(f"ImportError: {e}. Please check move.py")
    sys.exit(1)


class move:
    def __init__(self, isRetract = False, isSpecialMove = False):
        self.isRetract = isRetract
        self.moves = []
        self.isSpecialMove = isSpecialMove
    def add_move(self, vector, piece, piece_captured = None):
        start = piece.position
        end = (start[0] + vector[0], start[1] + vector[1])
        self.moves.append((piece, piece_captured, start, end))
    def return_information(self):

        for piece,_,start,end in self.moves:
            return helper.coordinate_to_information(piece.name, piece.color, start, end)#待优化

        
    
    def __str__(self):
        return f"{self.piece.name} of {self.piece.color} move from {self.start} to {self.end}"
    def __repr__(self):
        return self.__str__()
        
