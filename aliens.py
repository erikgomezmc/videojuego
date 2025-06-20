import pygame
import random

class Aliens(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/alien" + str(random.randint(1, 5)) + ".png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.contador_movimiento = 0
        self.direccion_movimiento = 1
    """esto se encarga de crear las naves alienigenas"""

    def update(self):
        self.rect.x += self.direccion_movimiento
        self.contador_movimiento += 1
        if abs(self.contador_movimiento) > 75:
            self.direccion_movimiento *= -1
            self.contador_movimiento *= self.direccion_movimiento

    """esta funcion es la encargada de que las naves aliemigenas se muevan"""