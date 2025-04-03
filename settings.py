import pygame

# ====================================================================================
#	settings.py (modulo de configuraciones)
# 
# ------------------------------------------------------------------------------------
class Colores:
    AMARILLO = (220, 190, 0)
    AMARILLENTO = (250, 245, 130)
    BLANCO = (240, 240, 240)
    GRIS_FONDO = (59, 59, 59)
    ROJO = (230, 30, 20)
    VERDE_FONDO = (20, 240, 30)
    AZUL_C = (144, 205, 205)

class Constantes:
    TX, TY = 50, 50 # Tamano de los Tiles
    FILAS, COLUMNAS = 15, 19 # Filas x Columnas
    PACMAN_INI_POS = (9, 4)
    N_FANTASMAS = 4
    DURACION_AZULES = 8000 # Duracion de los 'fantasmas-azules' en el nivel 1
    DURACION_PREPARADO = 4200
    INTERVALO_FRUTA = 12000
    TXT_PREPARADO = " Preparado! "
    ZONA_SCORES = 200
    RESOLUCION = (TX * COLUMNAS + ZONA_SCORES, TY * FILAS)
    FPS = 100

    LISTA_ARGS_FANTASMAS = [
        (5, 8, 0, 'le'), (8, 8, 1, 'le'),
        (10, 8, 2, 'ri'), (13, 8, 3, 'ri')
    ]

class Sonidos:
    def __init__(self):
        pygame.mixer.init()
        self.sonidos = self.cargar_sonidos()

    def cargar_sonidos(self):
        """Cargar todos los sonidos en un diccionario."""
        return {
            "wakawaka": self.cargar_sonido("sonido/pacmanwakawaka.ogg", 0.9),
            "sirena": self.cargar_sonido("sonido/pacmansirena.ogg", 0.2),
            "eating_cherry": self.cargar_sonido("sonido/pacmaneatingcherry.ogg"),
            "pacman_dies": self.cargar_sonido("sonido/pacmandies.ogg"),
            "gameover_retro": self.cargar_sonido("sonido/gameoveretro.ogg"),
            "fantasmas_azules": self.cargar_sonido("sonido/pacmanazules.ogg"),
            "eating_ghost": self.cargar_sonido("sonido/pacmaneatinghost.ogg"),
            "inicio_nivel": self.cargar_sonido("sonido/pacmaninicionivel.ogg")
        }

    def cargar_sonido(self, ruta, volumen=1.0):
        """Carga un sonido específico con el volumen indicado."""
        sonido = pygame.mixer.Sound(ruta)
        sonido.set_volume(volumen)
        return sonido

    def reproducir(self, nombre, duracion=None):
        """Reproduce un sonido si está en el diccionario."""
        if nombre in self.sonidos:
            if duracion == None:
                self.sonidos[nombre].play()
            else:
                self.sonidos[nombre].play(maxtime=duracion)

