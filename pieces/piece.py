from abc import ABC, abstractmethod
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
try:    
    import core.rules # type: ignore
except ImportError:
    print("Rules module not found. Please ensure that rules.py is in the same directory as piece.py.")

class Piece(ABC):
    def __init__(self, color, name, position = None):#position is a tuple representing the position of the piece on the board (row, column)
        self.color = color
        self.name = name
        self.position = position

    @abstractmethod
    def get_possible_moves(self, board_present):
        pass

    def update_position(self, new_position):
        self.position = new_position

    def is_enemy(self, board_present, new_position):#需要保证此处有棋子
        row, col = new_position
        if self.color != board_present[row][col].color:
            return True