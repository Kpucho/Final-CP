import pygame
import random
from lib import *

class Enemigo1(pygame.sprite.Sprite):
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
        self.rect.y += 30
        lista = pygame.sprite.spritecollide(self, self.plataformas, False)
        suelo = False

        for p in lista:
            if self.vely >= 0:
                if self.rect.bottom > p.rect.top:
                    suelo = True
        self.rect.y -= 30
        return suelo

    def update(self, plataformas, fondovel):

        self.rect.x += self.velx
        self.rect.x += fondovel[0]
        self.plataformas = plataformas


        ls_pla = pygame.sprite.spritecollide(self, self.plataformas, False)

        #Modifica al enemigo para que choque entre "paredes"
        for p in ls_pla:
            if self.velx > 0:
                if self.rect.right > p.rect.left:
                    self.rect.right = p.rect.left
                    self.accion = 1
            else:
                if self.rect.left < p.rect.right and self.velx != 0:
                    self.rect.left = p.rect.right
                    self.accion = 0


        self.rect.y+=self.vely
        self.rect.y+=fondovel[1]



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
                if self.rect.top < p.rect.bottom and self.vely != 0:
                    self.rect.top = p.rect.bottom
                    self.vely = 0


        if self.detectarPiso():
            self.piso = True
        else:
            self.piso = False
            # if self.accion == 0:
            #     self.accion = 2
            # elif self.accion == 1:
            #     self.accion = 3

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

class EnemigoEst1(pygame.sprite.Sprite):
    def __init__(self, pos, dim, plataformas):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(dim)
        self.image.fill(LIGHT_PINK)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.accion = 1
        self.cont = 0
        self.velx = 0
        self.vely = 0
        self.piso = False
        self.plataformas = plataformas
        self.damage = 1
        self.life = 60
        self.radius = 200
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

    def update(self, plataformas, fondovel):

        self.plataformas = plataformas
        self.rect.x += self.velx + fondovel[0]

        ls_pla = pygame.sprite.spritecollide(self, self.plataformas, False)


        for p in ls_pla:
            if self.velx > 0:
                if self.rect.right > p.rect.left:
                    self.rect.right = p.rect.left
            else:
                if self.rect.left < p.rect.right and self.velx != 0:
                    self.rect.left = p.rect.right


        self.rect.y+=self.vely + fondovel[1]


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
                if self.rect.top < p.rect.bottom and self.vely != 0:
                    self.rect.top = p.rect.bottom
                    self.vely = 0

        #Cambio de animacion
        if self.cont < 8:
            self.cont += 1
        else:
            self.cont = 0

        #Cambio de sprite
        # self.image = self.m[self.accion][self.cont]

        if not self.piso:
            self.gravedad()

        self.comportamiento()

class Enemigo2(pygame.sprite.Sprite):
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
                if self.rect.left < p.rect.right and self.velx != 0:
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
                if self.rect.top < p.rect.bottom and self.vely != 0:
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

class EnemigoEst2(pygame.sprite.Sprite):
    def __init__(self, pos, dim, plataformas, radio = 300):
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
        self.plataformas = plataformas
        self.damage = 1
        self.life = 30
        self.radius = 300
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

    def update(self, plataformas, velfondo):

        self.plataformas = plataformas

        self.rect.x += self.velx + velfondo[0]

        ls_pla = pygame.sprite.spritecollide(self, self.plataformas, False)


        for p in ls_pla:
            if self.velx > 0:
                if self.rect.right > p.rect.left:
                    self.rect.right = p.rect.left
            else:
                if self.rect.left < p.rect.right and self.velx != 0:
                    self.rect.left = p.rect.right


        self.rect.y+=self.vely + velfondo[1]


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
                if self.rect.top < p.rect.bottom and self.vely != 0:
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

# class Jefe1(pygame.sprite.Sprite):
#     def __init__(self, pos, dim, plataformas):
#         pygame.sprite.Sprite.__init__(self)
#         self.image = pygame.Surface(dim)
#         self.image.fill(DORADO)
#         self.rect = self.image.get_rect()
#         self.cont = 0
#         self.rect.x = pos[0]
#         self.rect.y = pos[1]
#         self.accion = 1
#         self.velx = 0
#         self.vely = 0
#         self.piso = False
#         self.plataformas = plataformas
#         self.damage = 1
#         self.life = 100
#         self.radius = 200
#         self.alerta = False
#         self.poder = True
#         self.podercont = 0
#         self.posxjugador = None
#
#     def comportamiento(self):
#
#         if self.alerta:
#             #Cambia posicion
#             if self.poder:
#                 # Se mueve hacia el jugador
#                 if self.rect.right < self.posxjugador:
#                     self.accion = 0
#                 elif self.rect.left > self.posxjugador:
#                     self.accion = 1
#                 else:
#                     #quedarse inmovil en x
#                     self.accion = 3
#             else:
#                 # Huye del jugador
#                 # Se mueve hacia el jugador
#                 if self.rect.right < self.posxjugador:
#                     self.accion = 1
#                 elif self.rect.left > self.posxjugador:
#                     self.accion = 0
#                 else:
#                     #quedarse inmovil en x
#                     self.accion = 2
#
#             if self.podercont < 10*FPS:
#                 self.podercont += 1
#             else:
#                 if not self.poder:
#                     self.poder = True
#                     self.podercont = 0
#
#         #Detecta si hay camino
#         if self.piso:
#             if self.accion == 1: #Izquierda
#                 self.rect.x -= 65
#                 if not self.detectarcamino():
#                     self.accion = 0
#                 self.rect.x += 65
#             else:
#                 self.rect.x += 65
#                 if not self.detectarcamino():
#                     self.accion = 1
#                 self.rect.x -= 65
#
#         #restaurar velocidad x
#         if self.accion == 1:
#             self.velx = -4
#         elif self.accion == 0:
#             self.velx = 4
#         else:
#             self.velx = 0
#
#     def lateral_der(self):
#         return self.rect.right
#     def lateral_izq(self):
#         return self.rect.left
#     def detectarcamino(self):
#         self.rect.y += 1
#         lista = pygame.sprite.spritecollide(self, self.plataformas, False)
#         camino = False
#         #Si se coloca plataforma de tipo pinchos o
#         #dano verificar aqui para cambiar direccion
#         for p in lista:
#             camino = True
#         self.rect.y -=1
#         return camino
#
#     def gravedad(self, g = 0.5):
#         if self.vely == 0:
#             self.vely = g
#         else:
#             self.vely += g
#
#     def detectarPiso(self):
#         self.rect.y += 1
#         lista = pygame.sprite.spritecollide(self, self.plataformas, False)
#         suelo = False
#
#         for p in lista:
#             if self.vely >= 0:
#                 if self.rect.bottom > p.rect.top:
#                     suelo = True
#         self.rect.y -=1
#         return suelo
#
#     def update(self, plataformas, fondovel):
#
#         self.plataformas = plataformas
#         self.rect.x += self.velx + fondovel[0]
#
#         ls_pla = pygame.sprite.spritecollide(self, self.plataformas, False)
#
#         #Modifica al enemigo para que choque entre "paredes"
#         for p in ls_pla:
#             if self.velx > 0:
#                 if self.rect.right > p.rect.left:
#                     self.rect.right = p.rect.left
#                     self.accion = 1
#             else:
#                 if self.rect.left < p.rect.right and self.velx != 0:
#                     self.rect.left = p.rect.right
#                     self.accion = 0
#
#
#         self.rect.y+=self.vely + fondovel[1]
#
#
#         if self.detectarPiso():
#             self.piso = True
#         else:
#             self.piso = False
#             # if self.accion == 0:
#             #     self.accion = 2
#             # elif self.accion == 1:
#             #     self.accion = 3
#
#
#         ls_pla = pygame.sprite.spritecollide(self, self.plataformas, False)
#
#         for p in ls_pla:
#             if self.vely > 0:
#                 if self.rect.bottom > p.rect.top:
#                     self.rect.bottom = p.rect.top
#                     self.vely = 0
#                     # if self.accion == 2:
#                     #     self.accion = 0
#                     # elif self.accion == 3:
#                     #     self.accion = 1
#             else:
#                 if self.rect.top < p.rect.bottom and self.vely != 0:
#                     self.rect.top = p.rect.bottom
#                     self.vely = 0
#
#         #Cambio de animacion
#         # if self.cont < 8:
#         #     self.cont += 1
#         # else:
#         #     self.cont = 0
#
#         #Cambio de sprite
#         # self.image = self.m[self.accion][self.cont]
#
#         self.comportamiento()
#
#         if not self.piso:
#             self.gravedad()
