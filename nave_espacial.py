import pygame
from controlador.config import ANCHO_PANTALLA, ROJO, VERDE, SONIDO_LASER
from balas import Balas
from explosion import Explosion

class NaveEspacial(pygame.sprite.Sprite):
    def __init__(self, x, y, salud):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/spaceship.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.salud_inicial = salud
        self.salud_restante = salud
        self.ultimo_disparo = pygame.time.get_ticks()

    def update(self, pantalla, grupo_balas, grupo_explosiones):
        # Establecer velocidad de movimiento
        velocidad = 8
        # Establecer variable de tiempo de espera
        tiempo_espera = 500  # milisegundos
        juego_terminado = 0

        # Obtener tecla presionada
        tecla = pygame.key.get_pressed()
        if tecla[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= velocidad
        if tecla[pygame.K_RIGHT] and self.rect.right < ANCHO_PANTALLA:
            self.rect.x += velocidad

        # Registrar tiempo actual
        tiempo_actual = pygame.time.get_ticks()
        # Disparar
        if tecla[pygame.K_SPACE] and tiempo_actual - self.ultimo_disparo > tiempo_espera:
            SONIDO_LASER.play()
            bala = Balas(self.rect.centerx, self.rect.top)
            grupo_balas.add(bala)
            self.ultimo_disparo = tiempo_actual

        # Actualizar máscara
        self.mask = pygame.mask.from_surface(self.image)

        # Dibujar barra de salud
        pygame.draw.rect(pantalla, ROJO, (self.rect.x, (self.rect.bottom + 10), self.rect.width, 15))
        if self.salud_restante > 0:
            pygame.draw.rect(pantalla, VERDE, (self.rect.x, (self.rect.bottom + 10), 
                           int(self.rect.width * (self.salud_restante / self.salud_inicial)), 15))
        elif self.salud_restante <= 0:
            explosion = Explosion(self.rect.centerx, self.rect.centery, 3)
            grupo_explosiones.add(explosion)
            self.kill()
            juego_terminado = -1
        return juego_terminado