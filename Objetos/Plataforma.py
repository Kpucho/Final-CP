import pygame
ROJO=[255,0,0]
VERDE=[0,255,0]
BLANCO=[255,255,255]

class Plataforma(pygame.sprite.Sprite):
    def __init__(self, pos, type):
        pygame.sprite.Sprite.__init__(self)
        if type == 's':
            self.image = pygame.Surface([70,70])
            self.image.fill(VERDE)
        elif type == 'm':
            self.image = pygame.Surface([70,70])
            self.image.fill(BLANCO)
        else:
            self.image = pygame.Surface([70,35])
            self.image.fill(ROJO)

        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def update(self,Mundo_velx):
        self.rect.x += Mundo_velx
