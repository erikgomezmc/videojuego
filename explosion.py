import pygame

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, tamaño):
        pygame.sprite.Sprite.__init__(self)
        self.imagenes = []
        for num in range(1, 6):
            img = pygame.image.load(f"img/exp{num}.png")
            if tamaño == 1:
                img = pygame.transform.scale(img, (20, 20))
            if tamaño == 2:
                img = pygame.transform.scale(img, (40, 40))
            if tamaño == 3:
                img = pygame.transform.scale(img, (160, 160))
            # Agregar la imagen a la lista
            self.imagenes.append(img)
        self.indice = 0
        self.image = self.imagenes[self.indice]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.contador = 0

    def update(self):
        velocidad_explosion = 3
        # Actualizar animación de explosión
        self.contador += 1

        if self.contador >= velocidad_explosion and self.indice < len(self.imagenes) - 1:
            self.contador = 0
            self.indice += 1
            self.image = self.imagenes[self.indice]

        # Si la animación está completa, eliminar explosión
        if self.indice >= len(self.imagenes) - 1 and self.contador >= velocidad_explosion:
            self.kill()