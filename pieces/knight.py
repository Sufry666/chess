from piece import Piece
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
try:    
    import core.rules # type: ignore
except ImportError:
    print("Rules module not found. Please ensure that rules.py is in the same directory as knight.py.")
class knight(Piece):
    pass