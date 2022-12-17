import pygame, sys
import random 
from pygame import mixer
from pygame.locals import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen_width, self.screen_height = 600, 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Tic Tac Toe! GET GO")
        linkBackGround = './img/background.jpg'
        self.backGround = pygame.image.load(linkBackGround)
        icon = pygame.image.load('./img/icon.jpg')
        self.icon = pygame.display.set_icon(icon)
        self.grid = (240,255,240)
        self.line_width = 5
        self.gamerunning = True
        self.green = (0,255,0)
        self.red = (255,0,0)
        self.blue = (0, 0, 255)
        self.clicked = False
        self.markers=[]
        for i in range (5):
            row = [0]*5
            self.markers.append(row)
        self.player = 1
        self.pos = (0,0)
        self.music('./sound/blackpink.mp3')
        self.font = pygame.font.SysFont(None,40)
        self.again_rect = Rect(self.screen_width//2-80,self.screen_height//2,160,50)
        self.winner = 0
        self.game_over = False
        self.check_turn = True
    def music(self, url):
        Sound = mixer.Sound(url)
        Sound.play()
        Sound.set_volume(0.7)
    def create_background(self):
        self.screen.blit(self.backGround, (0,0))
        for x in range (1,5):
            pygame.draw.line(self.screen, self.grid, (0, x*120), (self.screen_width, x*120), self.line_width)
            pygame.draw.line(self.screen, self.grid, (x*120,0), (x*120,self.screen_height), self.line_width)
    def draw_markers(self):
        x_pos = 0
        for x in self.markers:
            y_pos = 0
            for y in x:
                if y == 1:
                    pygame.draw.line(self.screen, self.red, (x_pos * 120 + 18, y_pos * 120 + 18), (x_pos * 120 + 102, y_pos * 120 + 102), self.line_width)
                    pygame.draw.line(self.screen, self.red, (x_pos * 120 + 102, y_pos * 120 + 18), (x_pos * 120 + 18, y_pos * 120 + 102), self.line_width)
                if y == -1:
                    pygame.draw.circle(self.screen, self.green, (x_pos * 120 + 60, y_pos * 120 + 60), 38, self.line_width)
                y_pos += 1
            x_pos += 1	
    def check_game_over(self):
        x_pos = 0
        for x in self.markers:
            if sum(x) == 5:
                self.winner = 1
                self.game_over = True
            if sum(x) == -5:
                self.winner = 2
                self.game_over = True
            if self.markers[0][x_pos] + self.markers [1][x_pos] + self.markers [2][x_pos] + self.markers[3][x_pos] + self.markers[4][x_pos] == 5:
                self.winner = 1
                self.game_over = True
            if self.markers[0][x_pos] + self.markers [1][x_pos] + self.markers [2][x_pos] + self.markers[3][x_pos] + self.markers[4][x_pos] == -5:
                self.winner = 2
                self.game_over = True
            x_pos += 1
        if self.markers[0][0] + self.markers[1][1] + self.markers [2][2] + self.markers[3][3] + self.markers[4][4] == 5 or self.markers[4][0] + self.markers[3][1] + self.markers[2][2] +self.markers[1][3] +self.markers[0][4]  == 5:
            self.winner = 1
            self.game_over = True
        if self.markers[0][0] + self.markers[1][1] + self.markers [2][2] + self.markers[3][3] + self.markers[4][4] == -5 or self.markers[4][0] + self.markers[3][1] + self.markers[2][2] +self.markers[1][3] +self.markers[0][4]  == -5:
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
    def draw_game_over(self):
        if self.winner != 0:
            end_text = "Player " + str(self.winner) + " wins!"
        elif self.winner == 0:
            end_text = "You have tied!"

        end_img = self.font.render(end_text, True, self.blue)
        pygame.draw.rect(self.screen, self.green, (self.screen_width // 2 - 100, self.screen_height // 2 - 60, 200, 50))
        self.screen.blit(end_img,(self.screen_width // 2 - 100, self.screen_height // 2 - 50))

        again_text = 'Play Again?'
        again_img = self.font.render(again_text, True, self.blue)
        pygame.draw.rect(self.screen, self.green, self.again_rect)
        self.screen.blit(again_img, (self.screen_width // 2 - 80, self.screen_height // 2 + 10))
    def random_move(self):
        x_pos = random.randint(0,4)
        y_pos = random.randint(0,4)
        while (self.markers[x_pos][y_pos]!=0):
            x_pos = random.randint(0,4)
            y_pos = random.randint(0,4)
        self.markers[x_pos][y_pos]=-1
        self.check_turn = True
    def run(self):
        print(self.markers)
        while self.gamerunning:
            self.create_background()
            self.draw_markers()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.gamerunning = False
                if self.game_over == False:
                    if self.check_turn:
                        if event.type == pygame.MOUSEBUTTONDOWN and self.clicked == False:
                            self.clicked = True
                        if event.type == pygame.MOUSEBUTTONUP and self.clicked == True:
                            self.clicked = False
                            self.pos = pygame.mouse.get_pos()
                            cell_x = self.pos[0]//120
                            cell_y = self.pos[1]//120
                            if self.markers[cell_x][cell_y] == 0:
                                self.markers[cell_x][cell_y] = self.player
                                self.check_turn=False
                                self.check_game_over()
                                # self.player *= -1
                    else:
                        self.random_move()
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
                        for i in range (5):
                            row = [0]*5
                            self.markers.append(row)
            pygame.display.update()
        pygame.quit()

if __name__ == '__main__':
    pyGame = Game()
    pyGame.run()
