import pygame

class Suelo(pygame.sprite.Sprite):
    def __init__(self, pos, img):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
