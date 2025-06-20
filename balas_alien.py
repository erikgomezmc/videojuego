import pygame
from controlador.config import ALTO_PANTALLA, SONIDO_EXPLOSION2
from explosion import Explosion

class BalasAlien(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/alien_bullet.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
    """creacion de balas de las naves """

    def update(self, grupo_nave, nave_espacial, grupo_explosiones):
        self.rect.y += 2
        #mueve los proyectiles hacia abajo
        if self.rect.top > ALTO_PANTALLA:
            self.kill()
        if pygame.sprite.spritecollide(self, grupo_nave, False, pygame.sprite.collide_mask):
            self.kill()
            SONIDO_EXPLOSION2.play()
            # Reduce salud de la nave espacial
            nave_espacial.salud_restante -= 1
            explosion = Explosion(self.rect.centerx, self.rect.centery, 1)
            grupo_explosiones.add(explosion)