import pygame
import random
import ConfigParser
from lib import *
from Objetos.Player import *
from Objetos.Plataforma import *
from Objetos.Enemys_moviles import *
from Objetos.Enemys_Est import *
from Objetos.Etc import *


"""             Validadores de nivel            """
Free_Tutorial = False
Free_Nivel1 = False
Free_Nivel2 = False

def Draw_World(archivo, Plataformas, Jugadores, Enemys_Est1, Enemys_Est2, Enemys_Movil1, Enemys_Movil2):
    Mapa1 = archivo.get('info','mapa').split('\n')
    M_limite = 0
    j=0
    for fila in Mapa1:
        i=0
        for c in fila:
            type = archivo.get(c,'tipo')
            col=int(archivo.get(c,'colision'))
            if col != 0:
                if (type == 'Muro'):
                    #Objeto = Plataforma([64*i,64*j],Mundo1[px][py])
                    Objeto = Plataforma([64*i,64*j],'m')
                    Plataformas.add(Objeto)
                elif (type == 'Suelo'):
                    #Objeto = Suelo([64*i,64*j],Mundo1[px][py])
                    Objeto = Plataforma([64*i,64*j],'s')
                    Plataformas.add(Objeto)
                elif (type == 'Plataforma'):
                    #Objeto = Plataforma([64*i,64*j],Mundo1[px][py])
                    Objeto = Plataforma([64*i,64*j],'p')
                    Plataformas.add(Objeto)
                elif (type == 'Jugador'):
                    J = Player([64*i,64*j], im_j)
                    Jugadores.add(J)
                elif (type == 'Es1'):
                    E = Enemy_Est1([64*i,64*j],[64,64])
                    Enemys_Est1.add(E)
                elif (type == 'Es2'):
                    E = Enemy_Est2([64*i,64*j],[64,64])
                    Enemys_Est2.add(E)
                elif (type == 'Em1'):
                    E = Enemy_Movil1([64*i,64*j],[64,64])
                    Enemys_Movil1.add(E)
                elif (type == 'Em2'):
                    E = Enemy_Movil2([64*i,64*j],[64,64])
                    Enemys_Movil2.add(E)
            i+=1
        M_Limite = i
        j+=1
    return (M_Limite*64)

def PLAY(ventana):
    ventana.fill(NEGRO)
    pygame.mixer.init(44100, -16, 2, 2048)
    archivo = ConfigParser.ConfigParser()

    if Free_Tutorial == False:
        archivo.read('Mapas/Tutorial.map')
    elif Free_Nivel1 == False:
        archivo.read('Mapas/Level1.map')
    elif Free_Nivel2 == False:
        archivo.read('Mapas/Level2.map')
    else:
        """GANA"""

    J = None
    Plataformas = pygame.sprite.Group()
    Jugadores = pygame.sprite.Group()
    espadazos = pygame.sprite.Group()
    Enemys_Movil1 = pygame.sprite.Group()
    Enemys_Movil2 = pygame.sprite.Group()
    Enemys_Est1 = pygame.sprite.Group()
    Enemys_Est2 = pygame.sprite.Group()

    Balas_ene = pygame.sprite.Group()
    Mundo_posx = 0
    Mundo_velx = 0

    """Creacion del mundo"""
    Mundo_Limite_der = Draw_World(archivo, Plataformas, Jugadores, Enemys_Est1, Enemys_Est2, Enemys_Movil1, Enemys_Movil2)

    Mundo_Limite_der = ANCHO - Mundo_Limite_der

    for jugador in Jugadores:
        J = jugador
        J.plataformas = Plataformas

    for E in Enemys_Movil1:
        E.plataformas = Plataformas

    for E in Enemys_Movil2:
        E.plataformas = Plataformas

    for E in Enemys_Est1:
        E.plataformas = Plataformas

    for E in Enemys_Est2:
        E.plataformas = Plataformas

    #fondojuego = pygame.image.load('carmap.png')
    #musica = pygame.mixer.Sound('sonidos/juego.wav')

    reloj = pygame.time.Clock()
    NextLvl= False
    fin = False
    #musica.play(-1)
    """Eventos"""
    while not fin and (not NextLvl):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fin = True
            if event.type ==pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    J.velx = 10
                    if not J.piso:
                        J.accion = 2
                    else:
                        J.vely = 0
                        J.accion = 0
                    J.cont = 0
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    J.velx = -10
                    if not J.piso:
                        J.accion = 3
                    else:
                        J.vely = 0
                        J.accion = 1
                    J.cont = 0
                if event.key == pygame.K_SPACE:
                    J.vely = -10
                    J.piso = False
                    if J.accion == 0:
                        J.accion = 2
                    elif J.accion == 1:
                        J.accion = 3
                    J.cont = 0
                if event.key == pygame.K_f:
                    if J.accion == 0:
                        J.accion = 4
                        J.cont = 0
                        espada = Golpe([J.lateral_der(), J.rect.y], im_es)
                        espada.accion = 0
                        espadazos.add(espada)
                    elif J.accion == 1:
                        J.accion = 5
                        J.cont = 0
                        espada = Golpe([J.lateral_izq() - 64, J.rect.y], im_es)
                        espada.accion = 1
                        espadazos.add(espada)
            if event.type == pygame.KEYUP:
                J.velx = 0

#control
        #Mov Mundo
        if J.velx > 0:
            if J.rect.x > Limite_der:
                J.rect.x = Limite_der
                if Mundo_posx > (Mundo_Limite_der):
                    Mundo_velx = -4
                else:
                    Mundo_velx = 0
            else:
                Mundo_velx = 0

        if J.velx < 0:
            if J.rect.x < Limite_iz:
                J.rect.x = Limite_iz
                if Mundo_posx > 0:
                    Mundo_velx = 4
                else:
                    Mundo_velx = 0
            else:
                Mundo_velx = 0

        # Deteccion de cercania
        # if pygame.sprite.collide_circle(r,j):
        #     print 'cerca', r.id

        #Actualizacion de pos del jugador para los enemigos
        #Colisiones radiales
        for ene2 in Enemys_Movil2:
            if ene2.alerta:
                ene2.posxjugador = J.rect.centerx
            elif pygame.sprite.collide_circle(ene2,J):
                print 'Alerta'
                ene2.alerta = True

        #SECCION DE CREACCION

        #crear balas enemigas de ciertos enemigos
        #Crea las balas del enemigo estacionario de nivel 1
        for eneEst1 in Enemys_Est1:
            if not eneEst1.ataque:
                eneEst1.ataque = True
                #Bala izq
                bala_e = Bala(eneEst1.get_poscentro())
                bala_e.velx = -5
                Balas_ene.add(bala_e)
                #Bala der
                bala_e = Bala(eneEst1.get_poscentro())
                bala_e.velx = 5
                Balas_ene.add(bala_e)
                #Bala superior
                bala_e = Bala(eneEst1.get_poscentro())
                bala_e.vely = -5
                Balas_ene.add(bala_e)

        for eneEst2 in Enemys_Est2:

            if pygame.sprite.collide_circle(eneEst2,j):
                eneEst2.alerta = True
            if not eneEst2.ataque:
                eneEst2.ataque = True
                #rebona al disparar
                eneEst2.vely = -5

                #Bala izq
                bala_e = Bala(eneEst2.get_poscentro())
                bala_e.velx = -5
                Balas_ene.add(bala_e)
                #Bala der
                bala_e = Bala(eneEst2.get_poscentro())
                bala_e.velx = 5
                Balas_ene.add(bala_e)

        #SECCION DE ELIMINACION
        #Eliminacion de balas con las paredes y fuera de area:
        for bala in Balas_ene:
            if pygame.sprite.spritecollide(bala, Plataformas, False):
                Balas_ene.remove(bala)
            elif pygame.sprite.spritecollide(bala, Jugadores, False):
                # Bajar vida al jugador

                #Retroceso del golpe
                J.retroceso = True
                if bala.velx > 0:
                    J.velx = 50
                else:
                    J.velx = -50
                Balas_ene.remove(bala)
            elif pygame.sprite.spritecollide(bala, espadazos, False):
                Balas_ene.remove(bala)
            elif bala.rect.y < -50 or bala.rect.y > (ALTO + 50):
                Balas_ene.remove(bala)
            elif bala.rect.x < -50 or bala.rect.x > (ANCHO + 50):
                Balas_ene.remove(bala)


        #Eliminacion del enemigo por el espadazo por 1
        for espada in espadazos:
            ls_ene = pygame.sprite.spritecollide(espada, Enemys_Movil1, False)
            for enemigo in ls_ene:
                Enemys_Movil1.remove(enemigo)

        for espada in espadazos:
            ls_ene = pygame.sprite.spritecollide(espada, Enemys_Est1, False)
            for enemigo in ls_ene:
                Enemys_Est1.remove(enemigo)

        #Eliminacion del golpe del jugador
        for espada in espadazos:
            if espada.fin:
                if J.accion == 4:
                    J.accion = 0
                elif J.accion == 5:
                    J.accion = 1
                espadazos.remove(espada)

        #Refresco de las plataformas para movs
        J.plataformas = Plataformas

        for E in Enemys_Movil1:
            E.plataformas = Plataformas

        for E in Enemys_Movil2:
            E.plataformas = Plataformas

        for E in Enemys_Est1:
            E.plataformas = Plataformas

        for E in Enemys_Est2:
            E.plataformas = Plataformas

        #Refresco
        Plataformas.update(Mundo_velx)
        Jugadores.update()
        espadazos.update()
        Enemys_Movil1.update(Mundo_velx)
        Enemys_Est1.update(Mundo_velx)
        Enemys_Est2.update(Mundo_velx)
        Enemys_Movil2.update(Mundo_velx)
        Balas_ene.update()
        Mundo_posx+=Mundo_velx

        #Dibujado
        ventana.fill(NEGRO)
        Plataformas.draw(ventana)
        Enemys_Movil1.draw(ventana)
        Enemys_Est1.draw(ventana)
        Enemys_Est2.draw(ventana)
        Enemys_Movil2.draw(ventana)
        Jugadores.draw(ventana)
        Balas_ene.draw(ventana)
        espadazos.draw(ventana)

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
        draw_text(Titulo, fuente, BLANCO, ventana, [300, 50])
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
        PLAY(ventana)
    elif (Lvl1 == True):
        Free_Tutorial = True
        PLAY(ventana)
    elif (Lvl2 == True):
        Free_Tutorial = True
        Free_Nivel1 = True
        PLAY(ventana)

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
