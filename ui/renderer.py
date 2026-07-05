import sys
import os
import pygame as pg
from pathlib import Path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
try:
    import config # type: ignore
    import utils.helper as helper # type: ignore
    from core.board import Board # type: ignore
    from pieces.king import king # type: ignore

except ImportError as e:
    print(f"ImportError: {e}. Please ensure that config.py, helper.py, and core/board.py are in the correct directories.")
    sys.exit(1)

class renderer:
    def __init__(self, topic = "test"):
        pg.display.set_caption(topic)
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))


    def draw_piece(self, board_present):
        for row in range(8):
            for col in range(8):
                piece = board_present[row][col]
                if piece != 0:
                    image_path = piece.get_image_path()
                    if image_path:
                        image = pg.image.load(image_path)
                        image = pg.transform.scale(image, (config.CELL_SIZE, config.CELL_SIZE))
                        x, y = helper.index_to_position(row, col)
                        self.screen.blit(image, (x, y))

    def print_board(self, rect_list):

        self.screen.fill(config.BACKGROUND_COLOR)
        for idx_r, row in enumerate(rect_list):
            for idx_c, rect in enumerate(row):
                if (idx_r + idx_c) % 2 == 0:
                    pg.draw.rect(self.screen, config.WHITE, rect)
                else:
                    pg.draw.rect(self.screen, config.GRAY, rect)
    def show_possible_destination(self, start_position, vectors):
        root_dir = helper.get_root_dir()
        point_dir = root_dir / config.POSSIBLE_DESTINATION_IMAGE_PATH
        destinations = helper.get_destinations_by_vectors(start_position, vectors)
        if point_dir:
            image = pg.image.load(point_dir)
            image = pg.transform.scale(image, (config.CELL_SIZE, config.CELL_SIZE))
            for destination in destinations:
                position = helper.index_to_position(destination[0], destination[1])
                self.screen.blit(image, position)
def main():
    board1 = Board()
    king_black = king("black", position = (0, 4))
    board1.board_list[0][4] = king_black
    """pg.init()
    renderer1 = renderer()
    renderer1.screen = pg.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
    renderer1.print_board(board1.rect_list)
    renderer1.draw_piece(board1.board_list)
    pg.display.flip()
    pg.time.wait(5000)"""
    print(type(board1.board_list))
if __name__ == "__main__":
    main()

        


        

