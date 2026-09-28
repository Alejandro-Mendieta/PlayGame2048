""" Autor : Alejandro Mendieta
Date : 27-09-2026
Descripción : Play Game 2048 """ 
import random
import pygame
import os
import sys
import math

pygame.init()

# =============================================================================
# CONFIGURACIÓN
# =============================================================================

ANCHO, ALTO = 1400, 900
FPS = 60

COLOR_FONDO_GRADIENTE_TOP = (18, 15, 40)
COLOR_FONDO_GRADIENTE_BOTTOM = (8, 8, 20)
COLOR_TABLERO = (22, 22, 40)
COLOR_BORDE = (100, 80, 200)
COLOR_BORDE_GLOW = (150, 100, 255)
COLOR_TEXTO = (230, 240, 255)
COLOR_TEXTO_SECUNDARIO = (140, 140, 180)
COLOR_ACENTO = (255, 200, 60)
COLOR_ACENTO_2 = (0, 220, 255)
COLOR_BOTON = (100, 50, 200)

COLORES_FICHAS = {
    0:    ((30, 30, 50), (25, 25, 42)),
    2:    ((238, 228, 218), (220, 210, 200)),
    4:    ((237, 224, 200), (220, 205, 180)),
    8:    ((255, 170, 80), (255, 140, 50)),
    16:   ((255, 140, 60), (255, 110, 30)),
    32:   ((255, 100, 70), (240, 70, 50)),
    64:   ((255, 60, 60), (220, 30, 30)),
    128:  ((255, 210, 100), (255, 180, 60)),
    256:  ((255, 200, 60), (255, 160, 40)),
    512:  ((255, 190, 40), (255, 140, 20)),
    1024: ((255, 215, 0), (255, 170, 0)),
    2048: ((255, 230, 0), (255, 190, 0)),
    4096: ((80, 220, 140), (40, 190, 100)),
    8192: ((60, 190, 240), (30, 150, 220)),
}

COLOR_TEXTO_FICHA = {2: (100, 95, 90), 4: (100, 95, 90)}
COLOR_TEXTO_FICHA_DEFAULT = (255, 255, 255)

TAMANO_TABLERO = 4
TAMANO_CELDA = 140
ESPACIO_CELDA = 18
TAMANO_TABLERO_PX = TAMANO_TABLERO * TAMANO_CELDA + (TAMANO_TABLERO + 1) * ESPACIO_CELDA

TABLERO_X = 80
TABLERO_Y = (ALTO - TAMANO_TABLERO_PX) // 2 + 20

# =============================================================================
# FUENTES
# =============================================================================

def obtener_fuente(tamano, bold=False):
    fuentes = ['dejavusans', 'liberationsans', 'freesans', 'arial', None]
    for nombre in fuentes:
        try:
            f = pygame.font.SysFont(nombre, tamano, bold=bold)
            if f.render('T', True, (255, 255, 255)).get_width() > 0:
                return f
        except:
            continue
    return pygame.font.Font(None, tamano)

def obtener_fuente_ficha(valor):
    digitos = len(str(valor))
    if digitos <= 2: return obtener_fuente(58, bold=True)
    elif digitos == 3: return obtener_fuente(48, bold=True)
    elif digitos == 4: return obtener_fuente(38, bold=True)
    else: return obtener_fuente(30, bold=True)

fuente_pequena = obtener_fuente(18)
fuente_mediana = obtener_fuente(26)
fuente_grande = obtener_fuente(44, bold=True)
fuente_titulo = obtener_fuente(84, bold=True)
fuente_huge = obtener_fuente(110, bold=True)

# =============================================================================
# UTILIDADES
# =============================================================================

def lerp(a, b, t):
    return a + (b - a) * t

def lerp_color(c1, c2, t):
    return (int(lerp(c1[0], c2[0], t)), int(lerp(c1[1], c2[1], t)), int(lerp(c1[2], c2[2], t)))

def ease_out_cubic(t):
    return 1 - pow(1 - t, 3)

def dibujar_rect_redondeado_con_glow(surf, color, rect, radio, glow_color=None, glow_size=3):
    if glow_color:
        for i in range(glow_size, 0, -1):
            alpha = max(0, min(255, int(80 / i)))
            glow_surf = pygame.Surface((rect.width + i*4, rect.height + i*4), pygame.SRCALPHA)
            pygame.draw.rect(glow_surf, (*glow_color, alpha), (i*2, i*2, rect.width, rect.height), border_radius=radio + i)
            surf.blit(glow_surf, (rect.x - i*2, rect.y - i*2))
    pygame.draw.rect(surf, color, rect, border_radius=radio)

def posicion_celda(fila, col):
    """Devuelve el centro (x, y) de una celda del tablero"""
    x = TABLERO_X + ESPACIO_CELDA + col * (TAMANO_CELDA + ESPACIO_CELDA) + TAMANO_CELDA // 2
    y = TABLERO_Y + ESPACIO_CELDA + fila * (TAMANO_CELDA + ESPACIO_CELDA) + TAMANO_CELDA // 2
    return x, y

# =============================================================================
# CLASE FICHA (con animación de movimiento correcta)
# =============================================================================

class Ficha:
    """Ficha visual con animación de deslizamiento."""
    def __init__(self, valor, fila, col):
        self.valor = valor
        self.fila = fila
        self.col = col
        # Posición visual actual (comienza en el destino)
        self.x, self.y = posicion_celda(fila, col)
        # Estado de animación
        self.moviendose = False
        self.velocidad_anim = 0.25
        # Animación de aparición
        self.spawn_time = pygame.time.get_ticks()
        self.spawn_duration = 150
        self.escala = 1.0
        # Eliminación (por fusión)
        self.eliminar = False
        self.eliminar_time = 0
        self.eliminar_duration = 100
    
    def mover_a(self, nueva_fila, nueva_col):
        """Cambia el destino de la ficha (mantiene la posición visual actual para animar)"""
        self.fila = nueva_fila
        self.col = nueva_col
        self.moviendose = True
    
    def marcar_para_eliminar(self):
        """Marca la ficha para desaparecer (fue absorbida en una fusión)"""
        self.eliminar = True
        self.eliminar_time = pygame.time.get_ticks()
    
    def actualizar(self):
        # Animación de eliminación
        if self.eliminar:
            t = (pygame.time.get_ticks() - self.eliminar_time) / self.eliminar_duration
            if t >= 1:
                return False  # Ya no existe
            self.escala = max(0, 1 - t)
            return True
        
        # Animación de aparición
        tiempo_spawn = pygame.time.get_ticks() - self.spawn_time
        if tiempo_spawn < self.spawn_duration:
            t = tiempo_spawn / self.spawn_duration
            self.escala = ease_out_cubic(t)
        else:
            self.escala = 1.0
        
        # Interpolación hacia el destino
        if self.moviendose:
            obj_x, obj_y = posicion_celda(self.fila, self.col)
            self.x = lerp(self.x, obj_x, self.velocidad_anim)
            self.y = lerp(self.y, obj_y, self.velocidad_anim)
            
            # Snap cuando está muy cerca (evita temblor)
            if abs(self.x - obj_x) < 0.5 and abs(self.y - obj_y) < 0.5:
                self.x = obj_x
                self.y = obj_y
                self.moviendose = False
        
        return True
    
    def dibujar(self, pantalla):
        if self.escala <= 0.01:
            return
        
        tamano = max(8, int(TAMANO_CELDA * self.escala))
        rect = pygame.Rect(0, 0, tamano, tamano)
        rect.center = (int(self.x), int(self.y))
        
        color_top, color_bottom = COLORES_FICHAS.get(self.valor, ((100,100,120),(80,80,100)))
        
        # Gradiente
        gradiente_surf = pygame.Surface((rect.width, rect.height))
        for i in range(rect.height):
            t = i / max(1, rect.height - 1)
            color = lerp_color(color_top, color_bottom, t)
            pygame.draw.line(gradiente_surf, color, (0, i), (rect.width, i))
        
        # Máscara redondeada
        mascara = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        pygame.draw.rect(mascara, (255, 255, 255, 255), (0, 0, rect.width, rect.height), border_radius=10)
        gradiente_surf = gradiente_surf.convert_alpha()
        gradiente_surf.blit(mascara, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        
        pantalla.blit(gradiente_surf, rect.topleft)
        
        # Borde
        if rect.width > 20:
            pygame.draw.rect(pantalla, (255, 255, 255, 50), rect, 2, border_radius=10)
        
        # Brillo superior
        brillo_ancho = rect.width - 10
        brillo_alto = rect.height // 3
        if brillo_ancho > 0 and brillo_alto > 0:
            brillo = pygame.Surface((brillo_ancho, brillo_alto), pygame.SRCALPHA)
            brillo.fill((255, 255, 255, 30))
            pantalla.blit(brillo, (rect.x + 5, rect.y + 5))
        
        # Texto
        if rect.width > 15:
            color_texto = COLOR_TEXTO_FICHA.get(self.valor, COLOR_TEXTO_FICHA_DEFAULT)
            fuente = obtener_fuente_ficha(self.valor)
            texto = fuente.render(str(self.valor), True, color_texto)
            texto_rect = texto.get_rect(center=(int(self.x), int(self.y)))
            pantalla.blit(texto, texto_rect)

# =============================================================================
# JUEGO
# =============================================================================

class Juego2048:
    def __init__(self):
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("2048 Premium")
        self.reloj = pygame.time.Clock()
        
        self.crear_icono()
        
        self.estado = "menu"
        self.puntuacion = 0
        self.mejor_puntuacion = self.cargar_mejor_puntuacion()
        self.movimientos = 0
        self.max_ficha = 0
        self.tiempo_inicio = 0
        self.tiempo_jugado = 0
        
        # Grid lógico de valores
        self.grid = [[0] * TAMANO_TABLERO for _ in range(TAMANO_TABLERO)]
        # Fichas visuales activas
        self.fichas = []
        
        # Mensajes flotantes
        self.mensajes = []
        
        self.nuevo_juego()
    
    def crear_icono(self):
        icono = pygame.Surface((32, 32), pygame.SRCALPHA)
        for i in range(4):
            pygame.draw.rect(icono, (255, 200, 60), (i*8, i*8, 7, 7), border_radius=2)
        pygame.display.set_icon(icono)
    
    def cargar_mejor_puntuacion(self):
        try:
            with open('2048_premium_mejor.txt', 'r') as f:
                return int(f.read().strip())
        except:
            return 0
    
    def guardar_mejor_puntuacion(self):
        try:
            with open('2048_premium_mejor.txt', 'w') as f:
                f.write(str(self.mejor_puntuacion))
        except:
            pass
    
    def nuevo_juego(self):
        self.grid = [[0] * TAMANO_TABLERO for _ in range(TAMANO_TABLERO)]
        self.fichas = []
        self.puntuacion = 0
        self.movimientos = 0
        self.max_ficha = 0
        self.tiempo_inicio = pygame.time.get_ticks()
        self.tiempo_jugado = 0
        self.mensajes = []
        
        # Crear dos fichas iniciales
        self._spawn_ficha()
        self._spawn_ficha()
    
    def _spawn_ficha(self):
        """Añade una ficha nueva en una celda vacía (2 o 4)"""
        vacias = [(i, j) for i in range(TAMANO_TABLERO) for j in range(TAMANO_TABLERO) 
                  if self.grid[i][j] == 0]
        if not vacias:
            return None
        
        i, j = random.choice(vacias)
        valor = 2 if random.random() < 0.9 else 4
        self.grid[i][j] = valor
        
        ficha = Ficha(valor, i, j)
        ficha.spawn_time = pygame.time.get_ticks()
        ficha.escala = 0
        self.fichas.append(ficha)
        return ficha
    
    def mover(self, direccion):
        """Mueve todas las fichas en la dirección indicada."""
        
        # Verificar si la dirección es válida (no todas las direcciones mueven)
        grid_antes = [fila[:] for fila in self.grid]
        
        # Estructura para rastrear movimientos y fusiones:
        # Para cada celda destino, saber qué fichas de origen la alimentan
        # Representamos el grid de origen como una matriz de listas de fichas
        origen = [[[] for _ in range(TAMANO_TABLERO)] for _ in range(TAMANO_TABLERO)]
        for f in self.fichas:
            if not f.eliminar:
                origen[f.fila][f.col].append(f)
        
        # Nuevo grid y mapa de "quién va a dónde"
        nuevo_grid = [[0] * TAMANO_TABLERO for _ in range(TAMANO_TABLERO)]
        movimientos = []  # (ficha, nueva_fila, nueva_col)
        fusiones = []     # (lista_de_fichas_absorbidas, fila, col, valor_final)
        
        if direccion == 'izquierda':
            for i in range(TAMANO_TABLERO):
                self._procesar_linea(
                    [(i, j) for j in range(TAMANO_TABLERO)],
                    origen, nuevo_grid, movimientos, fusiones
                )
        elif direccion == 'derecha':
            for i in range(TAMANO_TABLERO):
                self._procesar_linea(
                    [(i, j) for j in range(TAMANO_TABLERO - 1, -1, -1)],
                    origen, nuevo_grid, movimientos, fusiones
                )
        elif direccion == 'arriba':
            for j in range(TAMANO_TABLERO):
                self._procesar_linea(
                    [(i, j) for i in range(TAMANO_TABLERO)],
                    origen, nuevo_grid, movimientos, fusiones
                )
        elif direccion == 'abajo':
            for j in range(TAMANO_TABLERO):
                self._procesar_linea(
                    [(i, j) for i in range(TAMANO_TABLERO - 1, -1, -1)],
                    origen, nuevo_grid, movimientos, fusiones
                )
        
        # Verificar si hubo cambio
        if grid_antes == nuevo_grid:
            return False
        
        # Aplicar cambios visuales: mover fichas y marcar las fusionadas
        for ficha, nueva_fila, nueva_col in movimientos:
            ficha.mover_a(nueva_fila, nueva_col)
        
        # Procesar fusiones: eliminar las absorbidas y crear las nuevas
        for fichas_absorbidas, fila, col, valor_final in fusiones:
            for f in fichas_absorbidas:
                f.marcar_para_eliminar()
            # Crear la nueva ficha con valor fusionado
            nueva = Ficha(valor_final, fila, col)
            nueva.spawn_time = pygame.time.get_ticks()
            nueva.escala = 0.5  # Aparece creciendo
            self.fichas.append(nueva)
            
            # Mensaje flotante para valores grandes
            if valor_final >= 128:
                x, y = posicion_celda(fila, col)
                self.mensajes.append({
                    'texto': f'+{valor_final}',
                    'x': x,
                    'y': y,
                    'color': COLORES_FICHAS.get(valor_final, ((255,255,255),))[0],
                    'tiempo': pygame.time.get_ticks(),
                    'duracion': 900
                })
        
        # Actualizar grid lógico
        self.grid = nuevo_grid
        self.movimientos += 1
        self.max_ficha = max(max(fila) for fila in self.grid)
        
        # Añadir nueva ficha
        self._spawn_ficha()
        
        # Verificar victoria
        if self.max_ficha >= 2048 and self.estado == "jugando":
            self._activar_victoria()
        
        # Verificar game over
        if not self._hay_movimientos():
            self._activar_game_over()
        
        return True
    
    def _procesar_linea(self, celdas, origen, nuevo_grid, movimientos, fusiones):
        """Procesa una línea (fila o columna) en el orden dado.
        celdas: lista de (fila, col) en el orden en que se "leen" (de donde vienen las fichas)"""
        
        # Extraer las fichas en orden
        fichas_linea = []
        valores_linea = []
        for (i, j) in celdas:
            for f in origen[i][j]:
                fichas_linea.append(f)
                valores_linea.append(f.valor)
        
        # Fusionar la lista de valores
        resultado_valores = []
        resultado_fichas = []  # Cada entrada: lista de fichas que contribuyen
        idx = 0
        while idx < len(valores_linea):
            if idx + 1 < len(valores_linea) and valores_linea[idx] == valores_linea[idx + 1]:
                # Fusión
                nuevo_valor = valores_linea[idx] * 2
                resultado_valores.append(nuevo_valor)
                resultado_fichas.append([fichas_linea[idx], fichas_linea[idx + 1]])
                self.puntuacion += nuevo_valor
                idx += 2
            else:
                resultado_valores.append(valores_linea[idx])
                resultado_fichas.append([fichas_linea[idx]])
                idx += 1
        
        # Colocar en las celdas destino (en el mismo orden)
        for k, (valor, fichas_grupo) in enumerate(zip(resultado_valores, resultado_fichas)):
            fila, col = celdas[k]
            nuevo_grid[fila][col] = valor
            
            if len(fichas_grupo) == 1:
                # Movimiento simple
                movimientos.append((fichas_grupo[0], fila, col))
            else:
                # Fusión: las fichas se mueven primero a la celda y luego se marcan para eliminar
                # Para animación, movemos una al destino y la otra también
                movimientos.append((fichas_grupo[0], fila, col))
                movimientos.append((fichas_grupo[1], fila, col))
                fusiones.append((fichas_grupo, fila, col, valor))
    
    def _hay_movimientos(self):
        for i in range(TAMANO_TABLERO):
            for j in range(TAMANO_TABLERO):
                if self.grid[i][j] == 0:
                    return True
                if j + 1 < TAMANO_TABLERO and self.grid[i][j] == self.grid[i][j+1]:
                    return True
                if i + 1 < TAMANO_TABLERO and self.grid[i][j] == self.grid[i+1][j]:
                    return True
        return False
    
    def _activar_victoria(self):
        self.estado = "victoria"
        self.guardar_puntuacion()
    
    def _activar_game_over(self):
        self.estado = "game_over"
        self.guardar_puntuacion()
    
    def guardar_puntuacion(self):
        if self.puntuacion > self.mejor_puntuacion:
            self.mejor_puntuacion = self.puntuacion
            self.guardar_mejor_puntuacion()
    
    # =========================================================================
    # EVENTOS
    # =========================================================================
    
    def manejar_eventos(self):
        mouse_pos = pygame.mouse.get_pos()
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            
            if evento.type == pygame.KEYDOWN:
                if self.estado == "menu":
                    if evento.key in (pygame.K_RETURN, pygame.K_SPACE):
                        self.nuevo_juego()
                        self.estado = "jugando"
                
                elif self.estado == "jugando":
                    if evento.key == pygame.K_ESCAPE:
                        self.estado = "pausa"
                    elif evento.key in (pygame.K_LEFT, pygame.K_a):
                        self.mover('izquierda')
                    elif evento.key in (pygame.K_RIGHT, pygame.K_d):
                        self.mover('derecha')
                    elif evento.key in (pygame.K_UP, pygame.K_w):
                        self.mover('arriba')
                    elif evento.key in (pygame.K_DOWN, pygame.K_s):
                        self.mover('abajo')
                    elif evento.key == pygame.K_r:
                        self.nuevo_juego()
                
                elif self.estado == "pausa":
                    if evento.key == pygame.K_ESCAPE:
                        self.estado = "jugando"
                    elif evento.key == pygame.K_r:
                        self.nuevo_juego()
                        self.estado = "jugando"
                    elif evento.key == pygame.K_m:
                        self.estado = "menu"
                
                elif self.estado in ("game_over", "victoria"):
                    if evento.key in (pygame.K_RETURN, pygame.K_SPACE):
                        self.nuevo_juego()
                        self.estado = "jugando"
                    elif evento.key == pygame.K_ESCAPE:
                        self.estado = "menu"
            
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if self.estado == "menu":
                    if pygame.Rect(ANCHO//2 - 130, 620, 260, 70).collidepoint(mouse_pos):
                        self.nuevo_juego()
                        self.estado = "jugando"
                
                elif self.estado == "pausa":
                    if pygame.Rect(ANCHO//2 - 140, 400, 280, 60).collidepoint(mouse_pos):
                        self.estado = "jugando"
                    elif pygame.Rect(ANCHO//2 - 140, 480, 280, 60).collidepoint(mouse_pos):
                        self.nuevo_juego()
                        self.estado = "jugando"
                    elif pygame.Rect(ANCHO//2 - 140, 560, 280, 60).collidepoint(mouse_pos):
                        self.estado = "menu"
                
                elif self.estado in ("game_over", "victoria"):
                    if pygame.Rect(ANCHO//2 - 140, 620, 280, 60).collidepoint(mouse_pos):
                        self.nuevo_juego()
                        self.estado = "jugando"
                    elif pygame.Rect(ANCHO//2 - 140, 700, 280, 60).collidepoint(mouse_pos):
                        self.estado = "menu"
        
        return True
    
    # =========================================================================
    # ACTUALIZACIÓN
    # =========================================================================
    
    def actualizar(self):
        if self.estado == "jugando":
            self.tiempo_jugado = (pygame.time.get_ticks() - self.tiempo_inicio) // 1000
        
        # Actualizar fichas y eliminar las terminadas
        self.fichas = [f for f in self.fichas if f.actualizar()]
        
        # Actualizar mensajes
        self.mensajes = [m for m in self.mensajes 
                        if pygame.time.get_ticks() - m['tiempo'] < m['duracion']]
    
    # =========================================================================
    # DIBUJADO
    # =========================================================================
    
    def dibujar(self):
        self.dibujar_fondo(self.pantalla)
        
        if self.estado == "menu":
            self.dibujar_menu(self.pantalla)
        else:
            self.dibujar_juego(self.pantalla)
        
        self.dibujar_mensajes(self.pantalla)
        
        if self.estado == "pausa":
            self.dibujar_pausa(self.pantalla)
        elif self.estado == "game_over":
            self.dibujar_game_over(self.pantalla)
        elif self.estado == "victoria":
            self.dibujar_victoria(self.pantalla)
        
        pygame.display.flip()
    
    def dibujar_fondo(self, surf):
        for y in range(ALTO):
            t = y / ALTO
            color = lerp_color(COLOR_FONDO_GRADIENTE_TOP, COLOR_FONDO_GRADIENTE_BOTTOM, t)
            pygame.draw.line(surf, color, (0, y), (ANCHO, y))
        
        tiempo = pygame.time.get_ticks() / 1000
        for i in range(80):
            base_x = (i * 173) % ANCHO
            base_y = (i * 97) % ALTO
            x = (base_x + int(tiempo * (5 + i % 10))) % ANCHO
            y = base_y
            brillo = int(80 + 100 * math.sin(tiempo * 2 + i))
            brillo = max(0, min(255, brillo))
            azul = max(0, min(255, brillo + 30))
            tamano = 1 if i % 3 else 2
            pygame.draw.circle(surf, (brillo, brillo, azul), (x, y), tamano)
    
    def dibujar_menu(self, surf):
        tiempo = pygame.time.get_ticks() / 1000
        
        # Título
        titulo_texto = "2048"
        fuente = fuente_huge
        letras = []
        total_ancho = 0
        for i, letra in enumerate(titulo_texto):
            offset_y = math.sin(tiempo * 2 + i * 0.5) * 12
            letra_surf = fuente.render(letra, True, COLOR_ACENTO)
            letras.append((letra_surf, offset_y))
            total_ancho += letra_surf.get_width() + 5
        
        x_inicio = ANCHO // 2 - total_ancho // 2
        for letra_surf, offset_y in letras:
            glow_surf = letra_surf.copy()
            glow_surf.set_alpha(80)
            surf.blit(glow_surf, (x_inicio - 3, 130 + offset_y))
            surf.blit(glow_surf, (x_inicio + 3, 130 + offset_y))
            surf.blit(letra_surf, (x_inicio, 130 + offset_y))
            x_inicio += letra_surf.get_width() + 5
        
        subtitulo = fuente_mediana.render("PUZZLE NUMÉRICO", True, COLOR_TEXTO_SECUNDARIO)
        subtitulo_rect = subtitulo.get_rect(center=(ANCHO // 2, 280))
        surf.blit(subtitulo, subtitulo_rect)
        
        pygame.draw.line(surf, COLOR_ACENTO_2, (ANCHO // 2 - 200, 310), (ANCHO // 2 + 200, 310), 2)
        
        panel_mejor = pygame.Rect(ANCHO // 2 - 200, 360, 400, 90)
        dibujar_rect_redondeado_con_glow(surf, COLOR_TABLERO, panel_mejor, 15, COLOR_ACENTO, 2)
        
        texto = fuente_pequena.render("MEJOR PUNTUACIÓN", True, COLOR_TEXTO_SECUNDARIO)
        texto_rect = texto.get_rect(center=(ANCHO // 2, 385))
        surf.blit(texto, texto_rect)
        
        valor = fuente_grande.render(f"{self.mejor_puntuacion}", True, COLOR_ACENTO)
        valor_rect = valor.get_rect(center=(ANCHO // 2, 425))
        surf.blit(valor, valor_rect)
        
        mouse_pos = pygame.mouse.get_pos()
        boton_jugar = pygame.Rect(ANCHO // 2 - 130, 620, 260, 70)
        hover = boton_jugar.collidepoint(mouse_pos)
        color_boton = (140, 90, 240) if hover else COLOR_BOTON
        dibujar_rect_redondeado_con_glow(surf, color_boton, boton_jugar, 15, 
                                          COLOR_ACENTO_2 if hover else COLOR_BORDE_GLOW, 3)
        
        texto_jugar = fuente_mediana.render("JUGAR", True, (255, 255, 255))
        texto_rect = texto_jugar.get_rect(center=boton_jugar.center)
        surf.blit(texto_jugar, texto_rect)
        
        instrucciones = [
            ("← → ↑ ↓  /  W A S D", "Mover fichas"),
            ("R", "Reiniciar juego"),
            ("ESC", "Pausa"),
        ]
        
        for i, (tecla, accion) in enumerate(instrucciones):
            y = 720 + i * 28
            t = fuente_pequena.render(tecla, True, COLOR_ACENTO_2)
            a = fuente_pequena.render(accion, True, COLOR_TEXTO_SECUNDARIO)
            t_rect = t.get_rect(right=ANCHO // 2 - 15, centery=y)
            a_rect = a.get_rect(left=ANCHO // 2 + 15, centery=y)
            surf.blit(t, t_rect)
            surf.blit(a, a_rect)
    
    def dibujar_juego(self, surf):
        self.dibujar_panel_puntuacion(surf)
        self.dibujar_tablero(surf)
        
        # Fichas encima
        for f in self.fichas:
            f.dibujar(surf)
        
        self.dibujar_panel_estadisticas(surf)
    
    def dibujar_panel_puntuacion(self, surf):
        panel_x, panel_y = TABLERO_X, TABLERO_Y - 130
        panel_ancho = TAMANO_TABLERO_PX
        
        panel_score = pygame.Rect(panel_x, panel_y, panel_ancho // 2 - 10, 110)
        dibujar_rect_redondeado_con_glow(surf, COLOR_TABLERO, panel_score, 15, COLOR_ACENTO, 2)
        
        texto = fuente_pequena.render("PUNTUACIÓN", True, COLOR_TEXTO_SECUNDARIO)
        surf.blit(texto, (panel_score.x + 20, panel_score.y + 18))
        
        valor_surf = fuente_grande.render(f"{self.puntuacion}", True, COLOR_ACENTO)
        surf.blit(valor_surf, (panel_score.x + 20, panel_score.y + 48))
        
        panel_mejor = pygame.Rect(panel_x + panel_ancho // 2 + 10, panel_y, 
                                   panel_ancho // 2 - 10, 110)
        dibujar_rect_redondeado_con_glow(surf, COLOR_TABLERO, panel_mejor, 15, COLOR_ACENTO_2, 2)
        
        texto = fuente_pequena.render("MEJOR", True, COLOR_TEXTO_SECUNDARIO)
        surf.blit(texto, (panel_mejor.x + 20, panel_mejor.y + 18))
        
        valor_surf = fuente_grande.render(f"{self.mejor_puntuacion}", True, COLOR_ACENTO_2)
        surf.blit(valor_surf, (panel_mejor.x + 20, panel_mejor.y + 48))
    
    def dibujar_tablero(self, surf):
        tablero_rect = pygame.Rect(TABLERO_X, TABLERO_Y, TAMANO_TABLERO_PX, TAMANO_TABLERO_PX)
        dibujar_rect_redondeado_con_glow(surf, COLOR_TABLERO, tablero_rect, 15, COLOR_BORDE, 4)
        
        for i in range(TAMANO_TABLERO):
            for j in range(TAMANO_TABLERO):
                x = TABLERO_X + ESPACIO_CELDA + j * (TAMANO_CELDA + ESPACIO_CELDA)
                y = TABLERO_Y + ESPACIO_CELDA + i * (TAMANO_CELDA + ESPACIO_CELDA)
                rect = pygame.Rect(x, y, TAMANO_CELDA, TAMANO_CELDA)
                pygame.draw.rect(surf, (35, 35, 55), rect, border_radius=10)
                pygame.draw.rect(surf, (50, 50, 80), rect, 1, border_radius=10)
    
    def dibujar_panel_estadisticas(self, surf):
        panel_x = TABLERO_X + TAMANO_TABLERO_PX + 30
        panel_y = TABLERO_Y
        panel_ancho = 300
        panel_alto = 500
        
        panel = pygame.Rect(panel_x, panel_y, panel_ancho, panel_alto)
        dibujar_rect_redondeado_con_glow(surf, COLOR_TABLERO, panel, 15, COLOR_BORDE, 3)
        
        titulo = fuente_mediana.render("ESTADÍSTICAS", True, COLOR_ACENTO)
        titulo_rect = titulo.get_rect(center=(panel_x + panel_ancho // 2, panel_y + 35))
        surf.blit(titulo, titulo_rect)
        
        pygame.draw.line(surf, COLOR_BORDE, 
                        (panel_x + 30, panel_y + 60), 
                        (panel_x + panel_ancho - 30, panel_y + 60), 2)
        
        stats = [
            ("Movimientos", str(self.movimientos), COLOR_TEXTO),
            ("Ficha máxima", str(self.max_ficha), COLOR_ACENTO),
            ("Tiempo", f"{self.tiempo_jugado // 60}:{self.tiempo_jugado % 60:02d}", COLOR_TEXTO),
        ]
        
        for i, (label, valor, color) in enumerate(stats):
            y = panel_y + 90 + i * 60
            label_surf = fuente_pequena.render(label, True, COLOR_TEXTO_SECUNDARIO)
            surf.blit(label_surf, (panel_x + 25, y))
            valor_surf = fuente_mediana.render(valor, True, color)
            surf.blit(valor_surf, (panel_x + 25, y + 25))
        
        # Barra de progreso
        progreso = min(1.0, self.max_ficha / 2048)
        barra_x = panel_x + 25
        barra_y = panel_y + 290
        barra_ancho = panel_ancho - 50
        barra_alto = 28
        
        texto = fuente_pequena.render(f"Progreso a 2048: {int(progreso*100)}%", True, COLOR_TEXTO_SECUNDARIO)
        surf.blit(texto, (barra_x, barra_y - 22))
        
        pygame.draw.rect(surf, (30, 30, 50), (barra_x, barra_y, barra_ancho, barra_alto), border_radius=14)
        
        if progreso > 0:
            ancho_prog = int(barra_ancho * progreso)
            for i in range(ancho_prog):
                t = i / max(1, ancho_prog)
                color = lerp_color((100, 200, 255), (255, 200, 60), t)
                pygame.draw.line(surf, color, (barra_x + i, barra_y + 4), 
                                (barra_x + i, barra_y + barra_alto - 4))
        
        pygame.draw.rect(surf, COLOR_BORDE, (barra_x, barra_y, barra_ancho, barra_alto), 2, border_radius=14)
        
        controles_y = panel_y + 360
        texto = fuente_pequena.render("CONTROLES", True, COLOR_ACENTO)
        surf.blit(texto, (panel_x + 25, controles_y))
        
        controles = ["← → ↑ ↓  Mover", "W A S D  Mover", "R  Reiniciar", "ESC  Pausa"]
        for i, c in enumerate(controles):
            texto = fuente_pequena.render(c, True, COLOR_TEXTO_SECUNDARIO)
            surf.blit(texto, (panel_x + 25, controles_y + 30 + i * 24))
    
    def dibujar_mensajes(self, surf):
        for msg in self.mensajes:
            t = (pygame.time.get_ticks() - msg['tiempo']) / msg['duracion']
            alpha = max(0, min(255, int(255 * (1 - t))))
            y_offset = -60 * t
            escala = 1.0 + 0.3 * (1 - t)
            
            fuente = obtener_fuente(int(36 * escala), bold=True)
            texto = fuente.render(msg['texto'], True, msg['color'])
            texto.set_alpha(alpha)
            
            rect = texto.get_rect(center=(msg['x'], msg['y'] + y_offset))
            surf.blit(texto, rect)
    
    def dibujar_pausa(self, surf):
        overlay = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surf.blit(overlay, (0, 0))
        
        panel = pygame.Rect(ANCHO // 2 - 250, ALTO // 2 - 250, 500, 500)
        dibujar_rect_redondeado_con_glow(surf, COLOR_TABLERO, panel, 20, COLOR_ACENTO, 4)
        
        titulo = fuente_titulo.render("PAUSA", True, COLOR_ACENTO)
        titulo_rect = titulo.get_rect(center=(ANCHO // 2, ALTO // 2 - 170))
        surf.blit(titulo, titulo_rect)
        
        stats = [
            f"Puntuación: {self.puntuacion}",
            f"Movimientos: {self.movimientos}",
            f"Ficha máxima: {self.max_ficha}",
        ]
        
        for i, stat in enumerate(stats):
            texto = fuente_mediana.render(stat, True, COLOR_TEXTO)
            texto_rect = texto.get_rect(center=(ANCHO // 2, ALTO // 2 - 60 + i * 40))
            surf.blit(texto, texto_rect)
        
        mouse_pos = pygame.mouse.get_pos()
        botones = [
            ("CONTINUAR", pygame.Rect(ANCHO // 2 - 140, 400, 280, 60)),
            ("REINICIAR", pygame.Rect(ANCHO // 2 - 140, 480, 280, 60)),
            ("MENÚ PRINCIPAL", pygame.Rect(ANCHO // 2 - 140, 560, 280, 60)),
        ]
        
        for texto, rect in botones:
            hover = rect.collidepoint(mouse_pos)
            color_final = (140, 90, 240) if hover else COLOR_BOTON
            dibujar_rect_redondeado_con_glow(surf, color_final, rect, 12, 
                                              COLOR_ACENTO_2 if hover else COLOR_BORDE, 3)
            t = fuente_mediana.render(texto, True, (255, 255, 255))
            t_rect = t.get_rect(center=rect.center)
            surf.blit(t, t_rect)
    
    def dibujar_game_over(self, surf):
        overlay = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        overlay.fill((40, 0, 0, 200))
        surf.blit(overlay, (0, 0))
        
        panel = pygame.Rect(ANCHO // 2 - 300, ALTO // 2 - 280, 600, 560)
        dibujar_rect_redondeado_con_glow(surf, COLOR_TABLERO, panel, 20, (255, 80, 80), 4)
        
        titulo = fuente_titulo.render("GAME OVER", True, (255, 80, 80))
        titulo_rect = titulo.get_rect(center=(ANCHO // 2, ALTO // 2 - 200))
        surf.blit(titulo, titulo_rect)
        
        stats = [
            ("Puntuación final", str(self.puntuacion), COLOR_ACENTO),
            ("Ficha máxima", str(self.max_ficha), COLOR_ACENTO_2),
            ("Movimientos", str(self.movimientos), COLOR_TEXTO),
            ("Tiempo", f"{self.tiempo_jugado // 60}:{self.tiempo_jugado % 60:02d}", COLOR_TEXTO),
        ]
        
        for i, (label, valor, color) in enumerate(stats):
            y = ALTO // 2 - 90 + i * 60
            label_surf = fuente_pequena.render(label, True, COLOR_TEXTO_SECUNDARIO)
            label_rect = label_surf.get_rect(center=(ANCHO // 2, y))
            surf.blit(label_surf, label_rect)
            
            valor_surf = fuente_grande.render(valor, True, color)
            valor_rect = valor_surf.get_rect(center=(ANCHO // 2, y + 28))
            surf.blit(valor_surf, valor_rect)
        
        mouse_pos = pygame.mouse.get_pos()
        botones = [
            ("JUGAR DE NUEVO", pygame.Rect(ANCHO // 2 - 140, 620, 280, 60)),
            ("MENÚ PRINCIPAL", pygame.Rect(ANCHO // 2 - 140, 700, 280, 60)),
        ]
        
        for texto, rect in botones:
            hover = rect.collidepoint(mouse_pos)
            color_final = (140, 90, 240) if hover else COLOR_BOTON
            dibujar_rect_redondeado_con_glow(surf, color_final, rect, 12, 
                                              COLOR_ACENTO if hover else COLOR_BORDE, 3)
            t = fuente_mediana.render(texto, True, (255, 255, 255))
            t_rect = t.get_rect(center=rect.center)
            surf.blit(t, t_rect)
    
    def dibujar_victoria(self, surf):
        overlay = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        overlay.fill((60, 40, 0, 180))
        surf.blit(overlay, (0, 0))
        
        panel = pygame.Rect(ANCHO // 2 - 300, ALTO // 2 - 280, 600, 560)
        dibujar_rect_redondeado_con_glow(surf, COLOR_TABLERO, panel, 20, COLOR_ACENTO, 5)
        
        titulo = fuente_titulo.render("¡VICTORIA!", True, COLOR_ACENTO)
        titulo_rect = titulo.get_rect(center=(ANCHO // 2, ALTO // 2 - 200))
        surf.blit(titulo, titulo_rect)
        
        subtitulo = fuente_mediana.render(f"¡Has alcanzado {self.max_ficha}!", True, COLOR_TEXTO)
        subtitulo_rect = subtitulo.get_rect(center=(ANCHO // 2, ALTO // 2 - 100))
        surf.blit(subtitulo, subtitulo_rect)
        
        stats = [
            ("Puntuación", str(self.puntuacion), COLOR_ACENTO),
            ("Movimientos", str(self.movimientos), COLOR_TEXTO),
            ("Tiempo", f"{self.tiempo_jugado // 60}:{self.tiempo_jugado % 60:02d}", COLOR_TEXTO),
        ]
        
        for i, (label, valor, color) in enumerate(stats):
            y = ALTO // 2 - 20 + i * 50
            label_surf = fuente_pequena.render(label, True, COLOR_TEXTO_SECUNDARIO)
            label_rect = label_surf.get_rect(center=(ANCHO // 2, y))
            surf.blit(label_surf, label_rect)
            
            valor_surf = fuente_mediana.render(valor, True, color)
            valor_rect = valor_surf.get_rect(center=(ANCHO // 2, y + 25))
            surf.blit(valor_surf, valor_rect)
        
        mouse_pos = pygame.mouse.get_pos()
        botones = [
            ("SEGUIR JUGANDO", pygame.Rect(ANCHO // 2 - 140, 620, 280, 60)),
            ("MENÚ PRINCIPAL", pygame.Rect(ANCHO // 2 - 140, 700, 280, 60)),
        ]
        
        for texto, rect in botones:
            hover = rect.collidepoint(mouse_pos)
            color_final = (140, 90, 240) if hover else COLOR_BOTON
            dibujar_rect_redondeado_con_glow(surf, color_final, rect, 12, 
                                              COLOR_ACENTO if hover else COLOR_BORDE, 3)
            t = fuente_mediana.render(texto, True, (255, 255, 255))
            t_rect = t.get_rect(center=rect.center)
            surf.blit(t, t_rect)
    
    def correr(self):
        corriendo = True
        while corriendo:
            corriendo = self.manejar_eventos()
            self.actualizar()
            self.dibujar()
            self.reloj.tick(FPS)

# =============================================================================
# MAIN
# =============================================================================

def main():
    print("=" * 60)
    print("  2048 - CON ANIMACIONES DE MOVIMIENTO")
    print("=" * 60)
    
    try:
        juego = Juego2048()
        juego.correr()
    except KeyboardInterrupt:
        print("\nJuego interrumpido")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        pygame.quit()
        print("¡Gracias por jugar!")

if __name__ == "__main__":
    main()