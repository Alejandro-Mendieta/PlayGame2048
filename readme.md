# 🎮 2048

> Un remake moderno del clásico juego de rompecabezas numérico **2048**, construido con **Python + Pygame**.
>
> Con animaciones fluidas, diseño tipo *glassmorphism* y una estética inspirada en aplicaciones comerciales.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge\&logo=python\&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame-2.5%2B-green?style=for-the-badge\&logo=pygame\&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

---

## 📖 Descripción

**2048** es una reimaginación visual del clásico juego 2048. A diferencia de la versión web original, esta edición incluye:

* ✨ **Animaciones suaves de deslizamiento** para cada movimiento.
* 🎨 **Diseño glassmorphism** con tarjetas translúcidas y efectos de brillo.
* 🌈 **Sistema de colores progresivo** que evoluciona con el valor de las fichas.
* 📊 **Panel de estadísticas en tiempo real** con movimientos, tiempo y ficha máxima.
* 🏆 **Sistema de puntuaciones persistentes**, con la mejor puntuación guardada en un archivo.
* 🎬 **Pantallas de pausa, victoria y Game Over** con un diseño personalizado.
* 🎯 **Barra de progreso** visual hacia el objetivo de 2048.

---

## 🎯 Cómo se juega

### Objetivo

Llega a la ficha **2048** deslizando las fichas dentro de una cuadrícula de **4 × 4**.

### Reglas

1. Usa las **flechas** o **WASD** para mover todas las fichas en una dirección.
2. Cuando **dos fichas con el mismo número** chocan, se fusionan en una sola con el doble de valor.
3. Después de cada movimiento válido aparece una nueva ficha: **2** el 90 % de las veces y **4** el 10 %.
4. El juego termina cuando **no quedan movimientos posibles**.
5. Ganas al alcanzar la ficha **2048**, aunque puedes continuar jugando para conseguir puntuaciones más altas.

---

## 🕹️ Controles

|        Tecla        | Acción                      |
| :-----------------: | --------------------------- |
|   `←` `→` `↑` `↓`   | Mover fichas                |
|   `A` `D` `W` `S`   | Mover fichas (alternativo)  |
|         `R`         | Reiniciar partida           |
|        `ESC`        | Pausar / volver al menú     |
| `ENTER` / `ESPACIO` | Iniciar juego / confirmar   |
|   Click del ratón   | Interactuar con los botones |

---

## 🚀 Instalación

### Requisitos previos

* **Python 3.10 o superior**
* **pip** (gestor de paquetes de Python)

### Paso 1 — Clonar el repositorio

```bash
git clone https://github.com/Alejandro-mendieta/Playgame2048.git
cd Playgame2048
```

### Paso 2 — Instalar dependencias

Puedes instalar Pygame mediante:

```bash
pip install pygame
```

También puedes utilizar **pygame-ce (Community Edition)**:

```bash
pip install pygame-ce
```

> 💡 `pygame-ce` es compatible con el código que utiliza `import pygame`.

### Paso 3 — Ejecutar el juego

```bash
python app.py
```

En algunos sistemas también puedes utilizar:

```bash
python3 app.py
```

---

## 🎨 Características de diseño

### Paleta de colores

El juego utiliza una paleta personalizada con cuatro gradientes principales:

| Elemento              | Gradiente             |
| --------------------- | --------------------- |
| **Fondo**             | `#0D006E` → `#616E00` |
| **Tablero y paneles** | `#6E4B00` → `#00236E` |
| **Fichas**            | `#FFBA66` → `#66ABFF` |
| **Acentos**           | `#FF0000` → `#00FFFF` |

### Colores de fichas por valor

|         Valor | Color                              |
| ------------: | ---------------------------------- |
|          2, 4 | Beige / crema cálido               |
|         8, 16 | Naranja claro → intenso            |
|        32, 64 | Coral → rojo coral                 |
| 128, 256, 512 | Rosa → púrpura → índigo            |
|    1024, 2048 | Azul brillante → cyan              |
|   4096, 8192+ | Verde esmeralda → dorado → magenta |

---

## 📁 Estructura del proyecto

```text
Playgame2048/
│
├── app.py                        # Código principal del juego
├── README.md                     # Documentación del proyecto
├── 2048_premium_mejor.txt        # Mejor puntuación (autogenerado)
└── 2048_premium_historial.json   # Historial de partidas (autogenerado)
```

---

## ⚙️ Detalles técnicos

### Arquitectura

* **`Ficha`**: clase que representa una ficha individual con posición visual, animación de aparición, deslizamiento y eliminación.
* **`Juego2048`**: clase principal que gestiona el estado del juego, los eventos, la lógica y el renderizado.
* **Grid lógico**: matriz de valores enteros de **4 × 4**.
* **Fichas visuales**: lista independiente que se sincroniza con el grid para permitir animaciones fluidas.

### Sistema de animación

* **Deslizamiento**: interpolación lineal (`lerp`) hacia la posición objetivo.
* **Spawn**: escala de 0 a 1 mediante `ease_out_cubic` durante aproximadamente 160 ms.
* **Eliminación**: escala de 1 a 0 durante aproximadamente 110 ms al realizar fusiones.
* **Sin screen shake**: los movimientos mantienen una experiencia visual limpia, sin sacudidas de pantalla.

### Persistencia

* Mejor puntuación: `2048_premium_mejor.txt`
* Historial de partidas: `2048_premium_historial.json`

---

## 💡 Consejos para ganar

1. **Mantén la ficha de mayor valor en una esquina** y evita moverla innecesariamente.
2. **Ordena los números de mayor a menor** desde esa esquina.
3. **Utiliza principalmente dos direcciones** al principio para mantener el orden del tablero.
4. **Completa primero las filas o columnas cercanas a la esquina elegida** antes de expandirte.
5. **No persigas fusiones grandes constantemente**; prioriza mantener el tablero organizado.

---

## 🛠️ Tecnologías utilizadas

* **Python 3.10+**
* **Pygame / pygame-ce 2.5+**
* **math**
* **random**
* **json**

---

## 🔮 Roadmap

* [ ] Soporte para deshacer movimientos (*undo*)
* [ ] Modo oscuro / claro conmutable
* [ ] Tamaños de tablero configurables (3 × 3, 5 × 5)
* [ ] Sonidos y música de fondo
* [ ] Leaderboard local
* [ ] Modo contrarreloj
* [ ] IA que juegue automáticamente (modo demo)

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas.

1. Haz un **fork** del proyecto.
2. Crea una nueva rama:

```bash
git checkout -b feature/nueva-funcionalidad
```

3. Realiza tus cambios y crea un commit:

```bash
git commit -m "Añade nueva funcionalidad"
```

4. Envía la rama al repositorio:

```bash
git push origin feature/nueva-funcionalidad
```

5. Abre un **Pull Request**.

---

## 📄 Licencia

Este proyecto está bajo la licencia **MIT**.

Consulta el archivo [LICENSE](LICENSE) para obtener más información.

---

## 👤 Autor

**Alejandro Mendieta**

* GitHub: [@Alejandro-mendieta](https://github.com/Alejandro-mendieta)

---

## 🙏 Agradecimientos

* Inspirado en el [2048 original de Gabriele Cirulli](https://github.com/gabrielecirulli/2048).
* Agradecimientos a la comunidad de **Pygame** por las herramientas y recursos disponibles.

---

<div align="center">

### ⭐ Si te gustó el proyecto, ¡dale una estrella en GitHub! ⭐

Hecho con ❤️ y Python

</div>
