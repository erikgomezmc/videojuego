import pygame
from pygame import mixer

# Inicialización de pygame
pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()

# Configuración de la pantalla
ANCHO_PANTALLA = 600
ALTO_PANTALLA = 800
FPS = 60

# Configuración del juego
FILAS = 5
COLUMNAS = 5
TIEMPO_ESPERA_ALIEN = 1000  # tiempo de espera de bala en milisegundos

# Colores
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
BLANCO = (255, 255, 255)

# Fuentes
FUENTE30 = pygame.font.SysFont('Constantia', 30)
FUENTE40 = pygame.font.SysFont('Constantia', 40)

# Cargar sonidos
SONIDO_EXPLOSION = pygame.mixer.Sound("img/explosion.wav")
SONIDO_EXPLOSION.set_volume(0.25)

SONIDO_EXPLOSION2 = pygame.mixer.Sound("img/explosion2.wav")
SONIDO_EXPLOSION2.set_volume(0.25)

SONIDO_LASER = pygame.mixer.Sound("img/laser.wav")
SONIDO_LASER.set_volume(0.25)

# Cargar imagen de fondo
FONDO = pygame.image.load("img/bg.png")