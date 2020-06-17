import pygame
"""             Constantes                      """
Titulo = 'Un nombre mamado'
ANCHO = 960
ALTO = 640
FPS = 40
Limite_der = 700
Limite_iz = 420
Limite_arriba = 210
Limite_abajo = 490

#Colores
NEGRO=[0,0,0]
VERDE=[0,255,0]
ROJO=[255,0,0]
AMARILLO=[255,255,0]
DORADO = [212, 175, 55]
BLANCO=[255,255,255]
AZUL=[0,0,255]
LIGHT_ROJO = [255,55,55]
LIGHT_PINK = [212, 159, 183]

"""             Carga de Sprites Objetos            """
im_slime = pygame.image.load('Sprites/slime.png')
im_j = []
for j in range(6):
    fila = []
    for c in range(9):
        cuadro = im_slime.subsurface(128*c, 128*j, 128, 128)
        fila.append(cuadro)
    im_j.append(fila)

im_espada = pygame.image.load('Sprites/Espada.png')
im_es = []
for j in range(2):
    fila = []
    for c in range(5):
        cuadro = im_espada.subsurface(64*c, 128*j, 64, 128)
        fila.append(cuadro)
    im_es.append(fila)

"""             Carga de mundos                     """

Mundo = []
#carga de imagen
"""
img_textura = pygame.image.load('Sprites/lvl.png')
for j in range(12):
    fila = []
    for i in range(32):
        cuadro = img_textura.subsurface(i*64,j*64,64,64)
        fila.append(cuadro)
    Mundo.append(fila)
"""

"""             Funciones cracks                """
def draw_text(msj, font, color, surface, cord):
    object = font.render(msj, True, color)
    surface.blit(object, cord)

def draw_Mundo1(ventana):
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
