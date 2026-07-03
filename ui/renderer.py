import sys
import os
import pygame as pg
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
try:
    import config # type: ignore
    import utils.helper # type: ignore
    from core.board import Board # type: ignore

except ImportError as e:
    print(f"ImportError: {e}. Please ensure that config.py, helper.py, and core/board.py are in the correct directories.")
    sys.exit(1)

def draw_piece(screen, board_present):
    pass

def print_board():
    pg.init()
    clock = pg.time.Clock()
    pg.display.set_caption("Test Print Board")
    screen = pg.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
    screen.fill(config.BACKGROUND_COLOR)
    x = config.BOARD_COORDINATE[0]
    y = config.BOARD_COORDINATE[1]
    for i in range(8):
        for j in range(8):
            rect = pg.Rect(x + j * config.CELL_SIZE, y + i * config.CELL_SIZE, config.CELL_SIZE, config.CELL_SIZE)
            if (i + j) % 2 == 0:
                pg.draw.rect(screen, config.WHITE, rect)
            else:
                pg.draw.rect(screen, config.GRAY, rect)
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
        pg.display.update()
        clock.tick(config.FPS)
print_board()



