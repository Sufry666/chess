import sys
import os
import pygame as pg
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
try:    
    import utils.helper as helper # type: ignore
    import config # type: ignore
    from core.board import Board # type: ignore
    from ui.renderer import renderer # type: ignore
except ImportError as e:
    print(f"{e}. Please check menu.py.")
class Button:
    def __init__(self, x = None, y = None, width = None , height = None):
        self.rect = pg.Rect(x, y, width, height)
        self.position = (x, y)
    def update_name(self, name):
        if name:
            self.name = name
        return
class menu:
    def __init__(self):
        self.rect = pg.Rect(config.MENU_COORDINATE[0], config.MENU_COORDINATE[1], config.MENU_WIDTH, config.MENU_HEIGHT)
        self.get_init_menu()
        self.state = "start"
    def get_init_menu(self):
        init_co = (config.MENU_COORDINATE[0] + 40, config.MENU_COORDINATE[1] + 40)
        self.init_button_list = [0 for _ in range(5)]
        for i in range(5):
            self.init_button_list[i] = Button(init_co[0], init_co[1] + i * 120, 320, 80)
        self.init_button_list[0].update_name("PVP")
        self.init_button_list[1].update_name("PVE")
        self.init_button_list[2].update_name("Collections")
        self.init_button_list[3].update_name("Setting")
        self.init_button_list[4].update_name("Exit")
    def get_gaming_menu(self):
        pass
    def return_button_present(self):
        if self.state == "start":
            return self.init_button_list
        elif self.state == "gaming":
            return self.init_button_list
def main():
    pg.init()
    renderer_test = renderer()
    board_test = Board()
    menu_test = menu()
    print(menu_test.rect)
    
    renderer_test.print_board(board_test.rect_list)
    pg.draw.rect(renderer_test.screen, config.BLACK, menu_test.rect)
    renderer_test.print_menu(menu_test.init_button_list)
    pg.display.flip()
    pg.time.wait(5000)
if __name__ == "__main__":
    main()