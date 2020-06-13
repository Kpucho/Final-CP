"""             Constantes                      """
Titulo = 'Un nombre mamado'
ANCHO = 960
ALTO = 640
FPS = 40

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

"""             Carga de mundos                 """
Mundo1 = []
#carga de imagen
img_textura = pygame.image.load('Sprites/lvl.png')
for j in range(12):
    fila = []
    for i in range(32):
        cuadro = img_textura.subsurface(i*64,j*64,64,64)
        fila.append(cuadro)
    Mundo1.append(fila)

archivo.read('Level1.map')
Mapa1 = archivo.get('info','mapa').split('\n')

"""             Funciones cracks                """
def draw_text(msj, font, color, surface, cord):
    object = font.render(msj, True, color)
    surface.blit(object, cord)

def draw_Mundo1(ventana):
    j=0
    for fila in Mapa1:
        i=0
        for c in fila:
            px=int(archivo.get(c,'px'))
            py=int(archivo.get(c,'px'))
            col=int(archivo.get(c,'colision'))
            if col != 0:
                ventana.blit(m[px][py],[32*i,32*j])
            i+=1
        j+=1
