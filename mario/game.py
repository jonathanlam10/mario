import pygame
from pygame import *
from goomba import Goomba
from timer import Timer
from koopa import Koopa
from mario import Mario
import sys


def strip_from_sheet(start, size, columns, rows, sheet):
    frames = []
    for j in range(rows):
        for i in range(columns):
            location = (start[0] + size[0] * i, start[1] + size[1] * j)
            frames.append(sheet.subsurface(pygame.Rect(location, size)))
    return frames


def strip_platforms(file_name, platforms):
    with open(file_name, 'r') as file:
        lines = file.readlines()
    posX = 0
    posY = 0
    width = 0
    height = 0
    for line in lines:
        numbers = line.split()
        if posX == 0 and posY == 0:
            posX = int(numbers[0]) * 2
            posY = int(numbers[1]) * 2
            width = 0
            height = 0
        elif width == 0 and height == 0:
            width = int(numbers[0]) * 2 - posX
            height = int(numbers[1]) * 2 - posY
            platforms.append(pygame.Rect(posX, posY, width, height))
            posX = 0
            posY = 0


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 450))
        self.platforms = []
        strip_platforms('images/raw.txt', self.platforms)
        self.camera = Camera(self.platforms)
        self.goomba_images = strip_from_sheet((0, 0), (16, 16), 3, 1,
                                                   pygame.image.load('images/goomba.png').convert_alpha())
        self.enemies = pygame.sprite.Group()
        self.enemies.add(Goomba(self.screen, self.goomba_images, self.platforms, 400, 368))
        self.mario = Mario(self.screen, self.platforms, self.camera)
        self.mario_small_timer = Timer(strip_from_sheet((0, 0), (17, 16), 6, 1,
                                                   pygame.image.load('images/small mario normal.png').convert_alpha()), 300)
        self.mario_big_timer = Timer(strip_from_sheet((0, 0), (16, 32), 6, 1,
                                                        pygame.image.load(
                                                            'images/adult mario normal.png').convert_alpha()), 300)
        self.marioWorld = pygame.image.load("images/emptyWorld.png")
        self.marioWorld = pygame.transform.scale2x(self.marioWorld)
        self.font = pygame.font.Font(None, 32)
        self.clock = pygame.time.Clock()


    def play(self):
        while True:
            self.check_events()
            self.update_screen()

    def update_screen(self):
        self.screen.fill((255, 255, 255))
        self.screen.blit(self.marioWorld, (self.camera.background_x, 0))
        self.mario.update(self.mario_small_timer)
        self.mario.blitme()
        self.enemies.update()
        self.enemies.draw(self.screen)
        for enemy in self.enemies:
            if enemy.killme:
                self.enemies.remove(enemy)
        enemy = pygame.sprite.spritecollideany(self.mario, self.enemies)
        if enemy is not None and int(self.mario.velocity.y) > 0:
            enemy.squish()
        self.clock.tick(60)
        pygame.display.flip()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    sys.exit()

game = Game()
game.play()