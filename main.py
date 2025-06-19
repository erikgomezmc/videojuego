import pygame
from game_manager import GameManager
from modelo.db_manager import DBManager
from ui_forms import input_box, mostrar_mensaje, menu_botones, mostrar_tabla_puntajes, menu_post_juego
from controlador.config import ANCHO_PANTALLA, ALTO_PANTALLA, FUENTE40

def main():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
    pygame.display.set_caption("Space Invaders")
    db = DBManager()
    ejecutando = True

    while ejecutando:
        opcion = menu_botones(
            pantalla, FUENTE40,
            ["Nuevo Juego", "Registrarse", "Ver tabla de puntajes", "Salir"],
            200
        )
        if opcion is None or opcion == 3:
            ejecutando = False
        elif opcion == 0:  # Iniciar sesión
            usuario = input_box(pantalla, FUENTE40, "Usuario:", 120, 300)
            if usuario is None: break
            contrasena = input_box(pantalla, FUENTE40, "Contraseña:", 120, 400, password=True)
            if contrasena is None: break
            if db.verificar_login(usuario, contrasena):
                mostrar_mensaje(pantalla, "¡Inicio de sesión exitoso!", FUENTE40, (0,255,0), 500)
                while True:
                    juego = GameManager(usuario, db, pantalla)
                    resultado = juego.ejecutar()
                    if resultado == "cerrado":
                        ejecutando = False
                        break
                    post_opcion = menu_post_juego(pantalla, FUENTE40, usuario)
                    if post_opcion is None:
                        ejecutando = False
                        break
                    if post_opcion == 0:
                        continue  # Jugar de nuevo
                    elif post_opcion == 1:
                        mostrar_tabla_puntajes(pantalla, FUENTE40, db, 100)
                        break
                # Al cerrar sesión, vuelve al menú principal
            else:
                mostrar_mensaje(pantalla, "Usuario o contraseña incorrectos.", FUENTE40, (255,0,0), 500)
        elif opcion == 1:  # Registrarse
            usuario = input_box(pantalla, FUENTE40, "Nuevo usuario:", 120, 300)
            if usuario is None: break
            contrasena = input_box(pantalla, FUENTE40, "Nueva contraseña:", 120, 400, password=True)
            if contrasena is None: break
            if db.registrar_jugador(usuario, contrasena):
                mostrar_mensaje(pantalla, "Usuario registrado con éxito.", FUENTE40, (0,255,0), 500)
            else:
                mostrar_mensaje(pantalla, "Nombre de usuario ya existe.", FUENTE40, (255,0,0), 500)
        elif opcion == 2:  # Ver tabla de puntajes
            mostrar_tabla_puntajes(pantalla, FUENTE40, db, 100)

    pygame.quit()

if __name__ == "__main__":
    main()