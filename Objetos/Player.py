import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, m):
        pygame.sprite.Sprite.__init__(self)
        self.m = m
        self.accion = 0
        self.cont = 0
        self.image = self.m[self.accion][self.cont]
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.radius = 64
        self.velx = 0
        self.vely = 0
        self.piso = False
        self.plataformas = None
        self.damage = 3
        self.retroceso = False

    def lateral_der(self):
        return self.rect.right

    def lateral_izq(self):
        return self.rect.left

    def gravedad(self, g = 0.5):
        if self.vely == 0:
            self.vely = g
        else:
            self.vely += g

    def detectarPiso(self):
        self.rect.y += 1
        lista = pygame.sprite.spritecollide(self, self.plataformas, False)
        suelo = False

        for p in lista:
            if self.vely >= 0:
                if self.rect.bottom > p.rect.top:
                    suelo = True
        self.rect.y -=1
        return suelo

    def update(self):

        self.rect.x += self.velx
        ls_pla = pygame.sprite.spritecollide(self, self.plataformas, False)

        for p in ls_pla:
            if self.velx > 0:
                if self.rect.right > p.rect.left:
                    self.rect.right = p.rect.left
                    self.velx = 0
            else:
                if self.rect.left < p.rect.right:
                    self.rect.left = p.rect.right
                    self.velx = 0


        self.rect.y+=self.vely


        #Corregir luego
        if self.detectarPiso():
            self.piso = True
        else:
            self.piso = False
            if self.accion == 0:
                self.accion = 2
            elif self.accion == 1:
                self.accion = 3


        ls_pla = pygame.sprite.spritecollide(self, self.plataformas, False)

        for p in ls_pla:
            if self.vely > 0:
                if self.rect.bottom > p.rect.top:
                    self.rect.bottom = p.rect.top
                    self.vely = 0
                    if self.accion == 2:
                        self.accion = 0
                    elif self.accion == 3:
                        self.accion = 1
            else:
                if self.rect.top < p.rect.bottom:
                    self.rect.top = p.rect.bottom
                    self.vely = 0

        #Cambio de animacion
        if self.cont < 8:
            self.cont += 1
        else:
            self.cont = 0

        if self.retroceso:
            self.retroceso = False
            self.velx = 0

        if not self.piso:
            self.gravedad()

        #Cambio de sprite
        self.image = self.m[self.accion][self.cont]
