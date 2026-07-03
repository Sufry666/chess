import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
try:
    import config # type: ignore
except ImportError:
    print("Config module not found. Please ensure that config.py is in the same directory as helper.py.")
def index_to_position(row, col):
    x = config.BOARD_COORDINATE[0] + col * config.CELL_SIZE
    y = config.BOARD_COORDINATE[1] + row * config.CELL_SIZE
    return (x, y)