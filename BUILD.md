# NeuroNet: Instrucciones de Compilación y Ejecución

## Paso 1: Instalar Dependencias

```bash
pip install -r requirements.txt
```

Esto instalará:
- Cython (para compilar el código C++)
- NetworkX (para visualización de grafos)
- Matplotlib (para renderizado gráfico)

## Paso 2: Compilar el Módulo C++

```bash
python setup.py build_ext --inplace
```

**Nota:** En Windows, si tienes problemas de compilación, asegúrate de tener instalado Visual Studio Build Tools.

## Paso 3: Ejecutar Tests

```bash
python test_grafo.py
```

Esto verificará que todo funcione correctamente.

## Paso 4: Ejecutar la Aplicación

```bash
python neuronet_gui.py
```

## Estructura del Proyecto

```
ds-unidad-3-actividad-1-grafos/
│
├── src/                          # Código fuente C++
│   ├── GrafoBase.h              # Clase abstracta base
│   ├── GrafoDisperso.h          # Implementación CSR
│   └── GrafoDisperso.cpp        # Implementación CSR
│
├── cython/                       # Capa de integración
│   ├── grafo_wrapper.pxd        # Declaraciones C++
│   └── grafo_wrapper.pyx        # Wrapper Python
│
├── data/                         # Datasets
│   └── sample_data.txt          # Dataset de prueba
│
├── setup.py                      # Configuración de compilación
├── neuronet_gui.py              # Interfaz gráfica
├── test_grafo.py                # Suite de pruebas
├── requirements.txt             # Dependencias Python
├── USAGE.md                     # Guía de uso completa
└── README.md                    # Descripción del proyecto
```

## Solución de Problemas Comunes

### Error: "No se pudo importar grafo_wrapper"

**Causa:** El módulo no está compilado.

**Solución:**
```bash
python setup.py build_ext --inplace
```

### Error de compilación en Windows

**Causa:** Falta compilador C++.

**Solución:** Instala Visual Studio Build Tools desde:
https://visualstudio.microsoft.com/downloads/

### Error: "Faltan dependencias"

**Solución:**
```bash
pip install -r requirements.txt
```
