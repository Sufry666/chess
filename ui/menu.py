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
    def __init__(self, x = None, y = None, width = None , height = None, isButton = True):
        self.isButton = isButton
        self.rect = pg.Rect(x, y, width, height)
    def update_name(self, name):
        if name:
            self.name = name
        return
    
    def update_rect(self, x, y, w, h):
        self.rect.x = x
        self.rect.y = y
        self.rect.width = w 
        self.rect.height = h


class menu:
    def __init__(self):
        self.rect = pg.Rect(config.MENU_COORDINATE[0], config.MENU_COORDINATE[1], config.MENU_WIDTH, config.MENU_HEIGHT)
        self.get_init_menu()
        self.state = "start"
        self.get_gaming_menu()
    
    def update_data(self, menu_coordinate, menu_width, menu_height):
        self.rect.x, self.rect.y = menu_coordinate
        self.rect.width = menu_width
        self.rect.height = menu_height
        temp = self.rect.width / 10
        temp_ = temp * 3 / 4
        for i in range(5):
            self.init_button_list[i].update_rect(self.rect.x + temp , self.rect.y + temp * 3 * i, temp * 8, temp * 2)
        for i in range(2):
            for j in range(3):
                self.gaming_button_list[3*i + j].update_rect(
                    self.rect.x + temp + i * (4 *temp + temp_), 
                    self.rect.y + temp * 9 + temp_ + j * 2 * temp_,
                    temp_ * 3 + temp,
                    temp 
                    )
        self.gaming_button_list[6].update_rect(self.rect.x + temp , self.rect.y , temp * 8, temp * 9)
        
    
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
        init_co = (config.MENU_COORDINATE[0] + 40, config.MENU_COORDINATE[1] + 40)
        game_information = Button(init_co[0], init_co[1], 320, 360, isButton= False)
        self.gaming_button_list = []
        for i in range(2):
            for j in range(3):
                button_temp = Button(init_co[0] + i * 190, init_co[1] + 390 + j * 60, 130, 40)
                self.gaming_button_list.append(button_temp)
        self.gaming_button_list.append(game_information)
        self.gaming_button_list[6].update_name("information")
        self.gaming_button_list[0].update_name("<")
        self.gaming_button_list[1].update_name("give up")
        self.gaming_button_list[2].update_name("propose a draw")
        self.gaming_button_list[3].update_name(">")
        self.gaming_button_list[4].update_name("retract")
        self.gaming_button_list[5].update_name("exit")
    
    

    
    def return_button_present(self):
        if self.state == "start":
            return self.init_button_list
        elif self.state == "gaming":
            return self.gaming_button_list
        #elif self.state == "retracting":
            return self.gaming_button_list
def main():
    pg.init()
    renderer_test = renderer()
    board_test = Board()
    menu_test = menu()
    print(menu_test.rect)
    
    renderer_test.print_board(board_test.rect_list)
    

    pg.display.flip()
    pg.time.wait(5000)
if __name__ == "__main__":
    main()