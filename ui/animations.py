import sys
import os
import pygame as pg
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
try:    
    import utils.helper as helper # type: ignore
    import config # type: ignore
    from core.move import move # type: ignore
    from pieces.king import king # type: ignore
    from ui.renderer import renderer # type: ignore
    from core.board import Board # type: ignore
except ImportError as e:
    print(f"{e}. Please check animations.py.")
def get_moving_position(idx_s, idx_e, duration = config.ANIMATION_TIME, board = None):
    if board == None:
        return
    start_position =board.get_position_inscreen(idx_s[0], idx_s[1]) #TODO
    end_position = board.get_position_inscreen(idx_e[0], idx_e[1]) #TODO
    dx = end_position[0] - start_position[0]
    dy = end_position[1] - start_position[1]
    start_time = pg.time.get_ticks()
    while True:
        dt = pg.time.get_ticks() - start_time
        if dt >= duration:
            yield end_position
            return
        process = dt / duration
        position_present = (start_position[0] + dx * process, start_position[1] + dy * process)
        yield position_present

def show_highlight_piece(game):
    idx_s = game.PieceToMove.position
    idx_e = (idx_s[0] - 0.1, idx_s[1])
    get = get_moving_position(idx_s= idx_s, idx_e= idx_e, duration= 50, board= game.board)
    while True:
        try:
            game.PieceToMove.position_inscreen = next(get)
            '''game.renderer.print_board(game.board.rect_list)
            game.renderer.draw_piece(game.board)
            game.renderer.print_menu(game.menu.return_button_present(), game.menu.state)
            game.renderer.print_information(game)'''
            game.renderer.render_handle(game)
            yield
        except StopIteration:
            return

def move_animation(game):
    
    if not game.move_temp:
        return
    gets = []
    for piece, _, start, end in game.move_temp.moves:
        if game.move_temp.isRetract:
            idx_s = end
            idx_e = start
        else:
            idx_s = start
            idx_e = end
        gets.append((piece, get_moving_position(idx_s= idx_s, idx_e= idx_e, board= game.board)))
    
    
    while True:
        try:
            for piece, get in gets:
                piece.position_inscreen = next(get)
                '''game.renderer.print_board(game.board.rect_list)
                game.renderer.draw_piece(game.board)
                game.renderer.print_menu(game.menu.return_button_present(), game.menu.state)
                game.renderer.print_information(game)'''
                game.renderer.render_handle(game)
            yield
        except StopIteration:
            return





def handle_animation(game):
    if not game.animation_state:
        game.state = "input_getting"
        return
    if not game.anim and game.animation_state == "move":
        game.anim = move_animation(game)
        
    if not game.anim and game.animation_state == "highlight":
        game.anim = show_highlight_piece(game)
    try:
        next(game.anim)
    except StopIteration:
        if not game.PieceToMove and game.move_temp:
            
            #game.board.update(game.move_temp)
            '''game.renderer.print_board(game.board.rect_list)
            game.renderer.draw_piece(game.board)
            game.renderer.print_menu(game.menu.return_button_present(), game.menu.state)
            game.renderer.print_information(game)'''
            game.board.update(game.move_temp)
            game.renderer.render_handle(game)
            for piece,_,_,_ in game.move_temp.moves:
                piece.position_inscreen = None
            game.move_temp = None
            game.anim = None
            game.state = "input_getting"
            game.animation_state = None
        else:
            game.anim = None
            game.state = "input_getting"
            game.PieceToMove.position_inscreen = None
            game.animation_state = None


def main():
    pg.init()
    renderer_test = renderer()
    king_black = king("black",(0, 4))
    board_test = Board()
    board_test.board_list[0][4] = king_black
    test = get_moving_position((0, 4), (5, 5))
    while True:
        king_black.position_inscreen = next(test)
        print(king_black.position_inscreen)
        renderer_test.print_board(board_test.rect_list)
        renderer_test.draw_piece(board_test)
        pg.display.flip()
        renderer_test.clock.tick(60)
if __name__ == "__main__":
    main()
    

        