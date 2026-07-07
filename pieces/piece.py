from abc import ABC, abstractmethod
import sys
import os
import pygame as pg
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
try:    
    import core.rules # type: ignore
    import config # type: ignore
    import utils.helper as helper # type: ignore
except ImportError:
    print("Rules module not found. Please ensure that rules.py is in the same directory as piece.py.")

class Piece(ABC):
    def __init__(self, color, name, position = None):#position is a tuple representing the position of the piece on the board (row, column)
        self.color = color
        self.name = name
        self.position = position
        self.position_inscreen = None
        self.generate_image()
        
    @abstractmethod
    def get_possible_moves(self, board_present):
        pass
    @abstractmethod
    def get_image_path(self):
        pass

    def update_position(self, new_position):
        self.position = new_position

    def is_enemy(self, board_present, new_position):#需要保证此处有棋子
        row, col = new_position
        if self.color != board_present[row][col].color:
            return True
    
    def generate_image(self):
        image_path = self.get_image_path()
        if image_path:
            self.image = pg.image.load(image_path)
            self.image = pg.transform.scale(self.image, (config.CELL_SIZE, config.CELL_SIZE))
            
    
    