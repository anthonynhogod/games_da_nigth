import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, frames, pos, *groups):
        super().__init__(*groups)
        self.frames = frames
        self.index = 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect(topleft=pos)
        self.animation_speed = 0.15
        self.counter = 0
        self.speed = 3

    def update(self, keys):
        moving = False
        dx, dy = 0, 0

        if keys[pygame.K_a]:
            dx -= self.speed
            moving = True
        if keys[pygame.K_d]:
            dx += self.speed
            moving = True
        if keys[pygame.K_w]:
            dy -= self.speed
            moving = True
        if keys[pygame.K_s]:
            dy += self.speed
            moving = True

        self.rect.x += dx
        self.rect.y += dy

        if moving:
            self.counter += self.animation_speed
            if self.counter >= len(self.frames):
                self.counter = 0
            self.index = int(self.counter)
            self.image = self.frames[self.index]
