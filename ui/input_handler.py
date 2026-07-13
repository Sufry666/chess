import os
import sys
import pygame as pg
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
try:
    import config # type: ignore
    import core.board as board # type: ignore
    import utils.helper as helper # type: ignore
    from core.move import move #type: ignore
    import core.rules as rules #type: ignore
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
    try:
        row, col = get_mouse_coordinate_in_board(game.board.rect_list,game.pos)
    except TypeError:
        while get_mouse_coordinate_in_board(game.board.rect_list, game.pos):
            row, col = get_mouse_coordinate_in_board(game.board.rect_list, game.pos)
            break
    if game.state == "input_getting":
        if game.board.board_list[row][col] == 0:
            return
        if game.board.board_list[row][col].color != game.player:
            return
        game.state = "piece_selected"
        game.PieceToMove = game.board.board_list[row][col]
        
        game.PossibleVectors = game.PieceToMove.get_possible_moves(game.board.board_list)
        #game.renderer.show_possible_destination((row, col),game.PossibleVectors, game.board) #TODO
        game.renderer.render_handle(game,"show_possible_destination")
        game.VectorTodo = (row, col)
        
        return
    if game.state == "piece_selected":
        game.VectorTodo = (row - game.VectorTodo[0], col - game.VectorTodo[1])
        if game.VectorTodo not in game.PossibleVectors:
           
            game.state = "input_getting"
            game.state = "animation"
            game.animation_state = "highlight"
            return
        game.move_temp = move()
        
        if game.board.board_list[row][col] != 0: # 此情况为终点有子 必定为正常吃子
            game.move_temp.add_move(vector = game.VectorTodo, piece = game.PieceToMove, piece_captured = game.board.board_list[row][col])
        elif game.PieceToMove.name == "pawn" and game.VectorTodo[1] != 0: # 由于前一种情况为终点有子 故此处及后续情况均为终点无子 若被移动的棋子为pawn（此if的条件1）且移动方向不为竖直 即col坐标改变（此if的条件2） 说明该移动一定是吃过路兵
            game.move_temp.add_move(vector = game.VectorTodo, piece = game.PieceToMove, piece_captured = game.board.board_list[row - game.PieceToMove.direction][col])
            game.move_temp.isSpecialMove = True
        elif game.PieceToMove.name == "king" and abs(game.VectorTodo[1]) > 1: # 王车易位
            game.move_temp.add_move(vector = game.VectorTodo, piece = game.PieceToMove)
            game.move_temp.add_move(vector = (0, 3) if game.VectorTodo[1] == -2 else(0, -2), piece = game.board.board_list[game.PieceToMove.position[0]][0] if game.VectorTodo[1] == -2 else game.board.board_list[game.PieceToMove.position[0]][7])
        else: # 由于上述情况将 终点有子 与 终点无子且pawn斜着走 王车易位 讨论完毕 故此情况必定为终点无子的常规移动
            game.move_temp.add_move(vector = game.VectorTodo, piece = game.PieceToMove)
        if game.player == "black":
            game.player = "white"
        else:
            game.player = "black"
        for piece,_,_,_ in game.move_temp.moves:
            piece.moved_times += 1
        game.PieceToMove.is_moved_latest = True #移动后更新 最后移动的棋子 这一数据
        game.records.append(game.move_temp)
        #print(game.records) # 加入窗口显示
        if len(game.records) > 1:
            for piece,_,_,_ in game.records[-2].moves:
                piece.is_moved_latest = False # 移动前更新上一个被移动的棋子的 最后移动的棋子 这一数据
        
        game.PieceToMove = None
        game.state = "animation"
        game.animation_state = "move"
        return

def handle_click_inmenu(game):
    for button in game.menu.return_button_present():
        if not button.rect.collidepoint(game.pos):
            continue
        if button.name == "exit" and game.menu.state == "gaming":
            game.menu.state = "start"
            '''game.renderer.print_board(game.board.rect_list)
            game.renderer.print_menu(game.menu.return_button_present(),game.menu.state) #TODO'''
            game.renderer.render_handle(game)
            return
        if button.name == "retract":
            if len(game.records) == 0:
                return
            if game.player == "black":
                game.player = "white"
            else:
                game.player = "black"
            game.move_temp = game.records.pop()
            for piece,_,_,_ in game.move_temp.moves:
                piece.is_moved_latest = False # 悔棋前将回退步中移动的棋子的 最后移动的棋子 这一数据更新为False
                piece.moved_times -= 1
                
            if len(game.records) > 0:
                for piece,_,_,_ in game.records[-1].moves:
                    piece.is_moved_latest = True #悔棋后将此时的最后移动操作中被移动的棋子的 最后移动的棋子 这一数据更新为True
            game.move_temp.isRetract = True
            
            
            game.board.update(game.move_temp)
            
           
            game.state = "animation"
            game.animation_state = "move"
            return
        if button.name == "PVP":
            game.menu.state = "gaming"
            '''game.renderer.print_board(game.board.rect_list)
            game.renderer.draw_piece(game.board)
            game.renderer.print_menu(game.menu.return_button_present(), game.menu.state)'''
            game.renderer.render_handle(game)
            return
        if button.name == "Exit":
            game.running = False
            return
    
def handle_wait(game):
    '''if game.menu.state == "start":
        if not game.highlight_button:
            handle_wait_inmenu(game)
            return
        if not game.highlight_button.rect.collidepoint(game.pos):
            game.renderer.cover_highlight(game.highlight_button.rect)
            game.renderer.print_menu(game.menu.return_button_present(), game.menu.state)
            game.highlight_button = None
            return'''

    if game.menu.rect.collidepoint(game.pos):
        handle_wait_inmenu(game)
        return
    if game.PieceToMove and not game.board_rect.collidepoint(game.pos):
        if game.state != "piece_selected":
                
            '''game.renderer.print_board(game.board.rect_list)
            game.renderer.draw_piece(game.board)
            game.renderer.print_menu(game.menu.return_button_present(), game.menu.state)
            game.renderer.print_information(game)'''
            game.renderer.render_handle(game)
            game.PieceToMove = None
        else:
            pass
    '''if game.menu.rect.collidepoint(game.pos):
            
        if not game.highlight_button:
            handle_wait_inmenu(game)
            return
        if not game.highlight_button.rect.collidepoint(game.pos) :
            game.renderer.cover_highlight(game.highlight_button.rect)
            game.renderer.print_menu(game.menu.return_button_present(), game.menu.state)
            game.renderer.print_information(game)
            game.renderer.render_handle(game)
            game.highlight_button = None
            return'''
    if game.board_rect.collidepoint(game.pos):
        if game.state == "piece_selected":
            return
            
        handle_wait_inboard(game)
        return

def handle_wait_inmenu(game):
    if game.highlight_button and not game.highlight_button.rect.collidepoint(game.pos):
        game.renderer.render_handle(game)
        game.highlight_button = None
        return
    for button in game.menu.return_button_present():
        
        if not button.rect.collidepoint(game.pos):
            continue
        #if button.name == "information":
            continue

        if game.state == "piece_selected":
            game.state = "animation"
            game.animaiton_state = "highlight"
        game.highlight_button = button
        '''game.renderer.show_button_highlight(button)
        

       
        
        if game.menu.state == "gaming":
            
            game.renderer.print_menu(game.menu.return_button_present(), game.menu.state)
            game.renderer.print_information(game)
            return
        game.renderer.print_menu(game.menu.return_button_present(), game.menu.state)'''
        game.renderer.render_handle(game, state = "highlight_button")
        return


def handle_wait_inboard(game):

    if not game.PieceToMove:
        if not get_mouse_coordinate_in_board(game.board.rect_list, game.pos):
            return
        row, col = get_mouse_coordinate_in_board(game.board.rect_list,game.pos)

        if game.board.board_list[row][col] == 0:
            return
        if game.board.board_list[row][col].color != game.player:
            return
        game.PieceToMove = game.board.board_list[row][col]
        game.state = "animation"
        game.animation_state = "highlight"
        return
    if not game.board.rect_list[game.PieceToMove.position[0]][game.PieceToMove.position[1]].collidepoint(game.pos) :
            '''game.renderer.print_board(game.board.rect_list)
            game.renderer.draw_piece(game.board)
            game.renderer.print_menu(game.menu.return_button_present(), game.menu.state)
            game.renderer.print_information(game)'''
            game.renderer.render_handle(game)
            game.PieceToMove = None
            return 
    

'''def handle_chessmate(game, state):
    if state == "unchessmated" and rules.isChessmate(game.board.board_list, game.king_white.position):
        game.king_white.chessmated_image_handle()
        game.state = "animation"
        game.animation_state = "highlight"
        game.PieceToMove = game.king_white
        game.king_state = "white_chessmated"
        return state
    if state == "unchessmated" and rules.isChessmate(game.board.board_list, game.king_black.position):
        game.king_black.chessmated_image_handle()
        game.state = "animation"
        game.animation_state = "highlight"
        game.PieceToMove = game.king_black
        game.king_state = "black_chessmated"
        return state
    if state == "white_chessmated" and not rules.isChessmate(game.board.board_list, game.king_white.position):
        game.king_white.chessmated_image_handle()
        game.king_state = "unchessmated"
        return state
    if state == "black_chessmated" and not rules.isChessmate(game.board.board_list, game.king_black.position):
        game.king_black.chessmated_image_handle()
        game.king_state = "unchessmated"
        return state
    return state'''