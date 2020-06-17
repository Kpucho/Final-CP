import pygame
import random
import ConfigParser
from Librerias.lib import *
from Librerias.Enemy import *

#  ################
#  ................

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
        self.techo = False
        self.piso = False
        self.der = False
        self.izq = False
        self.plataformas = None
        self.damage = 3
        self.retroceso = False
        self.correccionx = 0
        self.correcciony = 0
        self.puntene = 0
        self.vida = 8
        self.tiempo = 0
        self.inmunidad = False
        self.temp_inmunidad = 0

    def lateral_der(self):
        return self.rect.right
    def lateral_izq(self):
        return self.rect.left

    def gravedad(self, g = 1):
        if self.vely == 0:
            self.vely = g
        else:
            # print 'bajada'
            self.vely += g

    def detectarPiso(self):
        print self.vely
        self.rect.y += (self.vely + 1)
        lista = pygame.sprite.spritecollide(self, self.plataformas, False)
        suelo = False

        for p in lista:
            if self.vely >= 0:
                if self.rect.bottom > p.rect.top:
                    suelo = True
        self.rect.y -= (self.vely + 1)
        return suelo

    def update(self, plataformas):

        self.plataformas = plataformas
        # self.rect.x += self.velx
        ls_pla = pygame.sprite.spritecollide(self, self.plataformas, False)

        for p in ls_pla:
            if self.velx > 0:
                if self.rect.right > p.rect.left:

                    self.correccionx = p.rect.left - self.rect.right

                    # print 'correcion x der -', self.correccionx
                    # print 'objeto', p.rect.left
                    # print 'jugador', self.rect.right

                    # self.rect.right = p.rect.left
                    self.velx = 0
            elif self.rect.left < p.rect.right and self.velx!= 0:
                self.correccionx = p.rect.right - self.rect.left
                # print 'correcion x izq -',self.correccionx
                # self.rect.left = p.rect.right
                self.velx = 0



        # self.rect.y+=self.vely


        #Corregir luego
        if self.detectarPiso():
            self.piso = True
            if self.accion != 0 and self.accion != 1:
                self.velx = 0
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
                    self.correcciony = p.rect.top - self.rect.bottom
                    # print 'corre y abajo', self.correcciony
                    # self.rect.bottom = p.rect.top
                    self.vely = 0
                    if self.accion == 2:
                        self.accion = 0
                    elif self.accion == 3:
                        self.accion = 1
            elif self.rect.top < p.rect.bottom and self.vely!= 0:
                self.correcciony = p.rect.bottom - self.rect.top
                # print 'corre y arriba', self.correcciony
                # self.rect.top = p.rect.bottom
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

        self.tiempo += 1

        if self.inmunidad and self.temp_inmunidad > 0:
            self.temp_inmunidad -= 1
        elif self.inmunidad and self.temp_inmunidad <= 0:
            self.inmunidad = False

        #Cambio de sprite
        self.image = self.m[self.accion][self.cont]

    def quitar_vida(self):
        if not self.inmunidad:
            # pygame.mixer.Channel(1).play(pygame.mixer.Sound('sonidos/efectos/choque.wav'))
            self.vida -= 1
            self.inmunidad = True
            self.temp_inmunidad = 3 * FPS

    def info_jugador(self):
        for v in range(self.vida + 1):
            if self.inmunidad == False:
                ventana.blit(MODIFI[0],[10+64*v,10])
            elif self.inmunidad == True:
                ventana.blit(MODIFI[2],[10+64*v,10])
        fuente = pygame.font.Font(None, 40)
        draw_text('Puntaje: ' + str(self.tiempo/FPS), fuente, ROJO, ventana, [10, 80])


class Modificador(pygame.sprite.Sprite):

    def __init__(self, pos, type):
        pygame.sprite.Sprite.__init__(self)
        #tipo 0 es vida
        #tipo 1 es x2
        #tipo 2 es inmunidadad
        #tipo 3 es vivacidad
        #tipo 4 es lentitud
        self.tipo = type
        #self.color = [VERDE, DORADO, BLANCO, ROJO, AZUL]
        self.image = MODIFI[self.tipo]
        #self.image = pygame.Surface([32,32])
        #self.image.fill(self.color[self.tipo])

        # self.image = pygame.image.load('images/sprites/obstaculos.png')
        # self.image = self.image.subsurface(0, 530, 80, 115)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.velx = 0
        self.vely = 0

    def update(self, fondovel):
        self.rect.x += fondovel[0]
        self.rect.y += fondovel[1]


class Plataforma(pygame.sprite.Sprite):
    def __init__(self, pos, m, tipo = 0):
        pygame.sprite.Sprite.__init__(self)
        # self.image = pygame.Surface(dim)
        # self.image.fill(VERDE)
        self.tipo = tipo
        self.image = m
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.velx = 0
        self.vely = 0
    def update(self, fondovel):

        self.rect.x += fondovel[0]
        self.rect.y += fondovel[1]


class Golpe(pygame.sprite.Sprite):
    def __init__(self, pos, me, damage = 3):
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

    def update(self, fondovel):
        self.rect.x += fondovel[0]
        self.rect.y += fondovel[1]

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

    def update(self, fondovel):

        self.rect.x += self.velx + fondovel[0]
        self.rect.y += self.vely + fondovel[1]

class Bola(pygame.sprite.Sprite):
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
    #Creacion de grupos
    jugadores = pygame.sprite.Group()
    plataformas = pygame.sprite.Group()
    espadazos = pygame.sprite.Group()
    golpesjefe1 = pygame.sprite.Group()
    enemigos1 = pygame.sprite.Group()
    enemigos2 = pygame.sprite.Group()
    enemigosEst1 = pygame.sprite.Group()
    enemigosEst2 = pygame.sprite.Group()
    modificadores = pygame.sprite.Group()
    jefes1 = pygame.sprite.Group()
    balas_ene = pygame.sprite.Group()

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



    velfondo = [0,0]
    #fondojuego = pygame.image.load('carmap.png')
    archivo = ConfigParser.ConfigParser()
    archivo.read('Mapas/level1.map')
    #carga de texturas
    archivo_text = archivo.get('info', 'texturas')
    img_textura = pygame.image.load(archivo_text)
    img_textura2 = pygame.image.load('Sprites/pinchos.png')
    cuadro = img_textura.subsurface(0, 0, 64, 64)
    pinchos = img_textura2.subsurface(0, 0, 64, 64)
    #
    # m = []
    # for j in range(12):
    #     fila = []
    #     for i in range(32):
    #         cuadro = img_textura.subsurface(i*32, j*32, 32, 32)
    #         fila.append(cuadro)
    #     m.append(fila)

    info_mapa = archivo.get('info', 'mapa')
    mapa = info_mapa.split('\n')
    j = 0
    for f in mapa:
        # print f
        i = 0
        for c in f:
            # print c, archivo.get(c, 'tf'), archivo.get(c, 'tc'), 32*i, 32*j
            tf = int(archivo.get(c, 'tf'))
            tc = int(archivo.get(c, 'tc'))
            col = int(archivo.get(c, 'colision'))
            #Tipos de plataforma
            if col > 0:
                # ventana.blit(m[tf][tc], [32*i, 32*j])
                tipo = int(archivo.get(c, 'ty'))
                if tipo == 1:
                    p = Plataforma([64*i, 64*j],cuadro)
                    plataformas.add(p)
                elif tipo == 2:
                    p = Plataforma([64*i, 64*j],pinchos)
                    plataformas.add(p)
                elif tipo == 4:
                    mod = Modificador([64*i, 64*j], 1)
                    modificadores.add(mod)
                elif tipo == 5:
                    mod = Modificador([64*i, 64*j], 2)
                    modificadores.add(mod)
            i+=1
        j+=1



    # Musica
    # pygame.mixer.init(44100, -16, 2, 2048)
    #musica = pygame.mixer.Sound('sonidos/juego.wav')




    j = Jugador([ANCHO/2, ALTO/2], m)
    jugadores.add(j)
    j.plataformas = plataformas

    # p = Plataforma([200, 300],[100, 50])
    # plataformas.add(p)
    #
    # p = Plataforma([500, 300],[100, 50])
    # plataformas.add(p)
    #
    # p = Plataforma([0, 576],[1024, 64])
    # plataformas.add(p)
    #
    # p = Plataforma([832, 512],[192, 64])
    # plataformas.add(p)
    #
    # p = Plataforma([0, 512],[64, 64])
    # plataformas.add(p)
    #
    # p = Plataforma([960, 448],[64, 64])
    # plataformas.add(p)

    eneEst1 = EnemigoEst1([2560, 1088], [64,64], plataformas)
    enemigosEst1.add(eneEst1)

    eneEst1 = EnemigoEst1([3520, 1024], [64, 64], plataformas)
    enemigosEst1.add(eneEst1)

    eneEst2 = EnemigoEst2([832, 64], [64, 64], plataformas)
    enemigosEst2.add(eneEst2)

    eneEst2 = EnemigoEst2([1536, 64], [64, 64], plataformas, 550)
    enemigosEst2.add(eneEst2)

    eneEst2 = EnemigoEst2([1728, 640], [64, 64], plataformas)
    enemigosEst2.add(eneEst2)

    # boss = Jefe1([512, 200], [128, 128], plataformas)
    # jefes1.add(boss)




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
                    print 'salto'
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
                ene2.posxjugador = ANCHO/2
            elif pygame.sprite.collide_circle(ene2,j):
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

        for eneEst2 in enemigosEst2:

            if pygame.sprite.collide_circle(eneEst2,j):
                eneEst2.alerta = True
            if not eneEst2.ataque:
                eneEst2.ataque = True
                #rebona al disparar
                eneEst2.vely = -5

                #Bala izq
                bala_e = Bala(eneEst2.get_poscentro())
                bala_e.velx = -5
                balas_ene.add(bala_e)
                #Bala der
                bala_e = Bala(eneEst2.get_poscentro())
                bala_e.velx = 5
                balas_ene.add(bala_e)

        for jefe in jefes1:
            if jefe.alerta:
                jefe.posxjugador = j.rect.centerx
                if jefe.poder and (jefe.podercont >= 10*FPS):
                    if jefe.accion == 0:
                        jefe.accion = 3
                        jefe.cont = 0
                        golpejefe = Golpe([jefe.lateral_der(), jefe.rect.y], me)
                        golpejefe.accion = 0
                        golpesjefe1.add(golpejefe)
                    elif jefe.accion == 1:
                        jefe.accion = 4
                        jefe.cont = 0
                        golpejefe = Golpe([jefe.lateral_izq() - 64, jefe.rect.y], me)
                        golpejefe.accion = 1
                        golpesjefe1.add(golpejefe)
                    jefe.poder = False
                    jefe.podercont = 0
            elif pygame.sprite.collide_circle(jefe,j):
                jefe.alerta = True

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
                enemigo.life -= j.damage
                if enemigo.life <= 0:
                    enemigosEst1.remove(enemigo)

            ls_ene2 = pygame.sprite.spritecollide(espada, enemigosEst2, False)

            for enemigo in ls_ene2:
                enemigo.life -= j.damage
                if enemigo.life <= 0:
                    enemigosEst2.remove(enemigo)

        #Eliminacion del golpe del jugador
        for espada in espadazos:
            if espada.fin:
                if j.accion == 4:
                    j.accion = 0
                elif j.accion == 5:
                    j.accion = 1
                espadazos.remove(espada)

        ls_mod = ls_ene2 = pygame.sprite.spritecollide(j, modificadores, False)

        for mod in ls_mod:
            if mod.tipo == 1:
                j.damage += 100
                modificadores.remove(mod)
            if mod.tipo == 2:
                j. inmunidad = True
                j.temp_inmunidad = 5*FPS
                modificadores.remove(mod)


        # print j.correccionx
        # print j.correcciony
        if j.correccionx == 0 and j.correcciony == 0:
            velfondo = [ -j.velx , - j.vely]
        if j.correccionx != 0:
            # print 'corrige x'
            velfondo[0] =  -j.correccionx
            j.correccionx = 0
            # print 'corrige y'
        if j.correcciony != 0:
            velfondo[1] = - j.correcciony
            j.correcciony = 0

        # print 'x: ',velfondo[0]
        # print 'y: ', velfondo[1]

        #Refresco
        plataformas.update(velfondo)
        jugadores.update(plataformas)
        espadazos.update(velfondo)
        enemigos1.update(plataformas, velfondo)
        enemigosEst1.update(plataformas, velfondo)
        enemigosEst2.update(plataformas, velfondo)
        enemigos2.update()
        jefes1.update(plataformas, velfondo)
        golpesjefe1.update(velfondo)
        balas_ene.update(velfondo)
        modificadores.update(velfondo)


        ventana.fill(NEGRO)
        plataformas.draw(ventana)
        enemigos1.draw(ventana)
        enemigosEst1.draw(ventana)
        enemigosEst2.draw(ventana)
        enemigos2.draw(ventana)
        jefes1.draw(ventana)
        golpesjefe1.draw(ventana)
        jugadores.draw(ventana)
        modificadores.draw(ventana)
        balas_ene.draw(ventana)
        espadazos.draw(ventana)
        j.info_jugador()

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
