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
    def __init__(self,vector, piece, piece_captured = None, isRetract = False, isSpecialMove = False):
        self.isRetract = isRetract
        self.piece_captured = piece_captured
        self.vector = vector
        self.piece = piece #pice is an instance of the piece class
        self.start = piece.position
        self.end = (self.start[0] + self.vector[0], self.start[1] + self.vector[1])
        self.isSpecialMove = isSpecialMove
    
    def return_information(self):
        return helper.coordinate_to_information(self.piece.name, self.piece.color, self.start, self.end)
    
    def __str__(self):
        return f"{self.piece.name} of {self.piece.color} move from {self.start} to {self.end}"
    def __repr__(self):
        return self.__str__()
        
