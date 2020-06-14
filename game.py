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
        self.velx = 0
        self.vely = 0
        self.piso = False
        self.plataformas = None
        self.damage = 3

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

        #Cambio de sprite
        self.image = self.m[self.accion][self.cont]


        if not self.piso:
            self.gravedad()

class Plataforma(pygame.sprite.Sprite):
    def __init__(self, pos, dim):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(dim)
        self.image.fill(VERDE)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

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

    j = Jugador([100, 100], m)
    jugadores.add(j)

    p = Plataforma([200, 300],[100, 50])
    plataformas.add(p)

    p = Plataforma([500, 300],[100, 50])
    plataformas.add(p)

    p = Plataforma([0, 600],[1024, 40])
    plataformas.add(p)

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

        ventana.fill(NEGRO)
        jugadores.draw(ventana)
        espadazos.draw(ventana)
        plataformas.draw(ventana)
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
