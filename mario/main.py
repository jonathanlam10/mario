import pygame
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

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((700, 700))
        self.goomba = Goomba('images/goomba.png', self.screen)
        self.goomba_timer = Timer(strip_from_sheet((0, 0), (16, 16), 3, 1,
                                                   pygame.image.load('images/goomba.png').convert_alpha()), 300)
        self.koopa = Koopa(self.screen)
        self.koopa_timer = Timer(strip_from_sheet((0, 0), (16, 24), 2, 1,
                                                   pygame.image.load('images/koopa.png').convert_alpha()), 300)
        self.mario = Mario(self.screen)
        self.mario_small_timer = Timer(strip_from_sheet((0, 0), (17, 16), 6, 1,
                                                   pygame.image.load('images/small mario normal.png').convert_alpha()), 300)
        self.mario_big_timer = Timer(strip_from_sheet((0, 0), (16, 32), 6, 1,
                                                        pygame.image.load(
                                                            'images/adult mario normal.png').convert_alpha()), 300)
        self.marioX, self.marioY = 0, 0

    def play(self):
        while True:
            self.check_events()
            self.update_screen()

    def update_screen(self):
        self.screen.fill((255, 255, 255))
        if not self.goomba.isSquished:
            self.goomba.update(self.goomba_timer)
        self.goomba.blitme()
        self.koopa.update(self.koopa_timer)
        self.koopa.blitme()
        self.mario.update(self.mario_small_timer, self.marioX, self.marioY)
        self.mario.blitme()
        pygame.display.flip()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    sys.exit()
                elif event.key == pygame.K_SPACE:
                    self.koopa.change_direction()
                    self.goomba.squish(self.goomba_timer)
                    if self.marioY == 0:
                        self.marioY = 1
                    else:
                        self.marioY = 0
                elif event.key == pygame.K_d:
                    self.marioX += 1
                elif event.key == pygame.K_a:
                    self.marioX -= 1

game = Game()
game.play()