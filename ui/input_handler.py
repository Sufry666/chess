import os
import sys
import pygame as pg
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
try:
    import config # type: ignore
    import core.board as board # type: ignore
    import utils.helper as helper # type: ignore
    from core.move import move #type: ignore
except ImportError as e:
    print(f"ImportError: {e}. Please ensure input_handler.py")
    sys.exit(1)
def get_mouse_coordinate_in_board(rect_list,mouse_position):
    for idx_r, row in enumerate(rect_list):
        for idx_c, rect in enumerate(row):
            if rect.collidepoint(mouse_position):
                return (idx_r, idx_c)

def handle_click(game, click):
    if click.button != 1:
        return
    if game.menu.rect.collidepoint(game.pos):
        handle_click_inmenu(game)
        return
    if game.menu.state == "start":
        return
    if game.board_rect.collidepoint(game.pos):
        handle_click_inboard(game)
        return
    

def handle_click_inboard(game):
    row, col = get_mouse_coordinate_in_board(game.board.rect_list,game.pos)
    if game.state == "input_getting":
        if game.board.board_list[row][col] == 0:
            return
        #TODO:待优化，需判断执棋者阵营，为做测试暂不写
        game.state = "piece_selected"
        game.PieceToMove = game.board.board_list[row][col]
        game.PossibleVectors = game.PieceToMove.get_possible_moves(game.board.board_list)
        game.renderer.show_possible_destination((row, col),game.PossibleVectors)
        game.VectorTodo = (row, col)
        
        return
    if game.state == "piece_selected":
        game.VectorTodo = (row - game.VectorTodo[0], col - game.VectorTodo[1])
        if game.VectorTodo not in game.PossibleVectors:
            game.renderer.print_board(game.board.rect_list)
            game.renderer.draw_piece(game.board.board_list)
            game.state = "input_getting"
            game.state = "animation"
            return
        move_temp = move(vector = game.VectorTodo, piece = game.PieceToMove)
        game.renderer.print_board(game.board.rect_list)
        game.renderer.draw_piece(game.board.board_list)
        game.records.append(move_temp)
        print(game.records)
        game.highlight_piece = None
        game.state = "animation"
        return

def handle_click_inmenu(game):
    if game.menu.state == "gaming":
        return
    for button in game.menu.return_button_present():
        if not button.rect.collidepoint(game.pos):
            continue
        if button.name == "PVP":
            game.menu.state = "gaming"
            game.renderer.print_board(game.board.rect_list)
            game.renderer.draw_piece(game.board.board_list)
            return
        if button.name == "Exit":
            game.running = False
            return
def handle_wait(game):
    if game.menu.state == "start":
        if not game.highlight_button:
            handle_wait_inmenu(game)
            return
        if not game.highlight_button.rect.collidepoint(game.pos):
            game.renderer.cover_highlight(game.menu.rect)
            game.renderer.print_menu(game.menu.return_button_present())
            game.highlight_button = None
            return

    if game.menu.state == "gaming":
        if game.state == "piece_selected":
            return
        if not game.highlight_piece:
            handle_wait_inboard(game)
            return
        if not game.board.rect_list[game.highlight_piece.position[0]][game.highlight_piece.position[1]].collidepoint(game.pos):
            game.renderer.print_board(game.board.rect_list)
            game.renderer.draw_piece(game.board.board_list)
            game.highlight_piece = None
            return 
        


def handle_wait_inmenu(game):
    if not game.menu.rect.collidepoint(game.pos):
            
        return
    
    for button in game.menu.return_button_present():
        if not button.rect.collidepoint(game.pos):
            continue
            
        game.renderer.show_button_highlight(button)
        game.highlight_button = button
        game.renderer.print_menu(game.menu.return_button_present())
        return


def handle_wait_inboard(game):
    
    if not game.board_rect.collidepoint(game.pos):
        return
    row, col = get_mouse_coordinate_in_board(game.board.rect_list,game.pos)

    if game.board.board_list[row][col] == 0:
        return
    game.highlight_piece = game.board.board_list[row][col]
    game.state = "animation"
    