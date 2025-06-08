import pygame

class Projetil(pygame.sprite.Sprite):
    def __init__(self, pos, destino, *groups):
        super().__init__(*groups)
        self.image = pygame.Surface((8, 8))
        self.image.fill((255, 255, 0))  # amarelo
        self.rect = self.image.get_rect(center=pos)
        self.speed = 10

        # Direção normalizada
        direction = pygame.Vector2(destino) - pygame.Vector2(pos)
        if direction.length() != 0:
            self.velocity = direction.normalize() * self.speed
        else:
            self.velocity = pygame.Vector2(0, 0)

    def update(self):
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y

        # Remove se sair da tela
        if not pygame.Rect(0, 0, 5000, 5000).colliderect(self.rect):  # ajuste conforme o mapa
            self.kill()
