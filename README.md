# Minesweeper (Buscaminas) - FCEN UBA 💣

![Python](https://img.shields.io/badge/python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Testing](https://img.shields.io/badge/coverage-95%25-green?style=for-the-badge)
![UBA](https://img.shields.io/badge/Institution-FCEN%20UBA-lightgrey?style=for-the-badge)

## 📋 Descripción
Implementación completa del clásico juego **Buscaminas** desarrollada como Trabajo Práctico Final para la materia *Introducción a la Programación* de la **Universidad de Buenos Aires (FCEN)**.

El proyecto se centra en la **Programación Imperativa**, el manejo de estados complejos y la persistencia de datos, siguiendo estrictas normas de codificación y tipado estático.

## 🚀 Características Técnicas
Basado en la especificación formal del TP, el sistema incluye:

### 🧠 Lógica de Juego
* **Motor de Estado:** Gestión centralizada del estado del juego mediante un diccionario tipado (`EstadoJuego`) que controla el tablero oculto, el tablero visible y las banderas.
* **Algoritmo de Expansión (Flood Fill):** Implementación de la función `caminos_descubiertos` para generar el "efecto cascada" que desbloquea automáticamente áreas vacías contiguas al descubrir una celda segura.
* **Generación Aleatoria:** Distribución uniforme de minas utilizando `random.sample` para asegurar partidas únicas.

### 💾 Persistencia de Datos (I/O)
Sistema robusto para **Guardar y Cargar partidas** en disco:
* **Serialización:** Exporta el estado actual a archivos de texto plano (`tablero.txt`, `tablero_visible.txt`) separados por comas.
* **Validación de Integridad:** Al cargar una partida, el sistema verifica la coherencia entre el tablero lógico y el visible, detecta corrupción de archivos y valida dimensiones.

### 🧪 Testing & Calidad
* **Cobertura:** Suite de pruebas unitarias (`unittest`) que garantiza una cobertura de código superior al **95%** (líneas y ramas), requisito obligatorio de la cátedra.
* **Tipado:** Uso estricto de sugerencias de tipo (Type Hinting) para todas las funciones.

## 📂 Estructura del Proyecto

```bash
├── buscaminas.py           # 🧠 Lógica del juego (Backend implementado)
├── interfaz_buscaminas.py  # 🖥️ GUI (Provee la interacción visual, provisto por cátedra)
├── tests/                  # 🧪 Suite de tests unitarios
├── CARGAR/                 # 📂 Directorio para importar partidas (.txt)
├── RUTA_VACIA/             # 📂 Directorio para un test
├── GUARDAR/                # 💾 Directorio donde se guardan las partidas
└── Enunciado.pdf           # 📄 Especificación oficial del TP
