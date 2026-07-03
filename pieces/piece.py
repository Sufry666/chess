from abc import ABC, abstractmethod


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