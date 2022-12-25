import pygame, sys
import random 
from pygame import mixer
from pygame.locals import *
from math import inf, sqrt, log
from copy import deepcopy

class Node:
    """
    # Node
    The Node class defines a node in a
    Monte-Carlo Search Tree, with all
    requisite parameters.
    """
    def __init__(self, board, aimove, move):
        self.wins = 0.0
        self.games = 0.0
        self.move = move
        self.board = board
        self.player_id = aimove
        self.children = []


class Board:
    def __init__(self):
        self.player = 1
        self.player2 = -1
        self.markers=[]
        for i in range (3):
            row = [0]*3
            self.markers.append(row)
        self.winner = 0
        self.game_over = False
    def check_game_over(self):
        x_pos = 0
        for x in self.markers:
            if sum(x) == 3:
                self.winner = 1
                self.game_over = True
            if sum(x) == -3:
                self.winner = 2
                self.game_over = True
            if self.markers[0][x_pos] + self.markers [1][x_pos] + self.markers [2][x_pos] == 3:
                self.winner = 1
                self.game_over = True
            if self.markers[0][x_pos] + self.markers [1][x_pos] + self.markers [2][x_pos] == -3:
                self.winner = 2
                self.game_over = True
            x_pos += 1
        if self.markers[0][0] + self.markers[1][1] + self.markers [2][2] == 3 or self.markers[2][0] + self.markers[1][1] + self.markers [0][2] == 3:
            self.winner = 1
            self.game_over = True
        if self.markers[0][0] + self.markers[1][1] + self.markers [2][2] == -3 or self.markers[2][0] + self.markers[1][1] + self.markers [0][2] == -3:
            self.winner = 2
            self.game_over = True
        if self.game_over == False:
            tie = True
            for row in self.markers:
                for i in row:
                    if i == 0:
                        tie = False
            if tie == True:
                self.game_over = True
                self.winner = 0
    def is_move_left(self):
        for i in range(3):
            for j in range (3):
                if self.markers[i][j] == 0:
                    return True
        return False
    def all_possible_move(self):
        for i in range (3):
            for j in range (3):
                if self.markers[i][j] !=0:
                    return False
        return True

class AI(Board):
    def __init__(self):
        super().__init__()    
    def random_move(self, aimove):
        x_pos = random.randint(0,2)
        y_pos = random.randint(0,2)
        while (self.markers[x_pos][y_pos]!=0):
            x_pos = random.randint(0,2)
            y_pos = random.randint(0,2)
        self.markers[x_pos][y_pos]=aimove
    def evaluate(self, aimove):
        x_pos = 0
        for x in self.markers:
            if sum(x) == -3*aimove:
                return -10
            if sum(x) == 3*aimove:
                return 10
            if self.markers[0][x_pos] + self.markers[1][x_pos] + self.markers[2][x_pos] == -3*aimove:
                return -10
            if self.markers[0][x_pos] + self.markers[1][x_pos] + self.markers[2][x_pos] == 3*aimove:
                return 10
            x_pos += 1
        if self.markers[0][0] + self.markers[1][1] + self.markers[2][2] == -3*aimove or self.markers[2][0] + self.markers[1][1] + self.markers [0][2] == -3*aimove:
            return -10
        if self.markers[0][0] + self.markers[1][1] + self.markers[2][2] == 3*aimove or self.markers[2][0] + self.markers[1][1] + self.markers [0][2] == 3*aimove:
            return 10
        return 0
    def minimax(self, depth, isMaximizing, alpha, beta, aimove):
        result = self.evaluate(aimove)
        if (result != 0):
            return result
        if (self.is_move_left()==False):
            return 0
        if(isMaximizing):
            bestScore = -inf
            for i in range(3):
                for j in range(3):
                    if (self.markers[i][j] == 0):
                        self.markers[i][j] = aimove
                        score = self.minimax(depth+1, False, alpha, beta, aimove)
                        self.markers[i][j] = 0
                        bestScore = max(score, bestScore)
                        alpha = max (bestScore, alpha)
                        if alpha >= beta:
                            break
            return bestScore
        else:
            bestScore = inf
            for i in range(3):
                for j in range(3):
                    if (self.markers[i][j] == 0):
                        self.markers[i][j] = -aimove
                        score = self.minimax(depth-1, True, alpha, beta, aimove)
                        self.markers[i][j] = 0
                        bestScore = min(score, bestScore)
                        beta = min(bestScore, beta)
                        if beta <= alpha:
                            break
            return bestScore
    def minimax_move(self, aimove):
        if (self.all_possible_move()):
            self.random_move(aimove)
            return 
        else:
            bestScore = -inf
            for i in range(3):
                for j in range(3):
                    if (self.markers[i][j] == 0):
                        self.markers[i][j] = aimove
                        score = self.minimax(3, False, -inf, inf,aimove)
                        self.markers[i][j] = 0
                        if (score > bestScore):
                            bestScore = score
                            x_pos = i
                            y_pos = j
            self.markers[x_pos][y_pos] = aimove

    #Negamax
    # def negamax2(self, depth, aimove): 


    def negamax(self, depth, alpha, beta, aimove): 
        result = self.evaluate(aimove)
        if (result != 0):
            return result
        if (self.is_move_left()==False):
            return 0
        
        bestScore = -inf
        for i in range(3):
            for j in range(3):
                if (self.markers[i][j] == 0): 
                    self.markers[i][j] = aimove
                    # aimove = -aimove
                    score = -self.negamax(depth - 1, -beta,  -alpha, -aimove)
                    self.markers[i][j] = 0
                    aimove = -aimove  
                    bestScore = max(bestScore, score)
                    alpha = max(alpha, score)
                    if alpha >= beta:
                        break
        return bestScore 
    def negamax_move(self, aimove):
        if(self.all_possible_move()):
            self.random_move(aimove)
            return
        else:
            bestScore = -inf
            for i in range(3):
                for j in range(3):
                    if (self.markers[i][j] == 0):
                        self.markers[i][j] = aimove
                        score = self.negamax(0, -inf, inf, aimove)
                        self.markers[i][j] = 0
                        if (score > bestScore):
                            bestScore = score
                            x_pos = i
                            y_pos = j
            self.markers[x_pos][y_pos] = aimove


class Game(AI):
    def __init__(self):
        super().__init__()
        pygame.init()
        self.screen_width, self.screen_height = 600, 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Tic Tac Toe! GET GO")
        linkBackGround = './img/background.jpg'
        self.backGround = pygame.image.load(linkBackGround)
        icon = pygame.image.load('./img/icon.jpg')
        self.icon = pygame.display.set_icon(icon)
        self.grid = (240,255,240)
        self.line_width = 6
        self.gamerunning = True
        self.green = (0,255,0)
        self.red = (255,0,0)
        self.blue = (0, 0, 255)
        self.clicked = False
        self.pos = (0,0)
        self.music('./sound/blackpink.mp3')
        self.font = pygame.font.SysFont('bitstreamverasans',35, bold=False, italic=False)
        self.again_rect = Rect(self.screen_width//2-80,self.screen_height//2,160,50)
        self.check_turn = None
        self.mode1_rect = Rect(self.screen_width//2-180,self.screen_height//2-75,360,50)
        self.mode2_rect = Rect(self.screen_width//2-180,self.screen_height//2+25,360,50)
        self.select_turn1_rect = Rect(self.screen_width//2-180,self.screen_height//2-75,360,50)
        self.select_turn2_rect = Rect(self.screen_width//2-180,self.screen_height//2+25,360,50)
        self.mode = None
        self.human = None
        self.ai = None
        self.algorithm1_rect = Rect(self.screen_width//2-180,self.screen_height//3-50,360,50)
        self.algorithm2_rect = Rect(self.screen_width//2-180,self.screen_height//2-25,360,50)
        self.algorithm3_rect = Rect(self.screen_width//2-180,self.screen_height*2//3,360,50)
        self.algorithm = None
    def music(self, url):
        Sound = mixer.Sound(url)
        #Sound.play()
        Sound.set_volume(0.7)
    def create_background(self):
        self.screen.blit(self.backGround, (0,0))
        for x in range (1,3):
            pygame.draw.line(self.screen, self.grid, (0, x*200), (self.screen_width, x*200), self.line_width)
            pygame.draw.line(self.screen, self.grid, (x*200,0), (x*200,self.screen_height), self.line_width)
    def draw_markers(self):
        x_pos = 0
        for x in self.markers:
            y_pos = 0
            for y in x:
                if y == 1:
                    pygame.draw.line(self.screen, self.red, (x_pos * 200 + 30, y_pos * 200 + 30), (x_pos * 200 + 170, y_pos * 200 + 170), self.line_width)
                    pygame.draw.line(self.screen, self.red, (x_pos * 200 + 170, y_pos * 200 + 30), (x_pos * 200 + 30, y_pos * 200 + 170), self.line_width)
                if y == -1:
                    pygame.draw.circle(self.screen, self.green, (x_pos * 200 + 100, y_pos * 200 + 100), 80, self.line_width)
                y_pos += 1
            x_pos += 1	
    def draw_mode(self):
        mode1_img = self.font.render("Human vs Human", True, self.blue)
        rect1_obj = pygame.draw.rect(self.screen,self.green, self.mode1_rect)
        mode1_box = mode1_img.get_rect(center=rect1_obj.center)
        self.screen.blit(mode1_img, mode1_box)

        mode2_img = self.font.render("Human vs Computer", True, self.blue)
        rect2_obj = pygame.draw.rect(self.screen,self.green, self.mode2_rect)
        mode2_box = mode1_img.get_rect(center=rect2_obj.center)
        self.screen.blit(mode2_img, mode2_box)
    def draw_turn(self):
        turn1_img = self.font.render("Human first", True, self.blue)
        turn1_obj = pygame.draw.rect(self.screen,self.green, self.select_turn1_rect)
        turn1_box = turn1_img.get_rect(center=turn1_obj.center)
        self.screen.blit(turn1_img, turn1_box)

        turn2_img = self.font.render("Computer first", True, self.blue)
        turn2_obj = pygame.draw.rect(self.screen,self.green, self.select_turn2_rect)
        turn2_box = turn2_img.get_rect(center=turn2_obj.center)
        self.screen.blit(turn2_img, turn2_box)
    def draw_algorithm(self):
        algorithm1_img = self.font.render("Random Move", True, self.blue)
        algorithm1_obj = pygame.draw.rect(self.screen,self.green, self.algorithm1_rect)
        algorithm1_box = algorithm1_img.get_rect(center=algorithm1_obj.center)
        self.screen.blit(algorithm1_img, algorithm1_box)

        algorithm2_img = self.font.render("Minimax (ab prunning)", True, self.blue)
        algorithm2_obj = pygame.draw.rect(self.screen,self.green, self.algorithm2_rect)
        algorithm2_box = algorithm2_img.get_rect(center=algorithm2_obj.center)
        self.screen.blit(algorithm2_img, algorithm2_box)

        algorithm3_img = self.font.render("Negamax (ab prunning)", True, self.blue)
        algorithm3_obj = pygame.draw.rect(self.screen,self.green, self.algorithm3_rect)
        algorithm3_box = algorithm3_img.get_rect(center=algorithm3_obj.center)
        self.screen.blit(algorithm3_img, algorithm3_box)
    def draw_game_over(self):
        if self.winner != 0:
            end_text = "Player " + str(self.winner) + " wins!"
        elif self.winner == 0:
            end_text = "You have tied!"

        end_img = self.font.render(end_text, True, self.blue)
        rect_obj = pygame.draw.rect(self.screen, self.green, (self.screen_width // 2 - 100, self.screen_height // 2 - 60, 200, 50))
        end_box = end_img.get_rect(center=rect_obj.center)
        self.screen.blit(end_img,end_box)

        again_text = 'Play Again?'
        again_img = self.font.render(again_text, True, self.blue)
        rect_obj = pygame.draw.rect(self.screen, self.green, self.again_rect)
        again_box = again_img.get_rect(center=rect_obj.center)
        self.screen.blit(again_img, again_box)
    def run(self):
        while self.gamerunning:
            self.create_background()
            self.draw_markers()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.gamerunning = False
            if self.mode is None:
                self.draw_mode()
                if event.type == pygame.MOUSEBUTTONDOWN and self.clicked == False:
                    self.clicked = True
                if event.type == pygame.MOUSEBUTTONUP and self.clicked == True:
                    self.clicked = False
                    self.pos = pygame.mouse.get_pos()
                    if self.mode1_rect.collidepoint(self.pos):
                        self.mode = 1
                    elif self.mode2_rect.collidepoint(self.pos):
                        self.mode = 2
            else:
                if self.mode == 1:
                    if self.game_over == False:
                        if event.type == pygame.MOUSEBUTTONDOWN and self.clicked == False:
                            self.clicked = True
                        if event.type == pygame.MOUSEBUTTONUP and self.clicked == True:
                            self.clicked = False
                            self.pos = pygame.mouse.get_pos()
                            cell_x = self.pos[0]//200
                            cell_y = self.pos[1]//200
                            if self.markers[cell_x][cell_y] == 0:
                                self.markers[cell_x][cell_y] = self.player
                                self.check_game_over()
                                self.player *=-1
                    if self.game_over == True:
                        self.draw_game_over()
                        if event.type == pygame.MOUSEBUTTONDOWN and self.clicked == False:
                            self.clicked = True
                        if event.type == pygame.MOUSEBUTTONUP and self.clicked == True:
                            self.clicked = False
                            self.pos = pygame.mouse.get_pos()
                            if self.again_rect.collidepoint(self.pos):
                                self.game_over = False
                                self.player = 1
                                self.pos = (0,0)
                                self.markers = []
                                self.winner = 0
                                for i in range (3):
                                    row = [0]*3
                                    self.markers.append(row)
                                self.mode = None 
                elif self.mode ==2:
                    if self.check_turn is None:
                        self.draw_turn()
                        if event.type == pygame.MOUSEBUTTONDOWN and self.clicked == False:
                            self.clicked = True
                        if event.type == pygame.MOUSEBUTTONUP and self.clicked == True:
                            self.clicked = False
                            self.pos = pygame.mouse.get_pos()
                            if self.select_turn1_rect.collidepoint(self.pos):
                                self.human = self.player
                                self.ai = self.player2
                                self.check_turn = True
                            elif self.select_turn2_rect.collidepoint(self.pos):
                                self.human = self.player2
                                self.ai = self.player
                                self.check_turn = False
                    else:
                        if self.algorithm == None:
                            self.draw_algorithm()
                            if event.type == pygame.MOUSEBUTTONDOWN and self.clicked == False:
                                self.clicked = True
                            if event.type == pygame.MOUSEBUTTONUP and self.clicked == True:
                                self.clicked = False
                                self.pos = pygame.mouse.get_pos()
                                if self.algorithm1_rect.collidepoint(self.pos):
                                    self.algorithm = 1
                                elif self.algorithm2_rect.collidepoint(self.pos):
                                    self.algorithm = 2
                                elif self.algorithm3_rect.collidepoint(self.pos):
                                    self.algorithm = 3
                        else:  
                            if self.game_over == False:
                                if self.check_turn:
                                    if event.type == pygame.MOUSEBUTTONDOWN and self.clicked == False:
                                        self.clicked = True
                                    if event.type == pygame.MOUSEBUTTONUP and self.clicked == True:
                                        self.clicked = False
                                        self.pos = pygame.mouse.get_pos()
                                        cell_x = self.pos[0]//200
                                        cell_y = self.pos[1]//200
                                        if self.markers[cell_x][cell_y] == 0:
                                            self.markers[cell_x][cell_y] = self.human
                                            self.check_turn=False
                                            self.check_game_over()
                                else:
                                    if self.algorithm == 1:
                                        self.random_move(self.ai)
                                    elif self.algorithm ==2:
                                        self.minimax_move(self.ai)
                                    elif self.algorithm ==3:
                                        self.negamax_move(self.ai)
                                    self.check_turn = True
                                    self.check_game_over()
                            if self.game_over == True:
                                self.draw_game_over()
                                if event.type == pygame.MOUSEBUTTONDOWN and self.clicked == False:
                                    self.clicked = True
                                if event.type == pygame.MOUSEBUTTONUP and self.clicked == True:
                                    self.clicked = False
                                    self.pos = pygame.mouse.get_pos()
                                    if self.again_rect.collidepoint(self.pos):
                                        self.game_over = False
                                        self.player = 1
                                        self.pos = (0,0)
                                        self.markers = []
                                        self.winner = 0
                                        self.check_turn=None
                                        for i in range (3):
                                            row = [0]*3
                                            self.markers.append(row)
                                        self.mode = None 
                                        self.algorithm = None
            pygame.display.flip()
        pygame.quit()

if __name__ == '__main__':
    pyGame = Game()
    pyGame.run()