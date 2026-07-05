import sys
import os
from pathlib import Path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
try:
    import config # type: ignore
except ImportError:
    print("Config module not found. Please ensure that config.py is in the same directory as helper.py.")
def index_to_position(row, col):
    x = config.BOARD_COORDINATE[0] + col * config.CELL_SIZE
    y = config.BOARD_COORDINATE[1] + row * config.CELL_SIZE
    return (x, y)

def get_root_dir():
    current = Path(__file__).resolve()
    for parent in  current.parents:
        if (parent / "data").exists():
            return parent

def get_destinations_by_vectors(start_position, vectors):
    destinations = []
    for vector in vectors:
        destination = (start_position[0] + vector[0], start_position[1] + vector[1])
        destinations.append(destination)
    return destinations