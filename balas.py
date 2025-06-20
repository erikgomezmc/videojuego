import pygame
from controlador.config import SONIDO_EXPLOSION
from explosion import Explosion

class Balas(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/bullet.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
    #crea las balas de la nave del jugador

    def update(self, grupo_aliens, grupo_explosiones):
        self.rect.y -= 5
        #mueve el proyectil hacia arriba
        if self.rect.bottom < 0:
            self.kill()
        if pygame.sprite.spritecollide(self, grupo_aliens, True):
            self.kill()
            SONIDO_EXPLOSION.play()
            explosion = Explosion(self.rect.centerx, self.rect.centery, 2)
            grupo_explosiones.add(explosion)
    """esta funcion se encarga de detectar si la bala tiene contacto con alguna nave,
      si es asi emitira un sonido de xplosion, eliminara el alien, creara una onda 
      expasiva y eliminara el proyectil """