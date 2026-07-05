import sys
import os
import pygame as pg
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
try:
    from core.board import Board # type: ignore
    from pieces.king import king # type: ignore 
    from pieces.rook import rook # type: ignore 
    from ui.renderer import renderer # type: ignore
    import ui.input_handler as input_handler # type: ignore
    import config # type: ignore
    import utils.helper as helper # type: ignore
    from core.move import move # type: ignore
except ImportError as e:
    print(f"ImportError: {e}. Please ensure game_state.py")
    sys.exit(1)
class game:
    def __init__(self, size = 8):
        pg.init()
        self.running = False
        x , y= helper.index_to_position(0, 0)
        self.board_rect = pg.Rect(x, y, size*config.CELL_SIZE, size*config.CELL_SIZE)
        self.records = []
        self.board = Board()
        self.rook_black = rook("black")
        self.king_black = king("black")
    def initialize(self):
        self.renderer = renderer()
        self.board.board_list[0][4] = self.king_black
        self.board.board_list[2][6] = self.rook_black
        self.king_black.update_position((0, 4))
        self.rook_black.update_position((2, 6))
        self.renderer.print_board(self.board.rect_list)
    def update_a_step(self, ):
        pass
    def run(self):
        self.running = True
        isTapPiece = False
        PossibleVectors = None
        VectorTodo = None
        PieceToMove = None
        self.initialize()
        while self.running:
            self.renderer.draw_piece(self.board.board_list)
            for event in pg.event.get()[:10]:
                if event.type == pg.QUIT:
                    self.running = False
                if event.type == pg.MOUSEMOTION:
                    continue
                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.board_rect.collidepoint(event.pos):
                            row, col = input_handler.get_mouse_coordinate_in_board(self.board.rect_list,event.pos)
                            if isTapPiece:
                                VectorTodo = (row - VectorTodo[0], col - VectorTodo[1])
                                if VectorTodo in PossibleVectors:
                                    
                                    move_temp = move(vector = VectorTodo, piece = PieceToMove)
                                    self.board.update(move_temp)
                                    self.renderer.print_board(self.board.rect_list)
                                    self.renderer.draw_piece(self.board.board_list)
                                    self.records.append(move_temp)
                                    isTapPiece = False
                                else:
                                    self.renderer.print_board(self.board.rect_list)
                                    self.renderer.draw_piece(self.board.board_list)
                                    isTapPiece = False
                            elif self.board.board_list[row][col] != 0 and not isTapPiece:#and 判断谁走
                                isTapPiece = True
                                PossibleVectors = self.board.board_list[row][col].get_possible_moves(self.board.board_list)
                                self.renderer.show_possible_destination((row, col),PossibleVectors )
                                VectorTodo = (row, col)
                                PieceToMove = self.board.board_list[row][col]
            pg.display.flip()
            self.renderer.clock.tick(config.FPS)    
        pg.quit()
def test():
    game1 = game()
    """game1.initialize()
    print(type(game1.board.board_list))
    game1.renderer.draw_piece(game1.board.board_list)
    pg.display.flip()
    pg.time.wait(5000)"""
    game1.run()
    #print(game1.board_rect)

if __name__ == "__main__":
    test()



    
            

