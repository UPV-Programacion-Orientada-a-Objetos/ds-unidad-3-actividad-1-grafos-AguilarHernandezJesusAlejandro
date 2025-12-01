# NeuroNet - Guía de Uso

## Descripción

**NeuroNet** es un sistema híbrido de análisis de grafos masivos que combina:
- **Backend C++** con matrices dispersas CSR (Compressed Sparse Row) para eficiencia de memoria
- **Cython** para integración Python-C++
- **GUI Python** con Tkinter y NetworkX para visualización

## Requisitos Previos

### 1. Compilador C++

**Windows:**
- Visual Studio Build Tools 2017 o superior, O
- MinGW-w64

**Linux/Mac:**
- GCC 5.0+ o Clang 3.4+

### 2. Python

- Python 3.7 o superior
- pip (gestor de paquetes)

## Instalación

### Paso 1: Instalar Dependencias de Python

```bash
pip install cython networkx matplotlib
```

### Paso 2: Compilar el Módulo Cython

Desde el directorio raíz del proyecto:

```bash
python setup.py build_ext --inplace
```

**Nota para Windows:** Si usas Visual Studio, asegúrate de ejecutar desde "Developer Command Prompt for VS".

**Solución de problemas:**
- Si obtienes errores de compilación, verifica que tienes un compilador C++ instalado
- En Windows, puede ser necesario instalar Visual Studio Build Tools desde: https://visualstudio.microsoft.com/downloads/

### Paso 3: Verificar la Instalación

```bash
python -c "import grafo_wrapper; print('Módulo importado correctamente')"
```

## Uso

### Ejecutar la Interfaz Gráfica

```bash
python neuronet_gui.py
```

### Flujo de Trabajo

1. **Cargar Dataset:**
   - Haz clic en "📁 Cargar Dataset"
   - Selecciona un archivo de lista de aristas (formato: `nodo_origen nodo_destino`)
   - El sistema mostrará las métricas del grafo

2. **Analizar el Grafo:**
   - Las métricas se actualizan automáticamente:
     - Número de nodos
     - Número de aristas
     - Memoria utilizada (en MB)
     - Nodo con mayor grado

3. **Ejecutar BFS:**
   - Ingresa el nodo de inicio (ej: `0`)
   - Ingresa la profundidad máxima (ej: `2`)
   - Haz clic en "🔍 Ejecutar BFS"
   - La visualización mostrará el subgrafo explorado

### Dataset de Prueba

El proyecto incluye un dataset de prueba en `data/sample_data.txt` con 20 nodos.

Para probar con datasets más grandes, descarga desde SNAP (Stanford Network Analysis Project):
- https://snap.stanford.edu/data/

Ejemplos:
- `web-Google.txt`: 875,713 nodos, 5,105,039 aristas
- `amazon0601.txt`: 403,394 nodos, 3,387,388 aristas

## Formato de Datos

Los archivos de entrada deben ser listas de aristas en formato texto plano:

```
# Comentarios comienzan con #
0 1
0 2
1 3
2 3
...
```

Cada línea representa una arista dirigida de `nodo_origen` a `nodo_destino`.

## Arquitectura del Sistema

```
┌─────────────────────────────────────┐
│     Python GUI (neuronet_gui.py)    │
│         Tkinter + NetworkX          │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│   Cython Wrapper (grafo_wrapper)    │
│    Conversión Python ↔ C++          │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│    C++ Core (GrafoDisperso.cpp)     │
│  CSR Sparse Matrix + BFS Manual     │
└─────────────────────────────────────┘
```

## Características Principales

### Eficiencia de Memoria

El formato CSR reduce drásticamente el uso de memoria:
- **Matriz densa:** O(N²) memoria
- **CSR:** O(N + E) memoria

Para un grafo con 1M nodos y 5M aristas:
- Matriz densa: ~4 TB de RAM
- CSR: ~40 MB de RAM

### Algoritmos Implementados

1. **BFS (Breadth-First Search):**
   - Implementación manual con cola
   - Retorna nodos visitados y distancias
   - Complejidad: O(V + E)

2. **Cálculo de Grado:**
   - Encuentra el nodo con más conexiones
   - Útil para identificar nodos críticos

## Ejemplos de Uso

### Ejemplo 1: Análisis de Red Pequeña

```bash
# 1. Ejecutar GUI
python neuronet_gui.py

# 2. Cargar data/sample_data.txt
# 3. Ejecutar BFS desde nodo 0, profundidad 2
# 4. Observar la visualización tipo "estrella"
```

### Ejemplo 2: Uso Programático

```python
import grafo_wrapper

# Crear instancia del grafo
grafo = grafo_wrapper.PyGrafoDisperso()

# Cargar datos
grafo.cargar_datos("data/sample_data.txt")

# Obtener métricas
print(f"Nodos: {grafo.get_num_nodos()}")
print(f"Aristas: {grafo.get_num_aristas()}")

# Ejecutar BFS
resultado = grafo.bfs(nodo_inicio=0, profundidad_maxima=2)
print(f"Nodos encontrados: {len(resultado)}")

# Encontrar nodo más importante
nodo_max, grado_max = grafo.get_nodo_mayor_grado()
print(f"Nodo con mayor grado: {nodo_max} (grado: {grado_max})")
```

## Salida de Consola

El backend C++ imprime logs de operación:

```
[C++ Core] Inicializando GrafoDisperso...
[C++ Core] Cargando dataset 'sample_data.txt'...
[C++ Core] Carga completa. Nodos: 20 | Aristas: 44
[C++ Core] Estructura CSR construida. Memoria estimada: 0 MB.
[C++ Core] Tiempo de carga: 2 ms.
[Cython] Solicitud recibida: BFS desde Nodo 0, Profundidad 2.
[C++ Core] Ejecutando BFS nativo...
[C++ Core] Nodos encontrados: 14. Tiempo ejecución: 0.015ms.
[Cython] Retornando lista de adyacencia local a Python.
```

## Solución de Problemas

### Error: "No se pudo importar el módulo 'grafo_wrapper'"

**Solución:** Compila el módulo primero:
```bash
python setup.py build_ext --inplace
```

### Error de compilación en Windows

**Solución:** Instala Visual Studio Build Tools o MinGW-w64.

### Error: "Faltan dependencias"

**Solución:** Instala las librerías de Python:
```bash
pip install cython networkx matplotlib
```

### El grafo no se visualiza correctamente

**Solución:** 
- Verifica que el archivo de datos esté en formato correcto
- Para grafos muy grandes (>1000 nodos), la visualización puede ser lenta
- Usa profundidades pequeñas (1-3) para grafos grandes

## Rendimiento Esperado

| Tamaño del Grafo | Tiempo de Carga | Memoria | Tiempo BFS (prof. 2) |
|------------------|-----------------|---------|----------------------|
| 100 nodos        | < 1 ms          | < 1 MB  | < 0.1 ms             |
| 10,000 nodos     | < 100 ms        | ~5 MB   | < 1 ms               |
| 100,000 nodos    | < 1 s           | ~50 MB  | < 10 ms              |
| 1,000,000 nodos  | < 10 s          | ~500 MB | < 100 ms             |

## Licencia

Este proyecto fue desarrollado como parte de la actividad académica de Estructuras de Datos.

## Contacto y Soporte

Para reportar problemas o sugerencias, consulta con tu instructor del curso.
