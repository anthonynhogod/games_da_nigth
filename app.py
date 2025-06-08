import pygame 
import pytmx
from Slime import Slime
from Camera import Camera
from Player import Player
import random
from Projetil import Projetil
import time

tempo_ultimo_spawn = time.time()
intervalo_spawn = 5 # segundos entre spawns (começa lento)
min_intervalo = 0.5 # limite mínimo de intervalo
reduzir_intervalo = 0.95# fator de aceleração

pygame.init()

display = pygame.display.set_mode([840, 480])
#Titulo 
pygame.display.set_caption("Game da nigth")

#Musica
pygame.mixer.music.load("data/soungs/base.wav")
pygame.mixer.music.play(-1)
#Efeito sonoro 
#tiro = pygame.mixer.Sound(...)
#tiro.play()

animacao_player = pygame.image.load("data/player_andar.png").convert_alpha()
player_frames = []
for i in range(4):
    frame = animacao_player.subsurface(pygame.Rect(i * 32, 0, 32, 32))
    player_frames.append(pygame.transform.scale(frame, (64, 64)))

animacao_slime = pygame.image.load("data/slime_andar.png").convert_alpha()
frames = []
for i in range(3):
    frame = animacao_slime.subsurface(pygame.Rect(i * 32, 0, 32, 32))
    frames.append(pygame.transform.scale(frame, (64, 64)))

groupoInimigos = pygame.sprite.Group()

grupoPlayer = pygame.sprite.Group()

grupoProjetil = pygame.sprite.Group()




player = Player(player_frames, (100, 100), grupoPlayer)

tmx_data = pytmx.load_pygame("data/mapa1.tmx")

def desenhar_mapa(surface, tmx_map, camera):
    for layer in tmx_map.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                tile = tmx_map.get_tile_image_by_gid(gid)
                if tile:
                    pos = pygame.Rect(x * tmx_map.tilewidth, y * tmx_map.tileheight, 0, 0)
                    surface.blit(tile, camera.apply(pos))

# X ----->
# Y |
#   V

camera = Camera(tmx_data.width * tmx_data.tilewidth, tmx_data.height * tmx_data.tileheight)


def spawn_slime():
    x = random.randint(0, tmx_data.width * tmx_data.tilewidth)
    y = random.randint(0, tmx_data.height * tmx_data.tileheight)
    slime = Slime(frames, (x, y), groupoInimigos, groupoInimigos)


gameloop = True
clock = pygame.time.Clock()

if __name__ == "__main__":
    while gameloop:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameloop = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                destino = pygame.mouse.get_pos()
                destino_mundo = pygame.Vector2(destino) - camera.offset  # converte para coordenadas do mundo
                projetil = Projetil(player.rect.center, destino_mundo, grupoProjetil)


        keys = pygame.key.get_pressed()
        grupoPlayer.update(keys)

        camera.update(player)  # atualiza a câmera com base no player

        display.fill((0, 0, 0))  # limpa a tela

        desenhar_mapa(display, tmx_data, camera)

        for sprite in grupoPlayer:
            display.blit(sprite.image, camera.apply(sprite.rect))

        groupoInimigos.update(player)
        
        for inimigo in groupoInimigos:
            display.blit(inimigo.image, camera.apply(inimigo.rect))

        grupoProjetil.update()

        for p in grupoProjetil:
            display.blit(p.image, camera.apply(p.rect))

        for projetil in grupoProjetil:
            atingidos = pygame.sprite.spritecollide(projetil, groupoInimigos, dokill=True, collided=pygame.sprite.collide_mask)
            if atingidos:
                projetil.kill()
        tempo_atual = time.time()
        if tempo_atual - tempo_ultimo_spawn >= intervalo_spawn:
            spawn_slime()
            tempo_ultimo_spawn = tempo_atual
            intervalo_spawn = max(min_intervalo, intervalo_spawn * reduzir_intervalo)

        pygame.display.update()

    
    pygame.quit()