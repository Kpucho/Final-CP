import pygame
import random
import ConfigParser
from lib import *
from Objetos import *

archivo = ConfigParser.ConfigParser()

def Tutorial(ventana):
    ventana.fill(NEGRO)
    pygame.mixer.init(44100, -16, 2, 2048)
    archivo.read('Mapas/Tutorial.map')

    """Creacion del mundo"""
    j=0
    for fila in Mapa1:
        i=0
        for c in fila:
            type = string(archivo.get(c,'tipo'))
            px=int(archivo.get(c,'px'))
            py=int(archivo.get(c,'px'))
            col=int(archivo.get(c,'colision'))
            if col != 0:
                ventana.blit(Mundo1[px][py],[64*i,64*j])
            i+=1
        j+=1

    #fondojuego = pygame.image.load('carmap.png')
    #musica = pygame.mixer.Sound('sonidos/juego.wav')

    reloj = pygame.time.Clock()
    fin_juego = False
    fin = False
    #musica.play(-1)
    """Eventos"""
    while not fin and (not NextLvl):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fin = True
            if event.type ==pygame.KEYDOWN:
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    pass
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    pass
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    pass
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    pass


        #Dibujado
        ventana.fill(NEGRO)
        pygame.display.flip()
        reloj.tick(FPS)

def Lvl1(ventana):
    ventana.fill(NEGRO)
    pygame.mixer.init(44100, -16, 2, 2048)
    archivo.read('Mapas/Level1.map')

    """Creacion del mundo"""
    j=0
    for fila in Mapa1:
        i=0
        for c in fila:
            type = string(archivo.get(c,'tipo'))
            px=int(archivo.get(c,'px'))
            py=int(archivo.get(c,'px'))
            col=int(archivo.get(c,'colision'))
            if col != 0:
                ventana.blit(Mundo1[px][py],[64*i,64*j])
            i+=1
        j+=1

    #fondojuego = pygame.image.load('carmap.png')
    #musica = pygame.mixer.Sound('sonidos/juego.wav')

    reloj = pygame.time.Clock()
    fin_juego = False
    fin = False
    #musica.play(-1)
    """Eventos"""
    while not fin and (not NextLvl):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fin = True
            if event.type ==pygame.KEYDOWN:
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    pass
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    pass
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    pass
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    pass


        #Dibujado
        ventana.fill(NEGRO)
        pygame.display.flip()
        reloj.tick(FPS)

def Lvl2(ventana):
    ventana.fill(NEGRO)
    pygame.mixer.init(44100, -16, 2, 2048)
    archivo.read('Mapas/Level2.map')

    """Creacion del mundo"""
    j=0
    for fila in Mapa1:
        i=0
        for c in fila:
            type = string(archivo.get(c,'tipo'))
            px=int(archivo.get(c,'px'))
            py=int(archivo.get(c,'px'))
            col=int(archivo.get(c,'colision'))
            if col != 0:
                ventana.blit(Mundo1[px][py],[64*i,64*j])
            i+=1
        j+=1

    #fondojuego = pygame.image.load('carmap.png')
    #musica = pygame.mixer.Sound('sonidos/juego.wav')

    reloj = pygame.time.Clock()
    fin_juego = False
    fin = False
    #musica.play(-1)
    """Eventos"""
    while not fin and (not NextLvl):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fin = True
            if event.type ==pygame.KEYDOWN:
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    pass
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    pass
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    pass
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    pass


        #Dibujado
        ventana.fill(NEGRO)
        pygame.display.flip()
        reloj.tick(FPS)


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
        SelectWorld(ventana)

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
        SelectWorld(ventana)
    if (info_juego):
        InfoJuego(ventana)

def SelectWorld(ventana):
    ventana.fill(NEGRO)
    pygame.font.init()
    pygame.mixer.init(44100, -16, 2, 2048)
    fuente = pygame.font.Font(None, 40)
    #fondo  = pygame.image.load('images/fondo.png')
    #musica = pygame.mixer.Sound('sonidos/menu.wav')
    fin = False
    Tuto = False
    Lvl1 = False
    Lvl2 = False
    click = False
    #musica.play(-1)
    while (not fin) and (not Tuto) and (not Lvl1) and (not Lvl2):

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fin = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        #ventana.blit(fondo, [0,0])
        mx, my = pygame.mouse.get_pos()
        draw_text(Titulo, fuente, BLANCO, ventana, [300, 50])
        boton1 = pygame.Rect(300, 150, 220, 50)
        boton2 = pygame.Rect(300, 250, 220, 50)
        boton3 = pygame.Rect(300, 350, 220, 50)

        if boton1.collidepoint((mx, my)):
            if click:
                Tuto = True
        if boton2.collidepoint((mx, my)):
            if click:
                Lvl1 = True
        if boton3.collidepoint((mx, my)):
            if click:
                Lvl2 = True

        pygame.draw.rect(ventana, LIGHT_PINK, boton1)
        draw_text('Tutorial', fuente, BLANCO, ventana, [370, 160])
        pygame.draw.rect(ventana, LIGHT_PINK, boton2)
        draw_text('Nivel 1', fuente, BLANCO, ventana, [370, 260])
        pygame.draw.rect(ventana, LIGHT_PINK, boton3)
        draw_text('Nivel 2', fuente, BLANCO, ventana, [370, 360])

        click = False

    #musica.stop()
    if (Tuto==True):
        Tutorial(ventana)
    elif (Lvl1 == True):
        Lvl1(ventana)
    elif (Lvl2 == True):
        Lvl2(ventana)

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
        SelectWorld(ventana)

if __name__ == '__main__':
    ventana = pygame.display.set_mode([ANCHO,ALTO])
    pygame.display.set_caption(Titulo)
    #pygame.display.set_icon(pygame.image.load(''))
    """                       MENU                                        """

    Menu(ventana)
