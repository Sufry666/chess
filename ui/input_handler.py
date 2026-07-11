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
        if game.board.board_list[row][col].color != game.player:
            return
        game.state = "piece_selected"
        game.PieceToMove = game.board.board_list[row][col]
        if game.highlight_piece and game.highlight_piece != game.PieceToMove:
            game.highlight_piece = game.PieceToMove
        game.PossibleVectors = game.PieceToMove.get_possible_moves(game.board.board_list)
        game.renderer.show_possible_destination((row, col),game.PossibleVectors)
        game.VectorTodo = (row, col)
        
        return
    if game.state == "piece_selected":
        game.VectorTodo = (row - game.VectorTodo[0], col - game.VectorTodo[1])
        if game.VectorTodo not in game.PossibleVectors:
           
            game.state = "input_getting"
            game.state = "animation"
            return
        if len(game.records) != 0:
            game.records[-1].piece.is_moved_latest = False # 移动前更新上一个被移动的棋子的 最后移动的棋子 这一数据
        if game.board.board_list[row][col] != 0: # 此情况为终点有子 必定为正常吃子
            game.move_temp = move(vector = game.VectorTodo, piece = game.PieceToMove, piece_captured = game.board.board_list[row][col])
        elif game.PieceToMove.name == "pawn" and game.VectorTodo[1] != 0: # 由于前一种情况为终点有子 故此处及后续情况均为终点无子 若被移动的棋子为pawn（此if的条件1）且移动方向不为竖直 即col坐标改变（此if的条件2） 说明该移动一定是吃过路兵
            game.move_temp = move(vector = game.VectorTodo, piece = game.PieceToMove, piece_captured = game.board.board_list[row - game.PieceToMove.direction][col], isSpecialMove = True)
        else: # 由于上述情况将 终点有子 与 终点无子且pawn斜着走 讨论完毕 故此情况必定为终点无子的常规移动
            game.move_temp = move(vector = game.VectorTodo, piece = game.PieceToMove)
        if game.player == "black":
            game.player = "white"
        else:
            game.player = "black"
        game.move_temp.piece.moved_times += 1
        game.PieceToMove.is_moved_latest = True #移动后更新 最后移动的棋子 这一数据
        game.records.append(game.move_temp)
        #print(game.records) # 加入窗口显示
        print(game.board.board_list)
        
        game.highlight_piece = None
        game.state = "animation"
        return

def handle_click_inmenu(game):
    for button in game.menu.return_button_present():
        if not button.rect.collidepoint(game.pos):
            continue
        if button.name == "exit" and game.menu.state == "gaming":
            game.menu.state = "start"
            game.renderer.print_board(game.board.rect_list)
            game.renderer.print_menu(game.menu.return_button_present())
            return
        if button.name == "retract":
            if len(game.records) == 0:
                return
            if game.player == "black":
                game.player = "white"
            else:
                game.player = "black"
            game.records[-1].piece.is_moved_latest = False # 悔棋前将回退步中移动的棋子的 最后移动的棋子 这一数据更新为False
            game.move_temp = game.records.pop()
            game.move_temp.isRetract = True
            game.move_temp.piece.moved_times -= 1
            temp = game.move_temp.start
            game.move_temp.start = game.move_temp.end
            game.move_temp.end = temp
            if len(game.records) != 0:
                game.records[-1].piece.is_moved_latest = True #悔棋后将此时的最后移动操作中被移动的棋子的 最后移动的棋子 这一数据更新为True
            game.state = "animation"
            return
        if button.name == "PVP":
            game.menu.state = "gaming"
            game.renderer.print_board(game.board.rect_list)
            game.renderer.draw_piece(game.board.board_list)
            game.renderer.print_menu(game.menu.return_button_present(), game.renderer.font_for_game)
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
            game.renderer.cover_highlight(game.highlight_button.rect)
            game.renderer.print_menu(game.menu.return_button_present())
            game.highlight_button = None
            return

    if game.menu.state == "gaming":
        if game.highlight_piece and not game.board_rect.collidepoint(game.pos):
            if game.state != "piece_selected":
                
                game.renderer.print_board(game.board.rect_list)
                game.renderer.draw_piece(game.board.board_list)
                game.renderer.print_menu(game.menu.return_button_present(), game.renderer.font_for_game)
                game.renderer.print_information(game)
                game.highlight_piece = None
            else:
                pass
        if game.menu.rect.collidepoint(game.pos):
            
            if not game.highlight_button:
                handle_wait_inmenu(game)
                return
            if not game.highlight_button.rect.collidepoint(game.pos) :
                game.renderer.cover_highlight(game.highlight_button.rect)
                game.renderer.print_menu(game.menu.return_button_present(), game.renderer.font_for_game)
                game.renderer.print_information(game)
                game.highlight_button = None
                return
        elif game.board_rect.collidepoint(game.pos):
            if game.state == "piece_selected":
                return
            
            handle_wait_inboard(game)
            return

def handle_wait_inmenu(game):
    if not game.menu.rect.collidepoint(game.pos):
            
        return
    
    for button in game.menu.return_button_present():
        if not button.rect.collidepoint(game.pos):
            continue
        if button.name == "information":
            continue
        if game.state == "piece_selected":
            game.state = "animation"
        game.renderer.show_button_highlight(button)
        

        game.highlight_button = button
        
        if game.menu.state == "gaming":
            
            game.renderer.print_menu(game.menu.return_button_present(), game.renderer.font_for_game)
            game.renderer.print_information(game)
            return
        game.renderer.print_menu(game.menu.return_button_present())
        return


def handle_wait_inboard(game):
    if not game.highlight_piece:
        row, col = get_mouse_coordinate_in_board(game.board.rect_list,game.pos)

        if game.board.board_list[row][col] == 0:
            return
        if game.board.board_list[row][col].color != game.player:
            return
        game.highlight_piece = game.board.board_list[row][col]
        game.state = "animation"
        return
    if not game.board.rect_list[game.highlight_piece.position[0]][game.highlight_piece.position[1]].collidepoint(game.pos) :
            game.renderer.print_board(game.board.rect_list)
            game.renderer.draw_piece(game.board.board_list)
            game.renderer.print_menu(game.menu.return_button_present(), game.renderer.font_for_game)
            game.renderer.print_information(game)
            game.highlight_piece = None
            return 