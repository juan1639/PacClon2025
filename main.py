import pygame
import sys
from enum import Enum
from jugador import *
from fantasmas import *
from varios import *
from laberintos import Pantallas
from settings import *

# ====================================================================================
#   main.py (modulo principal) ... clase principal --> class Game
#
# ------------------------------------------------------------------------------------
class TileType(Enum):
    WALL = 9
    DOT = 1
    POWER_DOT = 5

class Game:
    def __init__(self):
        pygame.init()

        # Colores y constantes
        self.COL = Colores()
        self.CO = Constantes()

        # Marcadores: ptos, nivel, vidas...
        self.nivel = 1
        self.puntos = 0
        self.vidas = 3

        # Varios
        self.sumaPtosComeFantasmas = 100	# 200 -> 400 -> 800 -> 1600
        self.temporizadorAzules = False 
        self.ultimo_update_azules = pygame.time.get_ticks()
        self.ultimo_update_preparado = pygame.time.get_ticks()

        # Estados del juego
        self.program_running = True
        self.menu_presentacion = True
        self.preparado = False
        self.en_juego = False
        self.game_over = False
        self.nivel_superado = False

        # Inicializar listas con sprites
        self.listas_sprites = {
            "all_sprites": pygame.sprite.Group(),
            "pacman": pygame.sprite.Group(),
            "laberinto": pygame.sprite.Group(),
            "puntitos": pygame.sprite.Group(),
            "puntos_gordos": pygame.sprite.Group(),
            "items": pygame.sprite.Group(),
            "textos": pygame.sprite.Group(),
            "bonus_come_fantasmas": pygame.sprite.Group(),
            "fantasmas": pygame.sprite.Group()
        }

        # Pantalla y reloj
        self.pantalla = pygame.display.set_mode(self.CO.RESOLUCION)
        self.reloj = pygame.time.Clock()

        # Cargar sonidos del modulo settings
        self.sonidos = Sonidos()
    
    def obtener_indice(self, x, y):
        """Obtener índice en el laberinto 1D basado en coordenadas 2D."""
        return y * self.CO.COLUMNAS + x if 0 <= x < self.CO.COLUMNAS and 0 <= y < self.CO.FILAS else None
    
    def crear_pantalla_nivel(self):
        """Crear el laberinto y los tiles correspondientes."""
        contador = -1
        for i in range(self.CO.FILAS):
            for ii in range(self.CO.COLUMNAS):
                contador += 1
                valor_tile = Pantallas.get_laberinto(self.nivel)[contador]

                # Usar enumeración para los tipos de tiles
                if valor_tile == TileType.WALL.value:
                    tile = LaberintoTile(self, ii, i, valor_tile)
                    self.listas_sprites["all_sprites"].add(tile)
                    self.listas_sprites["laberinto"].add(tile)
                elif valor_tile == TileType.DOT.value:
                    dot = Puntitos(self, ii, i, valor_tile)
                    self.listas_sprites["all_sprites"].add(dot)
                    self.listas_sprites["puntitos"].add(dot)
                elif valor_tile == TileType.POWER_DOT.value:
                    power_dot = PuntosGordos(self, ii, i, valor_tile)
                    self.listas_sprites["all_sprites"].add(power_dot)
                    self.listas_sprites["puntos_gordos"].add(power_dot)

    def vaciar_listas(self):
        """Vaciar todas las listas de sprites."""
        for grupo in self.listas_sprites.values():
            grupo.empty()
    
    def new_game(self):
        """Preparar un nuevo nivel o juego."""
        self.vaciar_listas()
        self.crear_pantalla_nivel()
        self.instanciar_objetos()
        self.instanciar_textos_iniciales()
        self.sonidos.reproducir("inicio_nivel")
    
    def obtener_grafico(self, nombrePng, escala):
        """Devolver una imagen y un rectangulo."""
        img = pygame.image.load('pacGraf/' + nombrePng).convert()
        escalaX = self.CO.TX * escala
        escalaY = self.CO.TY * escala
        image = pygame.transform.scale(img, (escalaX, escalaY))
        image.set_colorkey((255, 255, 255))
        rect = image.get_rect()
        
        return (image, rect)
    
    def instanciar_objetos(self):
        """Instanciar/re-instanciar Pacman, fantasmas, etc..."""
        self.pacman = PacMan(self, self.CO.PACMAN_INI_POS[0], self.CO.PACMAN_INI_POS[1])
        self.listas_sprites["all_sprites"].add(self.pacman)
        self.listas_sprites["pacman"].add(self.pacman)
        
        """ for i in range(self.CONSTANT.N_FANTASMAS):
            datos = self.CONSTANT.LISTA_ARGS_FANTASMAS[i]
            coorX = datos[0]
            coorY = datos[1]
            self.instanciar_fantasma(coorX, coorY, i, datos[3], False, False) """
    
    def instanciar_fantasma(self, coorX, coorY, i, direc, azul, ojos):
        fantasma = Fantasma(self, coorX, coorY, i, direc, azul, ojos)
        #self.lista_sprites_adibujar.add(fantasma)
        self.listas_sprites["fantasmas"].add(fantasma)
    
    def instanciar_textos_iniciales(self):
        """Instanciar textos marcadores, Preparado..."""
        MARGEN = 9

        self.instanciar_texto(self.CO.TXT_PREPARADO, 90, (self.CO.RESOLUCION[0] - self.CO.ZONA_SCORES) // 2,
            300, self.COL.VERDE_FONDO, negrita=True)
        
        self.instanciar_texto("Puntos", 48, self.CO.RESOLUCION[0] - self.CO.ZONA_SCORES + MARGEN,
            self.CO.TY, self.COL.AMARILLENTO, negrita=True, centrado=False)
        self.instanciar_texto("Nivel", 48, self.CO.RESOLUCION[0] - self.CO.ZONA_SCORES + MARGEN,
            self.CO.TY * 4, self.COL.AMARILLENTO, negrita=True, centrado=False)
        self.instanciar_texto("0", 48, self.CO.RESOLUCION[0] - self.CO.ZONA_SCORES + MARGEN,
            self.CO.TY * 2, self.COL.BLANCO, negrita=True, centrado=False, tipo="dinamico-puntos")
        self.instanciar_texto(str(self.nivel), 48, self.CO.RESOLUCION[0] - self.CO.ZONA_SCORES + MARGEN,
            self.CO.TY * 5, self.COL.BLANCO, negrita=True, centrado=False, tipo="dinamico-nivel")
    
    def instanciar_texto(self, txt, size, x, y, color, fondo=None, negrita=False, centrado=True, tipo=None):
        """Instanciar un texto y agregarlo a su lista correspondiente..."""
        newTxt = Textos(self, txt, size, x, y, color, fondo, negrita, centrado, tipo)
        self.listas_sprites["textos"].add(newTxt)
    
    def update(self):
        pygame.display.set_caption(str(int(self.reloj.get_fps())))
        
        #self.checkTemporizadorAzules()
        #self.checkNivelSuperado()
        #self.instanciar_itemFrutas()
        
        if not self.preparado:
            self.listas_sprites["all_sprites"].update()
            #self.listas_sprites["fantasmas"].update()
            self.listas_sprites["textos"].update()
        else:
            calculo = pygame.time.get_ticks()
            if calculo - self.ultimo_update_preparado > self.CO.DURACION_PREPARADO:
                self.ultimo_update_preparado = calculo
                self.preparado = False
                for sprite in self.listas_sprites["textos"]:
                    if isinstance(sprite, Textos) and sprite.texto == self.CO.TXT_PREPARADO:
                        self.listas_sprites["textos"].remove(sprite)
                        break
        
        #self.checkTransicion_gameOverRejugar()
        
        pygame.display.flip()
        self.reloj.tick(self.CO.FPS)
    
    def draw(self):
        self.pantalla.fill(self.COL.GRIS_FONDO)
        
        self.listas_sprites["all_sprites"].draw(self.pantalla)
        #self.listas_sprites["fantasmas"].draw(self.pantalla)

        # dibujar rectangulo "transparente" escapatoria
        pygame.draw.rect(self.pantalla, self.COL.GRIS_FONDO, 
            (self.CO.COLUMNAS * self.CO.TX, 11 * self.CO.TY, self.CO.TX, self.CO.TY))
        
        #self.renderizar_vidasMarcador()
        
        #self.listas_sprites["bonus_come_fantasmas"].draw(self.pantalla)
        self.listas_sprites["textos"].draw(self.pantalla)
    
    def check_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.program_running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.program_running = False
                    pygame.quit()
                    sys.exit()
                
                if event.key == pygame.K_RETURN and self.menu_presentacion:
                    pygame.mixer.music.stop()
                    self.menu_presentacion = False
                    self.en_juego = True
                    self.preparado = True
                    self.ultimo_update_preparado = pygame.time.get_ticks()
                    #self.sonido_inicioNivel.play()
                    self.new_game()
    
    def bucle_principal(self):
        while self.program_running:
            self.check_event()
            self.update()
            self.draw()

if __name__ == '__main__':
    game = Game()
    game.bucle_principal()

