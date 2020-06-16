import pygame
AZUL=[0,0,255]
LIGHT_PINK = [212, 159, 183]
FPS = 40
class Enemy_Est1(pygame.sprite.Sprite):
    def __init__(self, pos, dim):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(dim)
        self.image.fill(LIGHT_PINK)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.accion = 1
        self.velx = 0
        self.vely = 0
        self.piso = False
        self.plataformas = None
        self.damage = 1
        self.life = 13
        self.radius = 100
        self.ataque = False
        self.ataquecont = 0

    def get_poscentro(self):
        return self.rect.center

    def comportamiento(self):
        #Comportamiento de ataque
        #El enemigo es inmovil
        if self.ataquecont < 2*FPS:
            self.ataquecont += 1
        else:
            self.ataque = False
            self.ataquecont = 0


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
            else:
                if self.rect.left < p.rect.right:
                    self.rect.left = p.rect.right


        self.rect.y+=self.vely


        if self.detectarPiso():
            self.piso = True
        else:
            self.piso = False
            # if self.accion == 0:
            #     self.accion = 2
            # elif self.accion == 1:
            #     self.accion = 3


        ls_pla = pygame.sprite.spritecollide(self, self.plataformas, False)

        for p in ls_pla:
            if self.vely > 0:
                if self.rect.bottom > p.rect.top:
                    self.rect.bottom = p.rect.top
                    self.vely = 0
                    # if self.accion == 2:
                    #     self.accion = 0
                    # elif self.accion == 3:
                    #     self.accion = 1
            else:
                if self.rect.top < p.rect.bottom:
                    self.rect.top = p.rect.bottom
                    self.vely = 0

        #Cambio de animacion
        # if self.cont < 8:
        #     self.cont += 1
        # else:
        #     self.cont = 0

        #Cambio de sprite
        # self.image = self.m[self.accion][self.cont]


        if not self.piso:
            self.gravedad()

        self.comportamiento()


class Enemy_Est2(pygame.sprite.Sprite):
    def __init__(self, pos, dim):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(dim)
        self.image.fill(AZUL)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.accion = 1
        self.velx = 0
        self.vely = 0
        self.piso = False
        self.plataformas = None
        self.damage = 1
        self.life = 13
        self.radius = 150
        self.alerta = False
        self.ataque = True
        self.ataquecont = 0

    def get_poscentro(self):
        return self.rect.center

    def comportamiento(self):
        #Comportamiento de ataque
        #El enemigo es inmovil en x
        if not self.alerta:
            self.vely = 0
        else:
            if (not self.piso) and self.vely >= 0:
                self.gravedad()
            # elif self.piso and (not self.ataque):
            #     self.vely = -5
            elif self.piso:
                self.ataque = False
            elif self.detectarTecho():
                self.alerta = False



    def gravedad(self, g = 0.5):
        if self.vely == 0:
            self.vely = g
        else:
            self.vely += g

    def detectarTecho(self):
        self.rect.y += self.vely
        lista = pygame.sprite.spritecollide(self, self.plataformas, False)
        techo = False

        for p in lista:
            if self.vely <= 0:
                if self.rect.top < p.rect.bottom:
                    techo = True
        self.rect.y -= self.vely
        return techo

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
            else:
                if self.rect.left < p.rect.right:
                    self.rect.left = p.rect.right


        self.rect.y+=self.vely


        if self.detectarPiso():
            self.piso = True
        else:
            self.piso = False
            # if self.accion == 0:
            #     self.accion = 2
            # elif self.accion == 1:
            #     self.accion = 3


        ls_pla = pygame.sprite.spritecollide(self, self.plataformas, False)

        for p in ls_pla:
            if self.vely > 0:
                if self.rect.bottom > p.rect.top:
                    self.rect.bottom = p.rect.top
                    self.vely = 0
                    # if self.accion == 2:
                    #     self.accion = 0
                    # elif self.accion == 3:
                    #     self.accion = 1
            else:
                if self.rect.top < p.rect.bottom:
                    self.rect.top = p.rect.bottom
                    self.vely = 0

        #Cambio de animacion
        # if self.cont < 8:
        #     self.cont += 1
        # else:
        #     self.cont = 0

        #Cambio de sprite
        # self.image = self.m[self.accion][self.cont]
        self.comportamiento()
