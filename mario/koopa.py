import pygame

class Koopa:
    def __init__(self, screen):
        self.rect = pygame.Rect(150, 50, 16, 24)
        self.direction = 'r'
        self.screen = screen

    def change_direction(self):
        if self.direction == 'r':
            self.direction = 'l'
        else:
            self.direction = 'r'

    def update(self, timer):
        timer_image = timer.imagerect()
        if timer.frameindex == 2:
            timer.frameindex = 0
        else:
            if self.direction == 'r':
                self.image = pygame.transform.flip(timer_image, True, False)
            else:
                self.image = timer_image

    def blitme(self):
        self.screen.blit(pygame.transform.scale2x(self.image), self.rect)