from abc import ABC, abstractmethod
import sys
import os
import pygame as pg
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
try:    

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
        self.moved_times = 0 #棋子被移动过的次数
        self.generate_image(config.CELL_SIZE)
        self.is_moved_latest = False #该值表示本棋子是否为双方所有棋子中最新被移动的棋子
        
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

    
    def generate_image(self, cell_size):
        image_path = self.get_image_path()
        if image_path:
            self.image = pg.image.load(image_path).convert_alpha()
            self.image = pg.transform.scale(self.image, (cell_size, cell_size))
            
    
        
    