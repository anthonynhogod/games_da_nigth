import pygame

class Slime(pygame.sprite.Sprite):
    def __init__(self, frames, pos, grupo_inimigos, *groups):
        super().__init__(*groups)
        self.frames = frames
        self.index = 0
        self.image = self.frames[self.index]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft=pos)
        self.animation_speed = 0.15
        self.counter = 0
        self.speed = 1.5
        self.grupo_inimigos = grupo_inimigos

    def update(self, player):
        # Animação
        self.counter += self.animation_speed
        if self.counter >= len(self.frames):
            self.counter = 0
        self.index = int(self.counter)
        self.image = self.frames[self.index]
        self.mask = pygame.mask.from_surface(self.image)

        # Movimento em direção ao player
        direction = pygame.Vector2(player.rect.center) - pygame.Vector2(self.rect.center)
        if direction.length() != 0:
            direction = direction.normalize()
            nova_pos = self.rect.move(direction * self.speed)

            # Verifica colisão com outros slimes usando máscara
            for outro in self.grupo_inimigos:
                if outro != self:
                    offset = (int(outro.rect.x - nova_pos.x), int(outro.rect.y - nova_pos.y))
                    if self.mask.overlap(outro.mask, offset):
                        return  # colisão detectada, não se move

            self.rect = nova_pos

