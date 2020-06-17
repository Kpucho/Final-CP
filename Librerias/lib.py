import pygame
"""             Constantes                      """
ANCHO = 1024
ALTO = 640

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

FPS = 40


im_modificadores = pygame.image.load('Sprites/modificadores.png')
MODIFI = []
for c in range(3):
    cuadro=im_modificadores.subsurface(64*c,0,64,64)
    MODIFI.append(cuadro)

Titulo = 'Un nombre mamado'

"""             Funciones cracks                """
def draw_text(msj, font, color, surface, cord):
    object = font.render(msj, True, color)
    surface.blit(object, cord)
