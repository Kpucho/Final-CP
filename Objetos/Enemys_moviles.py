import pygame
DORADO = [212, 175, 55]
BLANCO=[255,255,255]

class Enemy_Movil1(pygame.sprite.Sprite):
    def __init__(self, pos, dim, plataformas):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(dim)
        self.image.fill(BLANCO)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.accion = 1
        self.velx = 0
        self.vely = 0
        self.piso = False
        self.plataformas = plataformas
        self.damage = 1
        self.life = 7

    def comportamiento(self):
        #Pasivo
        #Este enemigo solo se mueve en x
        if self.accion == 1: #Izquierda
            self.rect.x -= 65
            if not self.detectarcamino():
                self.accion = 0
            self.rect.x += 65
        else:
            self.rect.x += 65
            if not self.detectarcamino():
                self.accion = 1
            self.rect.x -= 65

        #restaurar velocidad
        if self.accion == 1:
            self.velx = -3
        else:
            self.velx = 3


    def detectarcamino(self):
        self.rect.y += 1
        lista = pygame.sprite.spritecollide(self, self.plataformas, False)
        camino = False
        #Si se coloca plataforma de tipo pinchos o
        #dano verificar aqui para cambiar direccion
        for p in lista:
            camino = True
        self.rect.y -=1
        return camino

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

        #Modifica al enemigo para que choque entre "paredes"
        for p in ls_pla:
            if self.velx > 0:
                if self.rect.right > p.rect.left:
                    self.rect.right = p.rect.left
                    self.accion = 1
            else:
                if self.rect.left < p.rect.right:
                    self.rect.left = p.rect.right
                    self.accion = 0


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

class Enemy_Movil2(pygame.sprite.Sprite):
    def __init__(self, pos, dim, plataformas):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(dim)
        self.image.fill(DORADO)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.accion = 1
        self.velx = 0
        self.vely = 0
        self.piso = False
        self.plataformas = plataformas
        self.damage = 1
        self.life = 10
        self.radius = 160
        self.alerta = False
        self.posxjugador = None

    def comportamiento(self):

        if self.alerta:
            if self.rect.right < self.posxjugador:
                self.accion = 0
            elif self.rect.left > self.posxjugador:
                self.accion = 1
            else:
                #quedarse inmovil en x
                self.accion = 3

        #Detecta si hay camino
        if self.piso:
            if self.accion == 1: #Izquierda
                self.rect.x -= 65
                if not self.detectarcamino():
                    self.accion = 0
                self.rect.x += 65
            else:
                self.rect.x += 65
                if not self.detectarcamino():
                    self.accion = 1
                self.rect.x -= 65

        #restaurar velocidad x
        if self.accion == 1:
            self.velx = -4
        elif self.accion == 0:
            self.velx = 4
        else:
            self.velx = 0
        #restaurar velocidad y
        if self.piso:
            self.vely = -6
            self.piso = False


    def detectarcamino(self):
        self.rect.y += 1
        lista = pygame.sprite.spritecollide(self, self.plataformas, False)
        camino = False
        #Si se coloca plataforma de tipo pinchos o
        #dano verificar aqui para cambiar direccion
        for p in lista:
            camino = True
        self.rect.y -=1
        return camino

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

        #Modifica al enemigo para que choque entre "paredes"
        for p in ls_pla:
            if self.velx > 0:
                if self.rect.right > p.rect.left:
                    self.rect.right = p.rect.left
                    self.accion = 1
            else:
                if self.rect.left < p.rect.right:
                    self.rect.left = p.rect.right
                    self.accion = 0


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

        if not self.piso:
            self.gravedad()
