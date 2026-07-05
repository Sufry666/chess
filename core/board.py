import os
import sys
import pygame as pg
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
try:
    import config # type: ignore
    import utils.helper as helper # type: ignore
    from core.move import move # type: ignore
except ImportError as e:
    print(f"ImportError: {e}. Please ensure board.py")
    sys.exit(1)
class Board:
    def __init__(self, board_list = None, size = 8):  # Default size is 8 for an 8x8 board
        self.size = size
        self.board_list = board_list if board_list is not None else [[0 for _ in range(size)] for _ in range(size)]
        self.rect_list = []
        for i in range(size):
            row = []
            for j in range(size):
                x , y= helper.index_to_position(i, j)
                row.append(pg.Rect(x, y, config.CELL_SIZE, config.CELL_SIZE))
            self.rect_list.append(row)

    def update(self, move):
        start_x, start_y = move.start
        end_x, end_y = move.end
        move.piece.update_position((end_x, end_y))
        self.board_list[end_x][end_y] = move.piece
        self.board_list[start_x][start_y] = 0
               
def main():
    board1 = Board()
    print(board1.board_list)
    print(board1.rect_list)
if __name__ == "__main__":
    main()
