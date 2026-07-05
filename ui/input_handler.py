import os
import sys
import pygame as pg
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
try:
    import config # type: ignore
    import core.board as board # type: ignore
    import utils.helper as helper # type: ignore
except ImportError as e:
    print(f"ImportError: {e}. Please ensure input_handler.py")
    sys.exit(1)
def get_mouse_coordinate_in_board(rect_list,mouse_position):
    for idx_r, row in enumerate(rect_list):
        for idx_c, rect in enumerate(row):
            if rect.collidepoint(mouse_position):
                return (idx_r, idx_c)
def get_piece_in_board(board_present):
    row, col = get_mouse_coordinate_in_board()                
    if board_present[row][col] == 0:
        return None
    else:
        return board_present[row][col].name