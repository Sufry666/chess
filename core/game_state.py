import sys
import os
import pygame as pg
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
try:
    from core.board import Board # type: ignore
    from pieces.king import king # type: ignore 
    from pieces.rook import rook # type: ignore 
    from pieces.knight import knight # type: ignore 
    from pieces.bishop import bishop # type: ignore 
    from pieces.queen import queen # type: ignore 
    from pieces.pawn import pawn # type: ignore
    from ui.renderer import renderer # type: ignore
    import ui.input_handler as input_handler # type: ignore
    import config # type: ignore
    import utils.helper as helper # type: ignore
    from core.move import move # type: ignore
    import ui.animations as animations #type: ignore
    from ui.menu import menu # type: ignore
except ImportError as e:
    print(f"ImportError: {e}. Please ensure game_state.py")
    sys.exit(1)
class game:
    def __init__(self, size = 8):
        pg.init()
        self.running = False
        
        self.board_rect = pg.Rect(config.BOARD_COORDINATE[0], config.BOARD_COORDINATE[1], size*config.CELL_SIZE, size*config.CELL_SIZE) #应修改
        self.records = []
        self.board = Board()
        self.menu = menu()
        self.rook_black_left = rook("black")
        self.rook_black_right = rook("black")
        self.knight_black_left = knight("black")
        self.knight_black_right = knight("black")
        self.bishop_black_left = bishop("black")
        self.bishop_black_right = bishop("black")
        self.queen_black = queen("black")
        self.king_black = king("black")
        self.pawn_black = [0 for _ in range(8)]
        for i in range(8):
            self.pawn_black[i] = pawn("black")
        self.rook_white_left = rook("white")
        self.rook_white_right = rook("white")
        self.knight_white_left = knight("white")
        self.knight_white_right = knight("white")
        self.bishop_white_left = bishop("white")
        self.bishop_white_right = bishop("white")
        self.queen_white = queen("white")
        self.king_white = king("white")
        self.pawn_white = [0 for _ in range(8)]
        for i in range(8):
            self.pawn_white[i] = pawn("white")
    def initialize(self):
        self.renderer = renderer()
        self.board.board_list[0][4] = self.king_black
        self.board.board_list[0][3] = self.queen_black
        self.board.board_list[0][0] = self.rook_black_left
        self.board.board_list[0][7] = self.rook_black_right
        self.board.board_list[0][1] = self.knight_black_left
        self.board.board_list[0][6] = self.knight_black_right
        self.board.board_list[0][2] = self.bishop_black_left
        self.board.board_list[0][5] = self.bishop_black_right
        for i in range(8):
            self.board.board_list[1][i] = self.pawn_black[i]
            self.board.board_list[6][i] = self.pawn_white[i]
        self.board.board_list[7][4] = self.king_white
        self.board.board_list[7][3] = self.queen_white
        self.board.board_list[7][0] = self.rook_white_left
        self.board.board_list[7][7] = self.rook_white_right
        self.board.board_list[7][1] = self.knight_white_left
        self.board.board_list[7][6] = self.knight_white_right
        self.board.board_list[7][2] = self.bishop_white_left
        self.board.board_list[7][5] = self.bishop_white_right


        for idx_r, row in enumerate(self.board.board_list):
            for idx_c, piece in enumerate(row):
                if piece != 0:
                    piece.update_position((idx_r, idx_c))
        
        """self.renderer.print_board(self.board.rect_list)
        self.renderer.print_menu(self.menu.init_button_list, "start")
        self.renderer.screen.blit(self.renderer.logical_surface, self.renderer.data["logical_surface_coordinate"])"""
        self.renderer.render_handle(self)

    def run(self):
        self.player = "white"
        self.move_temp = None
        self.highlight_button = None   #待优化
        #self.highlight_piece = None#待优化
        self.pos = None
        self.running = True
        self.state = "input_getting"
        self.animation_state = "highlight"
        self.PossibleVectors = None
        self.VectorTodo = None
        self.PieceToMove = None#待优化
        self.anim = None
        self.initialize()
        while self.running:
            self.pos = pg.mouse.get_pos()
            self.pos = ((self.pos[0] - self.renderer.data["logical_surface_coordinate"][0])
                        , (self.pos[1] - self.renderer.data["logical_surface_coordinate"][1]))
            if self.state == "animation":
                animations.handle_animation(self)

            elif self.state == "input_getting" or "piece_selected":
                for event in pg.event.get()[:10]:
                    if event.type == pg.VIDEORESIZE:

                        self.renderer.update_screen(self, event.w, event.h)
                        
                    if event.type == pg.QUIT:
                        self.running = False
                    if self.state == "animation":
                        continue
                    if event.type == pg.MOUSEBUTTONDOWN:
                        input_handler.handle_click(self, event) 
                    else:
                        input_handler.handle_wait(self)
                        
            pg.display.flip()
            self.renderer.clock.tick(config.FPS)    
        pg.quit()
def test():
    game1 = game()
    
    game1.run()


if __name__ == "__main__":
    test()



    
            

