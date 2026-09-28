```markdown
# 🎮 2048 — Premium Edition

> Un remake moderno del clásico juego de rompecabezas numérico **2048**, construido con **Python + Pygame**.
> Con animaciones fluidas, diseño tipo *glassmorphism* y una estética premium inspirada en apps comerciales.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame-2.5%2B-green?style=for-the-badge&logo=pygame&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

---

## 📖 Descripción

**2048 Premium Edition** es una reimaginación visual del clásico juego 2048. A diferencia de la versión original web, esta incluye:

- ✨ **Animaciones suaves de deslizamiento** para cada movimiento
- 🎨 **Diseño glassmorphism** con tarjetas translúcidas y glow
- 🌈 **Sistema de colores progresivo** que evoluciona con el valor de las fichas
- 📊 **Panel de estadísticas en tiempo real** (movimientos, tiempo, ficha máxima)
- 🏆 **Sistema de puntuaciones persistentes** (mejor puntuación guardada en archivo)
- 🎬 **Pantallas de pausa, victoria y game over** con diseño profesional
- 🎯 **Barra de progreso** visual hacia el objetivo 2048

---

## 🎯 Cómo se juega

### Objetivo

Llega a la ficha **2048** deslizando fichas en una cuadrícula de 4×4.

### Reglas

1. Usa las **flechas** (o **WASD**) para mover todas las fichas en una dirección.
2. Cuando **dos fichas del mismo número** chocan, se **fusionan** en una sola con el doble de valor.
3. Después de cada movimiento aparece una nueva ficha (**2** el 90% del tiempo, **4** el 10%).
4. El juego termina cuando **no quedan movimientos posibles**.
5. Ganas al alcanzar la ficha **2048** (puedes seguir jugando para conseguir puntuaciones más altas).

---

## 🕹️ Controles

| Tecla | Acción |
|:-----:|:-------|
| `←` `→` `↑` `↓` | Mover fichas |
| `A` `D` `W` `S` | Mover fichas (alternativo) |
| `R` | Reiniciar partida |
| `ESC` | Pausa / Volver al menú |
| `ENTER` / `ESPACIO` | Iniciar juego / Confirmar |
| Click del ratón | Interactuar con botones |

---

## 🚀 Instalación

### Requisitos previos

- **Python 3.10 o superior**
- **pip** (gestor de paquetes de Python)

### Paso 1 — Clonar el repositorio

```bash
git clone https://github.com/Alejandro-mendieta/Playgame2048.git
cd Playgame2048
```

### Paso 2 — Instalar dependencias

```bash
pip install pygame
```

> 💡 **Recomendación:** usa `pygame-ce` (Community Edition) para mejor rendimiento:
>
> ```bash
> pip install pygame-ce
> ```
>
> Es un reemplazo directo: tu código sigue usando `import pygame`.

### Paso 3 — Ejecutar el juego

```bash
python3 app.py
```

---

## 🎨 Características de diseño

### Paleta de colores

El juego utiliza una paleta personalizada con 4 gradientes principales:

| Elemento | Gradiente |
|----------|-----------|
| **Fondo** | `#0D006E` → `#616E00` |
| **Tablero y paneles** | `#6E4B00` → `#00236E` |
| **Fichas** | `#FFBA66` → `#66ABFF` |
| **Acentos** | `#FF0000` → `#00FFFF` |

### Colores de fichas por valor

| Valor | Color |
|-------|-------|
| 2, 4 | Beige/crema cálido |
| 8, 16 | Naranja claro → intenso |
| 32, 64 | Coral → rojo coral |
| 128, 256, 512 | Rosa → púrpura → índigo |
| 1024, 2048 | Azul brillante → cyan premium |
| 4096, 8192+ | Verde esmeralda → dorado → magenta |

---

## 📁 Estructura del proyecto

```
Playgame2048/
│
├── app.py                        # Código principal del juego
├── README.md                     # Este archivo
├── 2048_premium_mejor.txt        # Mejor puntuación (autogenerado)
└── 2048_premium_historial.json   # Historial de partidas (autogenerado)
```

---

## ⚙️ Detalles técnicos

### Arquitectura

- **`Ficha`**: clase que representa una ficha individual con posición visual, animación de spawn, deslizamiento y eliminación.
- **`Juego2048`**: clase principal que gestiona estado, eventos, lógica y renderizado.
- **Grid lógico**: matriz 4×4 de valores enteros.
- **Fichas visuales**: lista independiente que se sincroniza con el grid para permitir animaciones.

### Sistema de animación

- **Deslizamiento**: interpolación lineal (`lerp`) hacia la posición objetivo.
- **Spawn**: escala de 0 a 1 con `ease_out_cubic` (160 ms).
- **Eliminación** (fusiones): escala de 1 a 0 (110 ms).
- **Sin screen shake**: los movimientos son puramente horizontales/verticales.

### Persistencia

- Mejor puntuación en `2048_premium_mejor.txt`.
- Historial en `2048_premium_historial.json`.

---

## 💡 Consejos para ganar

1. **Mantén la ficha más alta en una esquina** y no la muevas de ahí.
2. **Ordena los números de mayor a menor** desde esa esquina.
3. **Usa solo 2 direcciones** al principio para no romper el orden.
4. **Rellena primero las filas/columnas de la esquina elegida** antes de expandirte.
5. **No persigas fusiones grandes**; mantén siempre la esquina limpia.

---


---

## 🛠️ Tecnologías usadas

- **Python 3.10+**
- **Pygame / pygame-ce 2.5+**
- **math**, **random**, **json**

---

## 🔮 Roadmap

- [ ] Soporte para deshacer movimiento (undo)
- [ ] Modo oscuro/claro conmutable
- [ ] Tamaños de tablero configurables (3×3, 5×5)
- [ ] Sonidos y música de fondo
- [ ] Leaderboard local
- [ ] Modo contrarreloj
- [ ] IA que juegue sola (modo demo)

---

## 🤝 Contribuciones

1. Haz un **fork** del proyecto.
2. Crea una rama: `git checkout -b feature/nueva-funcionalidad`.
3. Haz commit: `git commit -m 'Añade nueva funcionalidad'`.
4. Push: `git push origin feature/nueva-funcionalidad`.
5. Abre un **Pull Request**.

---

## 📄 Licencia

Este proyecto está bajo la licencia **MIT**. Consulta el archivo [LICENSE](LICENSE) para más detalles.

---

## 👤 Autor

**Alejandro Mendieta**

- GitHub: [@Alejandro-mendieta](https://github.com/Alejandro-mendieta)

---

## 🙏 Agradecimientos

- Inspirado en el [2048 original de Gabriele Cirulli](https://github.com/gabrielecirulli/2048).
- Comunidad de **Pygame** por las herramientas.

---

<div align="center">

**⭐ Si te gustó el proyecto, dale una estrella en GitHub ⭐**

Hecho con ❤️ y Python

</div>