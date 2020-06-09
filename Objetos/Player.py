import pygame
ROJO=[255,0,0]
class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.animacion = 0
        self.dir = 1
        #self.image = DIR[self.animacion]
        self.image = pygame.Surface([40,40])
        self.image.fill(ROJO)
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = ALTO/2
        self.velx = 0
        self.vely = 0
        self.rapidez = 5
        self.temp = 0
        self.impacto = False

        #Modificadores

        # De vida
        #incremento de vida
        self.vida = 3

        #inmunidadad
        self.inmunidad = False
        self.temp_inmunidad = 0

        #modificadores de movimiento
        self.lentitud = False
        self.temp_lentitud = 0

        self.impacto = False
        self.temp_impacto = 0

        self.muerto = False

        self.puntaje = 0

    def update(self):
        self.rect.x += self.velx
        self.rect.y+=self.vely
