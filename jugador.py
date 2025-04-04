import pygame
from enum import Enum
from main import TileType
from laberintos import Pantallas

# ====================================================================================
#   jugador.py (modulo logica del Pacman)
#   class --> PacMan, PacManDies, Direccion
#
# ------------------------------------------------------------------------------------
class Direccion(Enum):
    RIGHT = "ri"
    LEFT = "le"
    UP = "up"
    DOWN = "do"

class PacMan(pygame.sprite.Sprite):
    def __init__(self, game, x, y, dir_por_defecto=Direccion.RIGHT.value):
        super().__init__()
        self.game = game
        self.TX = self.game.CO.TX
        self.TY = self.game.CO.TY
        self.direccion_actual = dir_por_defecto
        self.direccion_confirmada = self.direccion_actual

        # 'teclaPulsada': [velX, velY, índice_animación]
        self.movimientos = {
            Direccion.RIGHT.value: [1, 0, 0],
            Direccion.LEFT.value: [-1, 0, 2],
            Direccion.UP.value: [0, -1, 4],
            Direccion.DOWN.value: [0, 1, 6],
        }

        # Animación
        self.lista_imagenes = [
            self.game.obtener_grafico(f"pacman{i + 1}.png", 1)[0] for i in range(8)
        ]
        self.indice_animacion = 0
        self.image = self.lista_imagenes[self.movimientos[self.direccion_actual][2]]

        # Rectángulo y posición
        self.rect = self.image.get_rect()
        self.rect.x = x * self.TX
        self.rect.y = y * self.TY

        # Configuración adicional
        self.velocidad = 2
        self.avanzar = True
        self.ultimo_update = pygame.time.get_ticks()
        self.fotograma_vel = 90 # Velocidad de la animación
        self.sonido_sirena_intervalo = 500
        self.ultimo_sonido = pygame.time.get_ticks()

    def update(self):
        if not self.game.estado_juego["en_juego"]:
            return

        self.leer_teclado()
        self.actualizar_animacion()
        self.manejar_colisiones()
        #self.reproducir_sirena()

    def leer_teclado(self):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            self.direccion_actual = Direccion.LEFT.value
        elif teclas[pygame.K_RIGHT]:
            self.direccion_actual = Direccion.RIGHT.value
        elif teclas[pygame.K_UP]:
            self.direccion_actual = Direccion.UP.value
        elif teclas[pygame.K_DOWN]:
            self.direccion_actual = Direccion.DOWN.value

    def manejar_colisiones(self):
        # Solo comprobamos si estamos en el centro exacto del tile
        if self.rect.x % self.TX == 0 and self.rect.y % self.TY == 0:
            x, y = self.rect.x // self.TX, self.rect.y // self.TY
            colision_direccion = self.colision_laberinto(self.direccion_actual, x, y)
            colision_velocidad = self.colision_laberinto(self.direccion_confirmada, x, y)

            if not colision_direccion:
                self.avanzar = True
                self.direccion_confirmada = self.direccion_actual
            elif not colision_velocidad:
                self.avanzar = True
            else:
                self.avanzar = False

        if self.avanzar:
            vel_x, vel_y = self.movimientos[self.direccion_confirmada][:2]
            self.rect.x += vel_x * self.velocidad
            self.rect.y += vel_y * self.velocidad

    def colision_laberinto(self, direccion, x, y):
        vel_x, vel_y = self.movimientos[direccion][:2]

        if self.es_teletransporte(x, y, vel_x):
            return False
        
        indice = self.game.obtener_indice(x + vel_x, y + vel_y)

        if (indice is None):
            return False
        
        return Pantallas.get_laberinto(self.game.nivel)[indice] == TileType.WALL.value

    def es_teletransporte(self, x, y, vel_x):
        if y == 11:  # Línea especial para teletransporte
            if x + vel_x > self.game.CO.COLUMNAS:
                self.rect.x = -self.TX
                return True
            elif x + vel_x < -1:
                self.rect.x = self.game.CO.COLUMNAS * self.TX
                return True
        return False

    def actualizar_animacion(self):
        if pygame.time.get_ticks() - self.ultimo_update > self.fotograma_vel:
            self.ultimo_update = pygame.time.get_ticks()
            self.indice_animacion = 1 - self.indice_animacion  # Alterna entre 0 y 1
            indice_base = self.movimientos[self.direccion_confirmada][2]
            self.image = self.lista_imagenes[indice_base + self.indice_animacion]

    def reproducir_sirena(self):
        if pygame.time.get_ticks() - self.ultimo_sonido > self.sonido_sirena_intervalo:
            self.ultimo_sonido = pygame.time.get_ticks()
            self.game.sonidos["sirena"].play(maxtime=500)

class PacManDies(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game

        # Cargar imágenes de animación
        indices_animacion = [1, 7, 3, 5]
        self.lista_imagenes = [
            self.game.obtenerGrafico(f"pacman{i}.png", 1)[0] for i in indices_animacion
        ]
        self.image = self.lista_imagenes[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Configuración de animación
        self.indice_animacion = 0
        self.ultimo_update = pygame.time.get_ticks()
        self.fotograma_vel = 170
        self.ultimo_update_duracion = pygame.time.get_ticks()
        self.duracion = 2400# Duracion de la secuencia PacmanDies

    def update(self):
        self.actualizar_animacion()
        self.verificar_duracion()

    def actualizar_animacion(self):
        if pygame.time.get_ticks() - self.ultimo_update > self.fotograma_vel:
            self.ultimo_update = pygame.time.get_ticks()
            self.indice_animacion = (self.indice_animacion + 1) % len(self.lista_imagenes)
            self.image = self.lista_imagenes[self.indice_animacion]

    def verificar_duracion(self):
        if pygame.time.get_ticks() - self.ultimo_update_duracion > self.duracion:
            self.kill()
            #self.game.listas_sprites["fantasmas"].empty()
            #self.game.vidas -= 1
            #self.game.reinstanciar_pacmanFantasmas = True
            #self.game.instanciar_objetos()
