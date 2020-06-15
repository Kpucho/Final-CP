import pygame
ROJO=[255,0,0]
VERDE=[0,255,0]
BLANCO=[255,255,255]

class Plataforma(pygame.sprite.Sprite):
    def __init__(self, pos, type):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([64,64])
        if type == s:
            self.image.fill(VERDE)
        elif type == m:
            self.image.fill(BLANCO)
        else:
            self.image.fill(ROJO)

        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.velx = 0
        self.vely = 0

    def update(Vel_fondo):
        pass
