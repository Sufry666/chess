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
        self.point_image = self.get_images(config.POSSIBLE_DESTINATION_IMAGE_PATH)
        self.font = self.get_fonts(config.FONT_PATH, 40)
    
    
    def get_images(self, path):
        root_dir = helper.get_root_dir()
        image_dir = root_dir / path
        if image_dir:
            image = pg.image.load(image_dir)
            image = pg.transform.scale(image, (config.CELL_SIZE, config.CELL_SIZE))
            return image
    
    
    def get_fonts(self, path, word_size = 36):
        root_dir = helper.get_root_dir()
        font_path = root_dir / path
        if font_path:
            font = pg.font.Font(font_path, word_size)
            return font
    
    def print_words(self, text, rect = None, font = None, color = config.BLACK):
        if not font:
            font = self.font
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        x, y = rect.center
        text_rect.center =  (x, y + 8)
        self.screen.blit(text_surface, text_rect)
    

    def draw_piece(self, board_present):
        for row in range(8):
            for col in range(8):
                piece = board_present[row][col]
                if piece == 0:
                    continue
                if piece.position_inscreen:
                    self.screen.blit(piece.image, piece.position_inscreen)
                    continue
                x, y = helper.index_to_position(row, col)
                self.screen.blit(piece.image, (x, y))

    def print_board(self, rect_list):

        self.screen.fill(config.BACKGROUND_COLOR)
        for idx_r, row in enumerate(rect_list):
            for idx_c, rect in enumerate(row):
                if (idx_r + idx_c) % 2 == 0:
                    pg.draw.rect(self.screen, config.WHITE_CELL, rect)
                else:
                    pg.draw.rect(self.screen, config.BLACK_CELL, rect)
    
    
    def show_possible_destination(self, start_position, vectors):
       
        destinations = helper.get_destinations_by_vectors(start_position, vectors)
        
        for destination in destinations:
            position = helper.index_to_position(destination[0], destination[1])
            self.screen.blit(self.point_image, position)
    
    def cover_highlight(self, rect):
        pg.draw.rect(self.screen, config.BACKGROUND_COLOR, rect)
    
    def show_button_highlight(self, button):
        light_rect = button.rect.copy()
        light_rect.x += 4
        light_rect.y += 4
        light_rect.inflate_ip(light_rect.width * 0.05, light_rect.height * 0.2)
        pg.draw.rect(self.screen, config.BUTTON_COLOR["highlight"], light_rect, border_radius= 10 )
    def print_menu(self, button_list):
        for button in button_list:
            shadow_rect = button.rect.copy()
            shadow_rect.x += 4
            shadow_rect.y += 4
            pg.draw.rect(self.screen, config.BUTTON_COLOR["shadow"], shadow_rect, border_radius= 10)
            pg.draw.rect(self.screen, config.BUTTON_COLOR["normal"], button.rect, border_radius= 10)
            self.print_words(button.name, button.rect)

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

        


        

