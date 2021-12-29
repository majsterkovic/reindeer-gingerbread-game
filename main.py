import random

import sys

from astar import astar

import pygame

pygame.init()

SCREEN_HEIGHT = 768
SCREEN_WIDTH = 768
IMG_SIZE = 64

###############
TO_WIN = 10
ENEMY_SPEED = 3
###############

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Reniferek Hesjan')
Icon = pygame.image.load('img/christmas-reindeer.png')
pygame.display.set_icon(Icon)


kinder = pygame.image.load("img/kinder.png")

maze = [ [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1],
            [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1],
            [1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
            [1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1],
            [1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

kinderki = False
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)


class Reindeer:
    def __init__(self, Y, X, Img):
        self.X = X
        self.Y = Y
        self.Img = Img

    def draw(self):
        screen.blit(self.Img, (self.X, self.Y))

    last_move = 0

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]: #1
            if maze[self.Y // 64][(self.X - IMG_SIZE) // 64] != 1:
                self.X -= IMG_SIZE
                if self.last_move != 1:
                    self.Img = pygame.transform.flip(self.Img, True, False)
                    self.last_move = 1
                return
        if keys[pygame.K_RIGHT]: #0
            if maze[self.Y // 64][(self.X + IMG_SIZE) // 64] != 1:
                self.X += IMG_SIZE
                if self.last_move != 0:
                    self.Img = pygame.transform.flip(self.Img, True, False)
                    self.last_move = 0
                return
        if keys[pygame.K_UP]:
            if maze[(self.Y - IMG_SIZE) // 64][self.X // 64] != 1:
                self.Y -= IMG_SIZE
                return
        if keys[pygame.K_DOWN]:
            if maze[(self.Y + IMG_SIZE) // 64][self.X // 64] != 1:
                self.Y += IMG_SIZE
                return

class Gingerbread:
    def __init__(self, Y, X, Img):
        self.X = X
        self.Y = Y
        self.Img = Img

    def draw(self):
        screen.blit(self.Img, (self.X, self.Y))

    def new_position(self, reindeer_position):
            while True:
                x = random.randint(1, 10)
                y = random.randint(1, 10)
                if maze[y][x] == 0 and (y, x) != reindeer_position and len(astar(maze, (reindeer_position[0], reindeer_position[1]), (y, x))) > 3:
                    self.X = x * 64
                    self.Y = y * 64
                    break
    def found(self, reindeer_position):
        if self.X == reindeer_position[1] and self.Y == reindeer_position[0]:
            return True
            
        return False

class Score:
    def __init__(self):
        self.score = 0
        self.score_text = ' Wynik: ' + str(self.score)
        self.textsurface = myfont.render(self.score_text, True, (255, 255, 255))
    def increment(self):
        self.score += 1
        self.score_text = ' Wynik: ' + str(self.score)
        self.textsurface = myfont.render(self.score_text, True, (255, 255, 255))
    def print(self):
        if not kinderki:
            screen.blit(self.textsurface, (0,5))
        else:
            for k in range(self.score):
                screen.blit(kinder, (64 * (k + 1) + (64 - kinder.get_width()) // 2, 0))

class Time_counter:
    def __init__(self, start_time):
        self.start_time = start_time
        self.time_since_enter = pygame.time.get_ticks() - self.start_time
        self.message = ' Czas: ' + str(round((self.time_since_enter / 1000), 2))

    def print(self):
        self.time_since_enter = pygame.time.get_ticks() - self.start_time
        self.message = ' Czas: ' + str(round((self.time_since_enter / 1000), 2))
        screen.blit(myfont.render(self.message, True, (255,255,255)), (0, SCREEN_HEIGHT - 64+5))

class Enemy:
    def __init__(self, Y, X, Img):
        self.X = X
        self.Y = Y
        self.Img = Img

    def draw(self):
        screen.blit(self.Img, (self.X, self.Y))

    def move(self, reindeer_position):
        path = astar(maze, (self.Y // 64, self.X // 64), (reindeer_position[0] //64, reindeer_position[1] //64))
        if len(path) > 1:
            self.X = path[1][1] * 64
            self.Y = path[1][0] * 64
            return False
        else:
            return True

def draw_border():
    for i in range(12):
        if kinderki:
            draw_block(i * 64, 0, (255, 255, 255))

def draw_maze():
    for i in range(12):
        for j in range(12):
            if maze[i][j] == 1:
                draw_block(j * 64, i* 64)

def draw_block(x, y, color=(168, 41, 32)):
    pygame.draw.rect(screen, color, (x, y, 64, 64))
    pygame.draw.rect(screen, (0, 0, 0), (x, y, 67, 67), 3, 1)

def show_path():
    path = astar(maze, (reindeer.Y //64, reindeer.X //64), (gingerbread.Y // 64, gingerbread.X // 64))
    for i in path:
        draw_block(i[1] * 64, i[0] * 64, (96, 231, 57))


reindeer = Reindeer(64*(1+0), 64*(1+0), pygame.image.load("img/reindeer.png"))
gingerbread = Gingerbread(64*(1+9), 64*(1+9), pygame.image.load("img/gingerbread-man.png"))
enemy = Enemy(64*10+2, 64*10+2, pygame.image.load("img/hunter.png"))


def game_over():
    clock = pygame.time.Clock()
    run = True
    while run:
        screen.fill((56, 141, 17))

        font = pygame.font.SysFont('Comic Sans MS', 100)
        text = font.render("Koniec Gry!", True, (0,0,0))
        text_rect = text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        screen.blit(text, text_rect)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start_the_game()

        pygame.display.flip()
        clock.tick(60)

def victory(time):
    clock = pygame.time.Clock()
    run = True
    m = 0
    while run:
        screen.fill((56, 141, 17))

        font = pygame.font.SysFont('Comic Sans MS', 50)
        text1 = font.render("Udało Ci się w " + str(time) + " sekund(y)!", True, (0,0,0))
        text2 = font.render("Gratulacje!", True, (0,0,0))

        text_rect = text1.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2-300))
        screen.blit(text1, text_rect)
        text_rect = text2.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2-240))
        screen.blit(text2, text_rect)
        

        m += 1

        if kinderki:
            czekolada = pygame.image.load("img/D" + str(m%4) + ".png")
            image_rect = czekolada.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2+100))
            screen.blit(czekolada, image_rect)
            pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()
        clock.tick(3)        

def reset():
    global kinderki
    reindeer.X = 64
    reindeer.Y = 64
    gingerbread.new_position((1, 1))
    enemy.X = 64*10
    enemy.Y = 64*10
    kinderki = False


def start_the_game():
    
    global kinderki
    clock = pygame.time.Clock()

    delta = 0
    T = 0
    max_tps = 10

    gingerbread.new_position((reindeer.Y // 64, reindeer.X // 64))

    score = Score()
    time_counter = Time_counter(pygame.time.get_ticks())

    run = True
    while run:
        #easter egg
        keys = pygame.key.get_pressed()
        if keys[pygame.K_1] and keys[pygame.K_0] and keys[pygame.K_2]:
            kinderki = True
            
        screen.fill((56, 141, 17))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_s]:
            show_path()
        
        draw_maze()
        draw_border()
    

        gingerbread.draw()
        reindeer.draw()
        enemy.draw()

        delta += clock.tick(60) / 1000.0
        while delta > 1 / max_tps:
            T += 1 / max_tps
            #print(T)
            delta -= 1 / max_tps

            reindeer.move()
            if round(10*T,1)%ENEMY_SPEED == 0:
                if enemy.move((reindeer.Y, reindeer.X)):
                    reset()
                    run = False
                    game_over()
                    break

        if gingerbread.found((reindeer.Y, reindeer.X)):
            score.increment()
            score.print()
            pygame.display.update()
            if score.score == TO_WIN:
                pygame.time.wait(333)
                victory(time_counter.time_since_enter // 1000)
                run = False
                break
            gingerbread.new_position((reindeer.Y // 64, reindeer.X // 64))

        score.print()
        time_counter.print()
                        
        pygame.display.update()
            
start_the_game()