import pygame
from pygame.sprite import Sprite
from timer import Timer


class Goomba(Sprite):
    def __init__(self, screen, goomba_images, platforms, x, y):
        super(Goomba, self).__init__()
        self.platforms = platforms
        self.rect = pygame.Rect(x, y, 32, 32)
        goomba_images[0] = pygame.transform.scale2x(goomba_images[0])
        goomba_images[1] = pygame.transform.scale2x(goomba_images[1])
        goomba_images[2] = pygame.transform.scale2x(goomba_images[2])
        self.goomba_timer = Timer(goomba_images, 300)
        self.screen = screen
        self.isSquished = False
        self.killme = False
        self.velocity = -1

    def update(self):
        timer_image = self.goomba_timer.imagerect()
        self.now = pygame.time.get_ticks()
        if self.isSquished:
            if self.now - self.last <= 180:
                self.goomba_timer.frameindex = 2
                timer_image = self.goomba_timer.imagerect()
                self.image = timer_image
            else:
                self.killme = True
        else:
            if self.goomba_timer.frameindex == 2:
                self.goomba_timer.frameindex = 0
            else:
                self.image = timer_image
        if self.rect.collidelist(self.platforms) != -1:
            self.velocity *= -1
        if not self.isSquished:
            self.rect.x += self.velocity

    def squish(self):
        self.last = self.now
        self.isSquished = True

    def blitme(self):
        self.screen.blit(pygame.transform.scale2x(self.image), self.rect)