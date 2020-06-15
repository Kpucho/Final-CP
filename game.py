import pygame
import random
from lib import *

class Jugador (pygame.sprite.Sprite):
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


class Plataforma(pygame.sprite.Sprite):
    def __init__(self, pos, dim):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(dim)
        self.image.fill(VERDE)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.velx = 0
        self.vely = 0


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

class EnemigoEst1(pygame.sprite.Sprite):
    def __init__(self, pos, dim, plataformas):
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
        self.plataformas = plataformas
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

    def update(self):
        self.rect.y += self.vely
        self.rect.x += self.velx


def Juego(ventana):
    #Borra lo anterior
    ventana.fill(NEGRO)
    #recorte de sprites
    im_slime = pygame.image.load('Sprites/slime.png')
    m = []
    for j in range(6):
        fila = []
        for c in range(9):
            cuadro = im_slime.subsurface(128*c, 128*j, 128, 128)
            fila.append(cuadro)
        m.append(fila)

    im_espada = pygame.image.load('Sprites/Espada.png')
    me = []
    for j in range(2):
        fila = []
        for c in range(5):
            cuadro = im_espada.subsurface(64*c, 128*j, 64, 128)
            fila.append(cuadro)
        me.append(fila)

    #Cargar mapa
    #fondojuego = pygame.image.load('carmap.png')

    # pygame.mixer.init(44100, -16, 2, 2048)
    #musica = pygame.mixer.Sound('sonidos/juego.wav')

    jugadores = pygame.sprite.Group()
    plataformas = pygame.sprite.Group()
    espadazos = pygame.sprite.Group()
    enemigos1 = pygame.sprite.Group()
    enemigos2 = pygame.sprite.Group()
    enemigosEst1 = pygame.sprite.Group()

    balas_ene = pygame.sprite.Group()


    j = Jugador([50, 100], m)
    jugadores.add(j)

    p = Plataforma([200, 300],[100, 50])
    plataformas.add(p)

    p = Plataforma([500, 300],[100, 50])
    plataformas.add(p)

    p = Plataforma([0, 576],[1024, 64])
    plataformas.add(p)

    p = Plataforma([832, 512],[192, 64])
    plataformas.add(p)

    p = Plataforma([0, 512],[64, 64])
    plataformas.add(p)

    p = Plataforma([960, 448],[64, 64])
    plataformas.add(p)

    ene = Enemigo1([850, 448], [64,64], plataformas)
    enemigos1.add(ene)

    ene2 = Enemigo2([512,512], [64,64], plataformas)
    enemigos2.add(ene2)
    # eneEst1 = EnemigoEst1([512, 512], [64, 64], plataformas)
    # enemigosEst1.add(eneEst1)

    j.plataformas = plataformas


    reloj = pygame.time.Clock()
    fin_juego = False
    fin = False
    #musica.play(-1)
    """Eventos"""
    while not fin and (not fin_juego):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fin = True
            if event.type ==pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    j.velx = 10
                    if not j.piso:
                        j.accion = 2
                    else:
                        j.vely = 0
                        j.accion = 0
                    j.cont = 0
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    j.velx = -10
                    if not j.piso:
                        j.accion = 3
                    else:
                        j.vely = 0
                        j.accion = 1
                    j.cont = 0
                if event.key == pygame.K_SPACE:
                    j.vely = -10
                    j.piso = False
                    if j.accion == 0:
                        j.accion = 2
                    elif j.accion == 1:
                        j.accion = 3
                    j.cont = 0
                if event.key == pygame.K_f:
                    if j.accion == 0:
                        j.accion = 4
                        j.cont = 0
                        espada = Golpe([j.lateral_der(), j.rect.y], me)
                        espada.accion = 0
                        espadazos.add(espada)
                    elif j.accion == 1:
                        j.accion = 5
                        j.cont = 0
                        espada = Golpe([j.lateral_izq() - 64, j.rect.y], me)
                        espada.accion = 1
                        espadazos.add(espada)
            if event.type == pygame.KEYUP:
                j.velx = 0

        #control
        # Deteccion de cercania
        # if pygame.sprite.collide_circle(r,j):
        #     print 'cerca', r.id

        #Actualizacion de pos del jugador para los enemigos
        #Colisiones radiales
        for ene2 in enemigos2:
            if ene2.alerta:
                ene2.posxjugador = j.rect.centerx
            elif pygame.sprite.collide_circle(ene2,j):
                print 'Alerta'
                ene2.alerta = True

        #SECCION DE CREACCION

        #crear balas enemigas de ciertos enemigos
        #Crea las balas del enemigo estacionario de nivel 1
        for eneEst1 in enemigosEst1:
            if not eneEst1.ataque:
                eneEst1.ataque = True
                #Bala izq
                bala_e = Bala(eneEst1.get_poscentro())
                bala_e.velx = -5
                balas_ene.add(bala_e)
                #Bala der
                bala_e = Bala(eneEst1.get_poscentro())
                bala_e.velx = 5
                balas_ene.add(bala_e)
                #Bala superior
                bala_e = Bala(eneEst1.get_poscentro())
                bala_e.vely = -5
                balas_ene.add(bala_e)


        #SECCION DE ELIMINACION
        #Eliminacion de balas con las paredes y fuera de area:
        for bala in balas_ene:
            if pygame.sprite.spritecollide(bala, plataformas, False):
                balas_ene.remove(bala)
            elif pygame.sprite.spritecollide(bala, jugadores, False):
                # Bajar vida al jugador

                #Retroceso del golpe
                j.retroceso = True
                if bala.velx > 0:
                    j.velx = 50
                else:
                    j.velx = -50
                balas_ene.remove(bala)
            elif pygame.sprite.spritecollide(bala, espadazos, False):
                balas_ene.remove(bala)
            elif bala.rect.y < -50 or bala.rect.y > (ALTO + 50):
                balas_ene.remove(bala)
            elif bala.rect.x < -50 or bala.rect.x > (ANCHO + 50):
                balas_ene.remove(bala)


        #Eliminacion del enemigo por el espadazo por 1
        for espada in espadazos:
            ls_ene = pygame.sprite.spritecollide(espada, enemigos1, False)
            for enemigo in ls_ene:
                enemigos1.remove(enemigo)

        for espada in espadazos:
            ls_ene = pygame.sprite.spritecollide(espada, enemigosEst1, False)
            for enemigo in ls_ene:
                enemigosEst1.remove(enemigo)

        #Eliminacion del golpe del jugador
        for espada in espadazos:
            if espada.fin:
                if j.accion == 4:
                    j.accion = 0
                elif j.accion == 5:
                    j.accion = 1
                espadazos.remove(espada)


        #Refresco
        jugadores.update()
        espadazos.update()
        enemigos1.update()
        enemigosEst1.update()
        enemigos2.update()
        balas_ene.update()

        ventana.fill(NEGRO)
        plataformas.draw(ventana)
        enemigos1.draw(ventana)
        enemigosEst1.draw(ventana)
        enemigos2.draw(ventana)
        jugadores.draw(ventana)
        balas_ene.draw(ventana)
        espadazos.draw(ventana)

        pygame.display.flip()
        reloj.tick(FPS)

    #musica.stop()
    FinJuego(ventana)

def FinJuego(ventana):
    ventana.fill(NEGRO)
    pygame.font.init()
    pygame.mixer.init(44100, -16, 2, 2048)
    #musica = pygame.mixer.Sound('sonidos/final.wav')
    fuente = pygame.font.Font(None, 40)
    #fondo  = pygame.image.load('images/fin_juego.jpg')
    click = False
    #musica.play(-1)
    fin = False
    volver = False
    while (not fin) and (not volver):
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fin = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        #ventana.blit(fondo, [0,0])
        mx, my = pygame.mouse.get_pos()
        draw_text(Titulo, fuente, ROJO, ventana, [300, 650])
        boton1 = pygame.Rect(100, 400, 250, 50)

        boton2 = pygame.Rect(450, 400, 250, 50)
        if boton1.collidepoint((mx, my)):
            if click:
                volver = True
        if boton2.collidepoint((mx, my)):
            if click:
                fin = True
        pygame.draw.rect(ventana, LIGHT_ROJO, boton1)
        draw_text('Volver a jugar', fuente, BLANCO, ventana, [120, 410])
        pygame.draw.rect(ventana, LIGHT_ROJO, boton2)
        draw_text('Salir', fuente, BLANCO, ventana, [540, 410])

        click = False

    if not fin:
        #musica.stop()
        Juego(ventana)

def Menu(ventana):
    ventana.fill(NEGRO)
    pygame.font.init()
    pygame.mixer.init(44100, -16, 2, 2048)
    fuente = pygame.font.Font(None, 40)
    #fondo  = pygame.image.load('images/fondo.png')
    #musica = pygame.mixer.Sound('sonidos/menu.wav')
    fin = False
    previo = False
    info_juego = False
    click = False
    #musica.play(-1)
    while (not fin) and (not previo) and (not info_juego):

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fin = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        #ventana.blit(fondo, [0,0])
        mx, my = pygame.mouse.get_pos()
        draw_text('Un titulo mamon', fuente, BLANCO, ventana, [300, 50])
        boton1 = pygame.Rect(300, 150, 220, 50)
        boton2 = pygame.Rect(300, 250, 220, 50)
        boton3 = pygame.Rect(300, 350, 220, 50)

        if boton1.collidepoint((mx, my)):
            if click:
                previo = True
        if boton2.collidepoint((mx, my)):
            if click:
                info_juego = True
        if boton3.collidepoint((mx, my)):
            if click:
                fin = True
        pygame.draw.rect(ventana, LIGHT_PINK, boton1)
        draw_text('Iniciar', fuente, BLANCO, ventana, [370, 160])
        pygame.draw.rect(ventana, LIGHT_PINK, boton2)
        draw_text('Como jugar', fuente, BLANCO, ventana, [350, 260])
        pygame.draw.rect(ventana, LIGHT_PINK, boton3)
        draw_text('Salir', fuente, BLANCO, ventana, [370, 360])

        click = False

    #musica.stop()
    if (previo):
        Juego(ventana)
    if (info_juego):
        InfoJuego(ventana)

def InfoJuego(ventana):
    ventana.fill(NEGRO)
    pygame.font.init()
    pygame.mixer.init(44100, -16, 2, 2048)
    fuente = pygame.font.Font(None, 40)
    #fondo  = pygame.image.load('images/infoJuego.jpg')
    #musica = pygame.mixer.Sound('sonidos/xd.wav')
    fin = False
    iniciar = False
    click = False
    #musica.play(-1)
    while (not fin) and (not iniciar):
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fin = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        #ventana.blit(fondo, [0,0])

        mx, my = pygame.mouse.get_pos()
        draw_text('Como jugar', fuente, BLANCO, ventana, [300, 50])
        draw_text(Titulo, fuente, BLANCO, ventana, [300, 670])
        boton1 = pygame.Rect(100, 580, 250, 50)

        boton2 = pygame.Rect(450, 580, 250, 50)
        if boton1.collidepoint((mx, my)):
            if click:
                iniciar = True
        if boton2.collidepoint((mx, my)):
            if click:
                fin = True

        pygame.draw.rect(ventana, LIGHT_ROJO, boton1)
        draw_text('Jugar', fuente, BLANCO, ventana, [190, 590])
        pygame.draw.rect(ventana, LIGHT_ROJO, boton2)
        draw_text('Salir', fuente, BLANCO, ventana, [540, 590])

        click = False

    #musica.stop()
    if (iniciar):
        Juego(ventana)







if __name__ == '__main__':
    ventana = pygame.display.set_mode([ANCHO,ALTO])
    pygame.display.set_caption(Titulo)
    #pygame.display.set_icon(pygame.image.load(''))
    """                       MENU                                        """

    Menu(ventana)
