import pygame
from pygame.sprite import Sprite
from pygame import *

class Mario(Sprite):
    def __init__(self, screen, platforms, camera):
        super(Mario, self).__init__()
        self.screen = screen
        self.rect = pygame.Rect(0, 300, 17, 16)
        self.camera = camera
        self.direction = 'r'
        self.velocity = pygame.math.Vector2()
        self.velocity.x = 0
        self.velocity.y = 0
        self.max_speed = 5
        self.jump_max = 10
        self.isCrouched = False
        self.onGround = False
        self.platforms = platforms
        self.width = 17
        self.height = 16

    def change(self, newMarioType):
        if newMarioType == 'big':
            self.rect = pygame.Rect(self.rect[0], self.rect[1], 17, 32)
            self.height = 32
        elif newMarioType == 'small':
            self.rect = pygame.Rect(self.rect[0], self.rect[1], 17, 16)
            self.height = 16

    def update(self, timer):
        timer_image = timer.imagerect()
        if int(self.velocity.y) == 0:
            if self.isCrouched:
                timer.frameindex = 6
                self.image = timer_image
            elif self.velocity.x == 0:
                timer.frameindex = 0
                if self.direction == 'l':
                    self.image = pygame.transform.flip(timer_image, True, False)
                else:
                    self.image = timer_image
            elif self.velocity.x > 0:
                self.direction = 'r'
                if timer.frameindex == 4:
                    timer.frameindex = 1
                else:
                    timer.wait = 300 / (abs(self.velocity.x) / 2)
                    self.image = timer_image
            elif self.velocity.x < 0:
                self.direction = 'l'
                if timer.frameindex == 4:
                    timer.frameindex = 1
                else:
                    timer.wait = 300 / (abs(self.velocity.x) / 2)
                    self.image = pygame.transform.flip(timer_image, True, False)
        else:
            if self.isCrouched:
                timer.frameindex = 6
            elif not self.isCrouched:
                timer.frameindex = 5
                if self.direction == 'l':
                    self.image = pygame.transform.flip(timer_image, True, False)
                else:
                    self.image = timer_image
        pressed = pygame.key.get_pressed()
        up = pressed[K_UP]
        left = pressed[K_LEFT]
        right = pressed[K_RIGHT]
        if up:
            if self.onGround and self.velocity.y <= self.jump_max:
                self.jump.play()
                self.velocity.y -= 10
        if left and abs(self.velocity.x) <= self.max_speed:
            self.velocity.x -= 0.3
        if right and self.velocity.x <= self.max_speed:
            self.velocity.x += 0.3
        if not self.onGround:
            self.velocity.y += 0.3
            if self.velocity.y > 10:
                self.velocity.y = 10
        if left and self.velocity.x > 0:
            self.velocity.x -= 0.2
        if right and self.velocity.x < 0:
            self.velocity.x += 0.2
        if not right and not left:
            if self.velocity.x > 0.2:
                self.velocity.x -= 0.1
            elif self.velocity.x < -0.2:
                self.velocity.x += 0.1
            else:
                self.velocity.x = 0
        self.rect.x += self.velocity.x
        self.collide(self.velocity.x, 0, self.platforms)
        self.rect.y += self.velocity.y
        self.onGround = False
        self.collide(0, self.velocity.y, self.platforms)
        # print(self.velocity)

    def collide(self, xvelocity, yvelocity, platforms):
        x = self.rect.collidelist(platforms)
        if x != -1:
            if xvelocity > 0:
                self.rect.right = platforms[x].left
                self.velocity.x = 0
            if xvelocity < 0:
                self.rect.left = platforms[x].right
                self.velocity.x = 0
            if yvelocity > 0:
                self.rect.bottom = platforms[x].top
                self.onGround = True
                self.velocity.y = 0
            if yvelocity < 0:
                self.rect.top = platforms[x].bottom
                self.velocity.y = 0
        if self.rect.colliderect(self.camera.edge):
            self.rect.right = self.camera.edge.left
            self.camera.update(xvelocity)

    def blitme(self):
        self.screen.blit(pygame.transform.scale2x(self.image), self.rect.inflate(self.width, self.height))