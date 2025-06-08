import pygame

class Camera:
    def __init__(self, width, height):
        self.offset = pygame.Vector2(0, 0)
        self.width = width
        self.height = height

    def apply(self, rect):
        return rect.move(self.offset)

    def update(self, target):
        self.offset.x = -target.rect.centerx + 400  # metade da tela (800x600)
        self.offset.y = -target.rect.centery + 300

        # Limites da câmera
        self.offset.x = max(min(0, self.offset.x), -(self.width - 800))
        self.offset.y = max(min(0, self.offset.y), -(self.height - 600))
