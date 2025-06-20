import sqlite3
import datetime

class DBManager:
    def __init__(self, db_file='jugadores.db'):
        self.db_file = db_file
        self.conexion = None
        self.crear_tabla()

    def conectar(self):
        if not self.conexion:
            self.conexion = sqlite3.connect(self.db_file)
        return self.conexion

    def crear_tabla(self):
        try:
            con = self.conectar()
            cur = con.cursor()
            cur.execute('''
                CREATE TABLE IF NOT EXISTS jugadores (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT UNIQUE NOT NULL,
                    contrasena TEXT NOT NULL
                )
            ''')
            cur.execute('''
                CREATE TABLE IF NOT EXISTS puntajes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    puntaje INTEGER NOT NULL,
                    fecha TEXT NOT NULL,
                    FOREIGN KEY(nombre) REFERENCES jugadores(nombre)
                )
            ''')
            con.commit()
        except Exception as e:
            print("Error al crear la tabla:", e)

    def registrar_jugador(self, nombre, contrasena):
        try:
            con = self.conectar()
            cur = con.cursor()
            cur.execute('INSERT INTO jugadores (nombre, contrasena) VALUES (?, ?)', (nombre, contrasena))
            con.commit()
            return True
        except sqlite3.IntegrityError:
            print("El nombre de usuario ya existe.")
            return False
        except Exception as e:
            print("Error al registrar jugador:", e)
            return False

    def verificar_login(self, nombre, contrasena):
        try:
            con = self.conectar()
            cur = con.cursor()
            cur.execute('SELECT * FROM jugadores WHERE nombre=? AND contrasena=?', (nombre, contrasena))
            return cur.fetchone() is not None
        except Exception as e:
            print("Error al verificar login:", e)
            return False

    def actualizar_puntaje(self, nombre, puntaje):
        try:
            con = self.conectar()
            cur = con.cursor()
            cur.execute('UPDATE jugadores SET puntaje = MAX(puntaje, ?) WHERE nombre=?', (puntaje, nombre))
            con.commit()
        except Exception as e:
            print("Error al actualizar puntaje:", e)

    def registrar_puntaje(self, nombre, puntaje):
        try:
            con = self.conectar()
            cur = con.cursor()
            fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            cur.execute('INSERT INTO puntajes (nombre, puntaje, fecha) VALUES (?, ?, ?)', (nombre, puntaje, fecha))
            con.commit()
        except Exception as e:
            print("Error al registrar puntaje:", e)

    def obtener_top_puntajes(self, limite=10):
        try:
            con = self.conectar()
            cur = con.cursor()
            cur.execute('''
                SELECT nombre, MAX(puntaje) as max_puntaje, fecha
                FROM puntajes
                WHERE (nombre, puntaje) IN (
                    SELECT nombre, MAX(puntaje)
                    FROM puntajes
                    GROUP BY nombre
                )
                GROUP BY nombre
                ORDER BY max_puntaje DESC
                LIMIT ?
            ''', (limite,))
            return cur.fetchall()
        except Exception as e:
            print("Error al obtener top puntajes:", e)
            return []