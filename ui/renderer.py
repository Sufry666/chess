import sys
import os
import pygame as pg
from pathlib import Path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
try:
    import config # type: ignore
    import utils.helper as helper # type: ignore
    from core.board import Board # type: ignore


except ImportError as e:
    print(f"ImportError: {e}. Please ensure that config.py, helper.py, and core/board.py are in the correct directories.")
    sys.exit(1)

class renderer:
    def __init__(self, topic = "test"):
        pg.display.set_caption(topic)

        self.clock = pg.time.Clock()
        self.screen_width = config.WINDOW_WIDTH
        self.screen_height = config.WINDOW_HEIGHT
        self.logical_surface = pg.Surface((self.screen_width, self.screen_height), pg.SRCALPHA)
        self.animation_surface = self.logical_surface.copy()
        self.data = {
            "logical_surface_coordinate" : (0, 0),
            "cell_size" : config.CELL_SIZE,
            "board_coordinate" : config.BOARD_COORDINATE,
            "menu_width" : config.MENU_WIDTH,
            "menu_height" : config.MENU_HEIGHT,
            "menu_coordinate" : config.MENU_COORDINATE
        }
        self.screen = pg.display.set_mode((self.screen_width,  self.screen_height ),pg.RESIZABLE)
        self.point_image = self.get_images(config.POSSIBLE_DESTINATION_IMAGE_PATH)
        self.font_for_init = self.get_fonts(config.FONT_PATH, 40)
        self.font_for_game = self.get_fonts(config.FONT_PATH, 18)
        
    def render_handle(self, game, state = None):
        if state == "show_possible_destination":
            self.show_possible_destination(game.PieceToMove.position, game.PossibleVectors, game.board)
            self.screen.blit(self.logical_surface, self.data["logical_surface_coordinate"])   
            return

        self.logical_surface.fill((0, 0, 0, 0))
        self.print_board(game.board.rect_list)
        if state == "highlight_button":
            self.show_button_highlight(game.highlight_button)
        
        self.print_menu(game.menu.return_button_present(), game.menu.state)
        if game.menu.state == "gaming":
            self.draw_piece(game.board)
            self.print_information(game)
        self.screen.blit(self.logical_surface, self.data["logical_surface_coordinate"])    
        
        

    def calculate(self, event_w, event_h):
        scale = min(event_w / config.WINDOW_WIDTH, event_h / config.WINDOW_HEIGHT)
        self.screen_width = scale * config.WINDOW_WIDTH
        self.screen_height = scale * config.WINDOW_HEIGHT

        self.data["logical_surface_coordinate"] = ((event_w - self.screen_width) // 2, (event_h - self.screen_height) // 2)
        self.logical_surface = pg.Surface((self.screen_width, self.screen_height), pg.SRCALPHA)
        self.animation_surface = self.logical_surface.copy()
        self.data["cell_size"] = self.screen_height / 9
        self.data["board_coordinate"] = (self.screen_height / 9, self.screen_width / 32)
        self.data["menu_width"] = self.screen_width * 5 / 16
        self.data["menu_height"] = self.data["cell_size"] * 8
        self.data["menu_coordinate"] = (self.screen_width * 5 / 8, self.screen_height / 9)

    def update_screen(self, game, event_w, event_h):
        self.calculate(event_w, event_h)
        game.menu.update_data(self.data["menu_coordinate"], self.data["menu_width"], self.data["menu_height"])
        game.board.update_data(self.data["cell_size"], self.data["board_coordinate"])
        self.point_image = self.get_images(config.POSSIBLE_DESTINATION_IMAGE_PATH)
        for row in game.board.board_list:
            for piece in row:
                if piece != 0:
                    piece.generate_image(self.data["cell_size"])
        if len(game.records) != 0:
            for move in game.records:
                for _,piece_captured,_,_ in move.moves:
                    if piece_captured:
                        piece_captured.generate_image(self.data["cell_size"])
        game.board_rect =  pg.Rect(self.data["board_coordinate"][0], self.data["board_coordinate"][1], 8 * self.data["cell_size"],  8 * self.data["cell_size"])
        self.screen = pg.display.set_mode((event_w,  event_h ),pg.RESIZABLE)
        self.render_handle(game)
    
    
    def get_images(self, path):
        root_dir = helper.get_root_dir()
        image_dir = root_dir / path
        if image_dir:
            image = pg.image.load(image_dir)
            image = pg.transform.scale(image, (self.data["cell_size"], self.data["cell_size"]))
            return image
    
    
    def get_fonts(self, path, word_size = 36):
        root_dir = helper.get_root_dir()
        font_path = root_dir / path
        if font_path:
            font = pg.font.Font(font_path, word_size)
            return font
    
    def print_words(self, text, rect = None, font = None, color = config.BLACK):

        if not font:
            font = self.font_for_init
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        x, y = rect.center
        text_rect.center =  (x, y + (rect.width / 80))
        self.logical_surface.blit(text_surface, text_rect)
        

    def draw_piece(self, board): #TODO
        
        for row in range(8):

            for col in range(8):
                piece = board.board_list[row][col]
                if piece == 0:
                    continue
                if piece.position_inscreen:
                    self.logical_surface.blit(piece.image, piece.position_inscreen)
                    continue
                x, y = board.get_position_inscreen(row, col)
                self.logical_surface.blit(piece.image, (x, y))
        
    def print_information(self, game):
        
        x = game.menu.gaming_button_list[6].rect.x
        y = game.menu.gaming_button_list[6].rect.y
        w = game.menu.gaming_button_list[6].rect.width
        information_list = [move.return_information() for move in game.records[-10:]]
        font = self.font_for_game
        for i in range(len(information_list)):
            text_surface = font.render(information_list[i], True, config.BLACK)
            text_rect = text_surface.get_rect()
            text_rect.center = (x + w / 2, y + 45 + i * 30)
            self.logical_surface.blit(text_surface, text_rect)
        

            
    def print_board(self, rect_list):
        
        self.screen.fill(config.BACKGROUND_COLOR)
        for idx_r, row in enumerate(rect_list):
            for idx_c, rect in enumerate(row):
                if (idx_r + idx_c) % 2 == 0:
                    pg.draw.rect(self.logical_surface, config.WHITE_CELL, rect)
                else:
                    pg.draw.rect(self.logical_surface, config.BLACK_CELL, rect)

    
    def show_possible_destination(self, start_position, vectors, board):

        destinations = helper.get_destinations_by_vectors(start_position, vectors)
        
        for destination in destinations:
            position = board.get_position_inscreen(destination[0], destination[1])
            self.logical_surface.blit(self.point_image, position)

    '''def cover_highlight(self, rect):
        self.logical_surface.fill((0, 0, 0, 0))
        light_rect = rect.copy()
        light_rect.x += light_rect.width / 80
        light_rect.y += light_rect.width / 80
        light_rect.inflate_ip(light_rect.width * 0.05, light_rect.height * 0.2)
        pg.draw.rect(self.logical_surface, config.BACKGROUND_COLOR, light_rect)
        self.screen.blit(self.logical_surface, self.data["logical_surface_coordinate"])'''
    def show_button_highlight(self, button):
        if not button.isButton:
            return
        light_rect = button.rect.copy()
        light_rect.x += light_rect.width / 80
        light_rect.y += light_rect.width / 80
        light_rect.inflate_ip(light_rect.width * 0.05, light_rect.height * 0.2)
        pg.draw.rect(self.logical_surface, config.BUTTON_COLOR["highlight"], light_rect, border_radius= 10 )

    
    def print_menu(self, button_list, menu_state):

        if menu_state == "start":
            font = self.font_for_init
        if menu_state == "gaming":
            font = self.font_for_game
        for button in button_list:
            if button.name == "information":
                rect_up = button.rect.copy()
                rect_up.height = 30

                pg.draw.rect(self.logical_surface, config.WHITE, button.rect, border_radius= 15)

                self.print_words(button.name, rect_up, font= font)

                continue
            shadow_rect = button.rect.copy()
            shadow_rect.x += shadow_rect.width / 80
            shadow_rect.y += shadow_rect.width / 80
            pg.draw.rect(self.logical_surface, config.BUTTON_COLOR["shadow"], shadow_rect, border_radius= 10)
            pg.draw.rect(self.logical_surface, config.BUTTON_COLOR["normal"], button.rect, border_radius= 10)
            self.print_words(button.name, button.rect, font= font)
           
def main():
    board1 = Board()

    board1.board_list[0][4] = king_black
    
    print(type(board1.board_list))
if __name__ == "__main__":
    main()

        


        

