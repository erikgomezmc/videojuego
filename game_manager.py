import pygame
import random
from controlador.config import *
from nave_espacial import NaveEspacial
from aliens import Aliens
from balas_alien import BalasAlien

class GameManager:
    def __init__(self, usuario, db, pantalla):
        self.usuario = usuario
        self.db = db
        self.pantalla = pantalla
        pygame.display.set_caption('Space Invaders')
        self.reloj = pygame.time.Clock()
        
        # Variables del juego
        self.ultimo_disparo_alien = pygame.time.get_ticks()
        self.cuenta_regresiva = 3
        self.ultimo_conteo = pygame.time.get_ticks()
        self.juego_terminado = 0  # 0 no hay fin del juego, 1 significa que el jugador ganó, -1 significa que el jugador perdió
        
        # Crear grupos de sprites
        self.grupo_nave = pygame.sprite.Group()
        self.grupo_balas = pygame.sprite.Group()
        self.grupo_aliens = pygame.sprite.Group()
        self.grupo_balas_alien = pygame.sprite.Group()
        self.grupo_explosiones = pygame.sprite.Group()
        
        # Crear jugador
        self.nave_espacial = NaveEspacial(int(ANCHO_PANTALLA / 2), ALTO_PANTALLA - 100, 3)
        self.grupo_nave.add(self.nave_espacial)
        
        # Crear aliens
        self.crear_aliens()

    def dibujar_fondo(self):
        self.pantalla.blit(FONDO, (0, 0))

    def dibujar_texto(self, texto, fuente, color_texto, x, y):
        img = fuente.render(texto, True, color_texto)
        self.pantalla.blit(img, (x, y))

    def crear_aliens(self):
        # Generar aliens
        for fila in range(FILAS):
            for elemento in range(COLUMNAS):
                alien = Aliens(100 + elemento * 100, 100 + fila * 70)
                self.grupo_aliens.add(alien)

    def actualizar_balas(self):
        # Actualizar balas del jugador
        for bala in self.grupo_balas:
            bala.update(self.grupo_aliens, self.grupo_explosiones)
        
        # Actualizar balas de aliens
        for bala_alien in self.grupo_balas_alien:
            bala_alien.update(self.grupo_nave, self.nave_espacial, self.grupo_explosiones)

    def manejar_disparos_alien(self):
        # Crear balas alien aleatorias
        tiempo_actual = pygame.time.get_ticks()
        if (tiempo_actual - self.ultimo_disparo_alien > TIEMPO_ESPERA_ALIEN and 
            len(self.grupo_balas_alien) < 5 and len(self.grupo_aliens) > 0):
            alien_atacante = random.choice(self.grupo_aliens.sprites())
            bala_alien = BalasAlien(alien_atacante.rect.centerx, alien_atacante.rect.bottom)
            self.grupo_balas_alien.add(bala_alien)
            self.ultimo_disparo_alien = tiempo_actual

    def actualizar_juego(self):
        if self.cuenta_regresiva == 0:
            self.manejar_disparos_alien()
            
            # Verificar si todos los aliens han sido eliminados
            if len(self.grupo_aliens) == 0:
                self.juego_terminado = 1

            if self.juego_terminado == 0:
                # Actualizar nave espacial
                self.juego_terminado = self.nave_espacial.update(
                    self.pantalla, self.grupo_balas, self.grupo_explosiones
                )
                
                # Actualizar grupos de sprites
                self.actualizar_balas()
                self.grupo_aliens.update()
            else:
                if self.juego_terminado == -1:
                    self.dibujar_texto('¡JUEGO TERMINADO!', FUENTE40, BLANCO, 
                                     int(ANCHO_PANTALLA / 2 - 120), int(ALTO_PANTALLA / 2 + 50))
                

        # Manejar cuenta regresiva
        if self.cuenta_regresiva > 0:
            self.dibujar_texto('¡PREPÁRATE!', FUENTE40, BLANCO, 
                             int(ANCHO_PANTALLA / 2 - 100), int(ALTO_PANTALLA / 2 + 50))
            self.dibujar_texto(str(self.cuenta_regresiva), FUENTE40, BLANCO, 
                             int(ANCHO_PANTALLA / 2 - 10), int(ALTO_PANTALLA / 2 + 100))
            temporizador_conteo = pygame.time.get_ticks()
            if temporizador_conteo - self.ultimo_conteo > 1000:
                self.cuenta_regresiva -= 1
                self.ultimo_conteo = temporizador_conteo

    def dibujar(self):
        # Dibujar fondo
        self.dibujar_fondo()
        
        # Actualizar juego
        self.actualizar_juego()
        
        # Actualizar grupo de explosiones
        self.grupo_explosiones.update()
        
        # Dibujar grupos de sprites
        self.grupo_nave.draw(self.pantalla)
        self.grupo_balas.draw(self.pantalla)
        self.grupo_aliens.draw(self.pantalla)
        self.grupo_balas_alien.draw(self.pantalla)
        self.grupo_explosiones.draw(self.pantalla)

    def ejecutar(self):
        ejecutando = True
        resultado = None
        while ejecutando:
            self.reloj.tick(FPS)
            self.dibujar()
            pygame.display.flip()
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    return "cerrado"
            if self.juego_terminado == 1:
                puntaje = FILAS * COLUMNAS * 500
                self.db.registrar_puntaje(self.usuario, puntaje)
                self.dibujar_texto("¡GANASTE!", FUENTE40, BLANCO, ANCHO_PANTALLA//2 - 120, ALTO_PANTALLA//2)
                pygame.display.update()
                pygame.time.delay(2000)
                resultado = "victoria"
                ejecutando = False
            elif self.juego_terminado == -1:
                puntaje = (FILAS * COLUMNAS - len(self.grupo_aliens)) * 500
                self.db.registrar_puntaje(self.usuario, puntaje)
                self.dibujar_texto("¡JUEGO TERMINADO!", FUENTE40, BLANCO, ANCHO_PANTALLA//2 - 220, ALTO_PANTALLA//2)
                pygame.display.update()
                pygame.time.delay(2000)
                resultado = "derrota"
                ejecutando = False
        return resultado