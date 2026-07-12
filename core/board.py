import os
import sys
import pygame as pg
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
try:
    import config # type: ignore

    #from core.move import move # type: ignore
except ImportError as e:
    print(f"ImportError: {e}. Please ensure board.py")
    sys.exit(1)
class Board:
    def __init__(self, board_list = None, size = 8):  # Default size is 8 for an 8x8 board
        self.size = size
        self.cell_size = config.CELL_SIZE
        self.board_coordinate = config.BOARD_COORDINATE
        self.board_list = board_list if board_list is not None else [[0 for _ in range(size)] for _ in range(size)]
        self.rect_list = []
        for i in range(size):
            row = []
            for j in range(size):
                x , y= self.get_position_inscreen(i, j)
                row.append(pg.Rect(x, y, config.CELL_SIZE, config.CELL_SIZE))
            self.rect_list.append(row)
    
    def update_data(self, cell_size, board_coordinate):
        self.cell_size = cell_size
        self.board_coordinate = board_coordinate
        for idx_r, row in enumerate(self.rect_list):
            for idx_c, rect in enumerate(row):
                rect.x , rect.y = self.get_position_inscreen(idx_r, idx_c)
                rect.width = self.cell_size
                rect.height = self.cell_size
    
    def get_position_inscreen(self, row, col):
        x = self.board_coordinate[0] + col * self.cell_size
        y = self.board_coordinate[1] + row * self.cell_size
        return (x, y)
    
    def update(self, move):
        if not move:
            return
        for piece, piece_captured, start, end in move.moves:
            if move.isRetract:
                start_x, start_y = end
                end_x, end_y = start
            else:
                start_x, start_y = start
                end_x, end_y = end
            piece.update_position((end_x, end_y))

            self.board_list[end_x][end_y] = piece
            
            if  move.isSpecialMove == True: # 若move为吃过路兵
                self.board_list[end_x - piece.direction][end_y] = 0 # 将被吃的过路兵所在位置设为 0
            if  move.isRetract and piece_captured:
                if move.isSpecialMove == True: # 若move为吃过路兵 且此时为悔棋
                    self.board_list[start_x - piece.direction][start_y] = piece_captured # 将被吃兵在原位还原
                else:
                    self.board_list[start_x][start_y] = piece_captured
                    return
            self.board_list[start_x][start_y] = 0

    



def main():
    board1 = Board()
    print(board1.board_list)
    print(board1.rect_list)
if __name__ == "__main__":
    main()
