import pygame

class LaberintoTile(pygame.sprite.Sprite):
    def __init__(self, game, x, y, valor_tile):
        super().__init__()
        self.game = game
        self.TX = self.game.TX
        self.TY = self.game.TY

        nivel = min(self.game.nivel, 3)  # Limitar nivel máximo a 3
        self.image = self.game.obtener_grafico(f'bloquepac{nivel}.png', 1)[0]
        self.rect = self.game.obtener_grafico(f'bloquepac{nivel}.png', 1)[1]
        self.rect.x, self.rect.y = x * self.TX, y * self.TY
        self.valor = valor_tile

    def update(self):
        pass  # El laberinto no necesita actualización dinámica

class Puntitos(pygame.sprite.Sprite):
    SUMA_PUNTOS = 10

    def __init__(self, game, x, y, valor_tile):
        super().__init__()
        self.game = game
        self.TX = self.game.TX
        self.TY = self.game.TY

        self.image = self.game.obtener_grafico('pildopac.png', 0.2)[0]
        self.rect = self.game.obtener_grafico('pildopac.png', 0.2)[1]
        self.rect.center = (x * self.TX + self.TX // 2, y * self.TY + self.TY // 2)
        self.valor = valor_tile

    def update(self):
        if pygame.sprite.spritecollide(self, self.game.listas_sprites["pacman"], False):
            self.kill()
            self.game.puntos += Puntitos.SUMA_PUNTOS
            #self.game.sonido_sirena.stop()
            #self.game.cargar_sonidos()["wakawaka"].play(maxtime=500)

class PuntosGordos(pygame.sprite.Sprite):
    def __init__(self, game, x, y, valor_tile):
        super().__init__()
        self.game = game
        self.TX = self.game.TX
        self.TY = self.game.TY

        self.escala = 0.5
        self.vel_anima = 150
        self.ultimo_update = pygame.time.get_ticks()

        self.image = self._cargar_imagen()[0]
        self.rect = self._cargar_imagen()[1]
        self.rect.center = (x * self.TX + self.TX // 2, y * self.TY + self.TY // 2)
        self.centerXY = self.rect.center
        self.valor = valor_tile

    def _cargar_imagen(self):
        """Carga la imagen del punto gordo con la escala actual."""
        return self.game.obtener_grafico('puntoGordo.png', self.escala)

    def _alternar_escala(self):
        """Alternar la escala entre 0.3 y 0.5."""
        self.escala = 0.3 if self.escala == 0.5 else 0.5
        self.image = self._cargar_imagen()[0]
        self.rect = self._cargar_imagen()[1]

    def update(self):
        # Animación de escala
        if pygame.time.get_ticks() - self.ultimo_update > self.vel_anima:
            self.ultimo_update = pygame.time.get_ticks()
            self._alternar_escala()
            self.rect.center = self.centerXY

        # Colisión con PacMan
        if pygame.sprite.spritecollide(self, self.game.listas_sprites["pacman"], False) and not self.game.temporizadorAzules:
            self.kill()
            #self.game.temporizadorAzules = True
            #self.game.ultimoUpdate_azules = pygame.time.get_ticks()

            """ for fantasma in self.game.lista_los4fantasmas:
                x, y = int(fantasma.rect.x / self.game.TX), int(fantasma.rect.y / self.game.TY)
                self.game.instanciar_fantasma(x, y, fantasma.idFantasma, fantasma.direccion, azul=True, ojos=False)
                fantasma.kill() """

            #self.game.sonido_eatingGhost.play()

class Textos(pygame.sprite.Sprite):
    def __init__(self, game, texto, size, x, y, color, fondo=None, negrita=False, centrado=True, tipo=None):
        super().__init__()
        self.game = game
        self.texto = texto
        self.size = size
        self.color = color
        self.fondo = fondo
        self.centrado = centrado
        self.tipo = tipo
        self.font = pygame.font.SysFont('verdana', self.size)
        self.font.set_bold(negrita)
        self.image = self.font.render(self.texto, True, self.color, self.fondo)

        if self.centrado:
            self.rect = self.image.get_rect(center=(x, y))
        else:
            self.rect = self.image.get_rect(topleft=(x, y))
        
        # Identificar si se trata de un texto dinámico (puntos o nivel)
        #self.render_nivel = self.texto = str(self.game.nivel)

    def update(self):
        if self.tipo == "dinamico-puntos":
            self.image = self.font.render(f'{self.game.puntos}', True, self.color, self.fondo)
        if self.tipo == "dinamico-nivel":
            self.image = self.font.render(f'{self.game.nivel}', True, self.color, self.fondo)

class ItemFrutas(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self.x, self.y = x, y

        # Limitar el número máximo de niveles para la fruta
        item_nivel = min(self.game.nivel, 4)
        self.image, self.rect = self.game.obtenerGrafico(f'item{item_nivel}.png', 1)
        self.rect.x, self.rect.y = x * self.game.TX, y * self.game.TY

    def update(self):
        if pygame.sprite.spritecollide(self, self.game.lista_pacman, False):
            self.kill()
            puntos_fruta = (self.game.nivel * 10) ** 2
            self.game.puntos += puntos_fruta
            self.game.ultimo_update_itemFruta = pygame.time.get_ticks()
            self.game.instanciaPtosComeFantasmas(puntos_fruta, self.x, self.y)
            self.game.sonido_eatingCherry.play()

