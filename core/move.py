import copy
class move:
    def __init__(self,vectors, piece): #vectors is a list of tuples representing the direction and distance of the move
        self.vectors = vectors
        self.piece = piece #pice is an instance of the piece class
    
    def move(self, board_present, final_position): #final_position为最终选取的移动位置
        o_r, o_c = self.piece.position  #棋子原先位置
        r, c = final_position   #移动后位置
        #创建新的棋盘实例 board_new






        if board_new[r][c] != 0:    #若该移动为吃子
            #如有需要，可在此处添加吃子细节，如加分等




            board_new[r][c] = 0 #在新棋盘上清除被吃棋子
        board_new[r][c] = self.piece    #在新棋盘移动后位置放置被移动棋子
        board_new[o_r][o_c] = 0 #在新棋盘上清除原先位置棋子
        return board_new
