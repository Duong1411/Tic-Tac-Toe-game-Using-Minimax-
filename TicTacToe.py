import random
import sys
import pygame
import numpy as np
import copy
pygame.init()
screen = pygame.display.set_mode((600,600))
#setup
pygame.display.set_caption("TIC_TAC_TOE")
#Tham so dung trong bai
#Tham số này dùng để setting trò chơi
#Vẽ trò chơi hiểu đơn giản là vậy
WHITE = (255,255,255) #Chỉ số màu trắng trong bảng màu RGB
BG = (35,230,119) #Bảng màu Xanh cỏ làm nền trong RGB
COT = 3 #Chỉ số Hàng
HANG = 3 #Chỉ số cột
SQSIZE = 600 // HANG #Chiều dài của 1 ô
LINE_W = 10 #Độ dày của 1 line
CTRC_W = 10 #Độ dày của line hình tròn O
CROSS_W= 10 #Độ dày của line line cho X
R = SQSIZE // 4 #Bán kính hình tròn
OFFSET = 50 #Chỉ số OFFSET
MAU_DK = (255,255,255) #Màu Trắng
CYCLE = (139,0,0) #Màu đỏ
CROSS = (0,0,139) #Màu Xanh
screen.fill(BG)
class BOARD:
    def __init__(self):
        self.squares = np.zeros((COT,HANG))
        self.empty_sqrs = self.squares
        self.marked_sqrs = 0
    def final_state(self, show=False):
        #chả về 0 nếu ko thắng (hòa)
        #Nếu player 1 thắng trả về 1
        #Nếu player 2 thắng trả về 2

        #Hàng ăn 3
        for col in range(HANG):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                if show:
                    color = CYCLE if self.squares[0][col] == 2 else CROSS
                    iPos = (col * SQSIZE + SQSIZE // 2, 15)
                    fPos = (col * SQSIZE + SQSIZE // 2, 600 - 15)
                    pygame.draw.line(screen, color, iPos, fPos, LINE_W)
                return self.squares[0][col]
        #Cột ăn 3
        for row in range(COT):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                if show:
                    color = CYCLE if self.squares[row][0] == 2 else CROSS
                    iPos = (15, row * SQSIZE + SQSIZE // 2)
                    fPos = (600 - 15, row * SQSIZE + SQSIZE // 2)
                    pygame.draw.line(screen, color, iPos, fPos, LINE_W)
                return self.squares[0][row]
        #Chéo ăn 3 trái
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            if show:
                color = CYCLE if self.squares[1][1] == 2 else CROSS
                iPos = (15, 15)
                fPos = (600 - 15, 600 - 15)
                pygame.draw.line(screen, color, iPos, fPos, LINE_W)
            return self.squares[1][1]
        #Chéo phải ăn 3
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            if show:
                color = CYCLE if self.squares[1][1] == 2 else CROSS
                iPos = (15, 600 - 15)
                fPos = (600 - 15, 15)
                pygame.draw.line(screen, color, iPos, fPos, LINE_W)
            return self.squares[1][1]
        #ko ai thắng
        return 0


    def mark_spr(self, row, col, player):
        self.squares[row][col] = player
        self.marked_sqrs +=1
    def empty_sqr(self, row, col):
        return self.squares[row][col] == 0

    def get_empty_sqrs(self):
        empty_sqrs = []
        for row in range(COT):
            for col in range(HANG):
                if self.empty_sqr(row,col):
                    empty_sqrs.append((row,col))
        return  empty_sqrs

    def isfull(self):
        return self.marked_sqrs == 9

    def isempty(self):
        return self.marked_sqrs == 0

class AI:
    def __init__(self, level=1, player=2):
        self.level = level
        self.player = player

    def rnd(self, board):
        empty_sqrs = board.get_empty_sqrs()
        idx = random.randrange(0, len(empty_sqrs))
        return empty_sqrs[idx]
    def minimax(self, board, maximizing):
        #terminal case
        case = board.final_state()

        #player 1 thắng
        if case == 1:
            return 1, None #eval, Move
        #player 2 thắng (AI)
        if case == 2:
            return -1, None
        elif board.isfull():
            return 0, None
        if maximizing:
            max_eval = -100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_spr(row, col, 1)
                eval = self.minimax(temp_board, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)
            return max_eval, best_move
        elif not maximizing:
            min_eval = 100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_spr(row, col, self.player)
                eval = self.minimax(temp_board, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)
            return min_eval, best_move
    def eval(self, main_board):
        if self.level == 0:
            #random choice
            eval = 'random'
            move = self.rnd(main_board)
        else:
            #minimax choice
            eval, move = self.minimax(main_board, False)
        print(f"AI HAS CHOSEN TO MARK THE SQUARE IN POS {move} with an eval of: {eval} ")
        return move
class GAME:

    def __init__(self):
        self.board = BOARD()
        self.ai = AI()
        self.player = 1
        self.gamemode = "ai"
        self.running = True
        self.show_lines()
    def make_move(self, row, col):
        self.board.mark_spr(row, col, self.player)
        self.draw_fig(row, col)
        self.next_turn()
    def show_lines(self):
        screen.fill(BG)
        #khung caro
        pygame.draw.line(screen, MAU_DK, (SQSIZE,0), (SQSIZE,600), LINE_W)
        pygame.draw.line(screen, MAU_DK, (600- SQSIZE, 0), (600 - SQSIZE, 600), LINE_W)
        pygame.draw.line(screen, MAU_DK, (0, SQSIZE), (600, SQSIZE), LINE_W)
        pygame.draw.line(screen, MAU_DK, (0, 600 - SQSIZE), (600, 600 - SQSIZE), LINE_W)
    def draw_fig(self, row, col):
        if self.player == 1:
            #VE DUONG CUA X
            start_desc = (col * SQSIZE + OFFSET, row * SQSIZE + OFFSET)
            end_desc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE +SQSIZE - OFFSET)
            pygame.draw.line(screen, CROSS, start_desc, end_desc, CROSS_W)
            #VE DUONG CUA X
            start_asc = (col * SQSIZE + OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            end_asc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + OFFSET)
            pygame.draw.line(screen, CROSS, start_asc, end_asc, CROSS_W)
        elif self.player == 2:
            center = (col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE //2)
            pygame.draw.circle(screen, CYCLE, center, R, CTRC_W)
    def next_turn(self):
        self.player = self.player % 2 + 1

    def change_gm(self):
        if self.gamemode == "pvp":
            self.gamemode = "ai"
        else:
            self.gamemode = "pvp"
    def restart(self):
        self.__init__()

    def isover(self):
        return self.board.final_state(show=True) != 0 or self.board.isfull()
def main():

    game = GAME()
    board = game.board
    ai = game.ai

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


            if event.type == pygame.KEYDOWN:

                #g-gamemode
                if event.key == pygame.K_g:
                    game.change_gm()

                if event.key == pygame.K_r:
                    game.restart()
                    board = game.board
                    ai = game.ai
                #0- ramdom AI
                if event.key == pygame.K_0:
                    ai.level = 0
                #1- Minimax AI
                if event.key == pygame.K_1:
                    ai.level = 1

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] // SQSIZE
                col = pos[0] // SQSIZE

                if board.empty_sqr(row, col) and game.running:
                    game.make_move(row, col)
                    if game.isover():
                        game.running=False

        if game.gamemode == 'ai' and game.player == ai.player and game.running:
            pygame.display.update()

            row, col = ai.eval(board)

            game.make_move(row, col)
            if game.isover():
                game.running = False

        pygame.display.update()
main()

