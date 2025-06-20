import pygame
from controlador.config import FONDO, FUENTE30

def mostrar_texto(pantalla, texto, fuente, color, x, y):
    img = fuente.render(texto, True, color)
    pantalla.blit(img, (x, y))

def mostrar_texto_centrado(pantalla, texto, fuente, color, y):
    ancho_ventana = pantalla.get_width()
    img = fuente.render(texto, True, color)
    x = (ancho_ventana - img.get_width()) // 2
    pantalla.blit(img, (x, y))

def input_box(pantalla, fuente, prompt, x, y, ancho=350, alto=50, password=False):
    clock = pygame.time.Clock()
    input_rect = pygame.Rect(x, y, ancho, alto)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = True
    texto = ''
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    active = True
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        done = True
                    elif event.key == pygame.K_BACKSPACE:
                        texto = texto[:-1]
                    else:
                        if len(texto) < 20:
                            texto += event.unicode

        pantalla.blit(FONDO, (0, 0))
        mostrar_texto_centrado(pantalla, prompt, fuente, (255,255,255), y-60)
        display_text = '*'*len(texto) if password else texto
        txt_surface = fuente.render(display_text, True, color)
        pantalla.blit(txt_surface, (input_rect.x+5, input_rect.y+5))
        pygame.draw.rect(pantalla, color, input_rect, 2)
        pygame.display.flip()
        clock.tick(30)
    return texto

def mostrar_mensaje(pantalla, mensaje, fuente, color, y, tiempo=1500):
    pantalla.blit(FONDO, (0, 0))
    mostrar_texto_centrado(pantalla, mensaje, fuente, color, y)
    pygame.display.flip()
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start_time < tiempo:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        clock.tick(60)

def menu_botones(pantalla, fuente, opciones, y_inicial, espacio=70):
    clock = pygame.time.Clock()
    seleccion = 0
    while True:
        pantalla.blit(FONDO, (0, 0))
        for i, texto in enumerate(opciones):
            color = (255,255,0) if i == seleccion else (255,255,255)
            mostrar_texto_centrado(pantalla, texto, fuente, color, y_inicial + i*espacio)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    seleccion = (seleccion - 1) % len(opciones)
                if event.key == pygame.K_DOWN:
                    seleccion = (seleccion + 1) % len(opciones)
                if event.key == pygame.K_RETURN:
                    return seleccion
        clock.tick(20)

def mostrar_tabla_puntajes(pantalla, fuente, db, y_inicial):
    pantalla.blit(FONDO, (0, 0))
    mostrar_texto_centrado(pantalla, "Tabla de Puntajes", fuente, (255,255,255), y_inicial)
    puntajes = db.obtener_top_puntajes()
    y = y_inicial + 60
    fuente_tabla = FUENTE30  # Fuente más pequeña para la tabla
    for i, (nombre, puntaje, fecha) in enumerate(puntajes):
        texto = f"{i+1}. {nombre[:12]:<12} - {puntaje}   ({fecha})"
        mostrar_texto_centrado(pantalla, texto, fuente_tabla, (255,255,255), y)
        y += 38
        if y > pantalla.get_height() - 80:
            break
    mostrar_texto_centrado(pantalla, "Presiona cualquier tecla para volver", fuente_tabla, (200,200,200), pantalla.get_height() - 60)
    pygame.display.flip()
    esperando = True
    while esperando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                esperando = False

def menu_post_juego(pantalla, fuente, usuario):
    opciones = ["Jugar de nuevo", "Cerrar sesión y ver tabla de puntajes"]
    return menu_botones(pantalla, fuente, opciones, pantalla.get_height()//2 - 60)