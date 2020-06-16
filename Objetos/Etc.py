import pygame
ROJO=[255,0,0]

class Golpe(pygame.sprite.Sprite):
    def __init__(self, pos, me, damage = 1):
        pygame.sprite.Sprite.__init__(self)
        self.accion = 0
        self.cont = 0
        self.me = me
        self.fin = False
        self.image = self.me[self.accion][self.cont]
        self.rect = self.image.get_rect()
        self.damage = damage
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def update(self):
        if self.cont <4:
            self.cont +=1
        else:
            self.cont = 0
            self.fin =True
        self.image = self.me[self.accion][self.cont]

class Bala(pygame.sprite.Sprite):
    #Constructor Clase
    def __init__(self, pos, color = ROJO):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([20,20])
        self.image.fill(color)
        #Permite cambiar la posicion perteminada que impone get_rect
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y= pos[1]
        self.velx = 0
        self.vely = 0

    def update(self, Mundo_velx):
        self.rect.y += self.vely
        self.rect.x += self.velx + Mundo_velx
