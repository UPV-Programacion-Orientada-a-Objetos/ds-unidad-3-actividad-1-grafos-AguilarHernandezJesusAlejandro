#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test suite para NeuroNet
Prueba las funcionalidades del grafo C++ desde Python
"""

import sys
import os

# Intentar importar el módulo compilado
try:
    import grafo_wrapper
except ImportError:
    print("ERROR: No se pudo importar grafo_wrapper.")
    print("Compila el módulo primero con: python setup.py build_ext --inplace")
    sys.exit(1)


def test_carga_datos():
    """Test: Cargar datos desde archivo"""
    print("\n=== Test 1: Carga de Datos ===")
    
    grafo = grafo_wrapper.PyGrafoDisperso()
    
    # Intentar cargar el dataset de prueba
    archivo = "data/sample_data.txt"
    if not os.path.exists(archivo):
        print(f"❌ FALLO: Archivo {archivo} no encontrado")
        return False
    
    exito = grafo.cargar_datos(archivo)
    
    if exito:
        print(f"✓ Datos cargados correctamente desde {archivo}")
        print(f"  Nodos: {grafo.get_num_nodos()}")
        print(f"  Aristas: {grafo.get_num_aristas()}")
        return True
    else:
        print("❌ FALLO: No se pudieron cargar los datos")
        return False


def test_metricas_basicas():
    """Test: Métricas básicas del grafo"""
    print("\n=== Test 2: Métricas Básicas ===")
    
    grafo = grafo_wrapper.PyGrafoDisperso()
    grafo.cargar_datos("data/sample_data.txt")
    
    num_nodos = grafo.get_num_nodos()
    num_aristas = grafo.get_num_aristas()
    memoria = grafo.get_memoria_estimada()
    
    print(f"  Nodos: {num_nodos}")
    print(f"  Aristas: {num_aristas}")
    print(f"  Memoria: {memoria / 1024:.2f} KB")
    
    if num_nodos > 0 and num_aristas > 0:
        print("✓ Métricas obtenidas correctamente")
        return True
    else:
        print("❌ FALLO: Métricas inválidas")
        return False


def test_nodo_mayor_grado():
    """Test: Encontrar nodo con mayor grado"""
    print("\n=== Test 3: Nodo con Mayor Grado ===")
    
    grafo = grafo_wrapper.PyGrafoDisperso()
    grafo.cargar_datos("data/sample_data.txt")
    
    nodo_max, grado_max = grafo.get_nodo_mayor_grado()
    
    print(f"  Nodo con mayor grado: {nodo_max}")
    print(f"  Grado: {grado_max}")
    
    if nodo_max >= 0 and grado_max > 0:
        print("✓ Nodo con mayor grado encontrado")
        return True
    else:
        print("❌ FALLO: No se pudo encontrar el nodo con mayor grado")
        return False


def test_bfs():
    """Test: Búsqueda BFS"""
    print("\n=== Test 4: Búsqueda BFS ===")
    
    grafo = grafo_wrapper.PyGrafoDisperso()
    grafo.cargar_datos("data/sample_data.txt")
    
    nodo_inicio = 0
    profundidad = 2
    
    resultado = grafo.bfs(nodo_inicio, profundidad)
    
    print(f"  BFS desde nodo {nodo_inicio}, profundidad {profundidad}")
    print(f"  Nodos encontrados: {len(resultado)}")
    
    if len(resultado) > 0:
        print(f"  Primeros 5 nodos: {resultado[:5]}")
        print("✓ BFS ejecutado correctamente")
        return True
    else:
        print("❌ FALLO: BFS no retornó resultados")
        return False


def test_vecinos():
    """Test: Obtener vecinos de un nodo"""
    print("\n=== Test 5: Vecinos de Nodo ===")
    
    grafo = grafo_wrapper.PyGrafoDisperso()
    grafo.cargar_datos("data/sample_data.txt")
    
    nodo = 0
    vecinos = grafo.get_vecinos(nodo)
    
    print(f"  Vecinos del nodo {nodo}: {vecinos}")
    print(f"  Número de vecinos: {len(vecinos)}")
    
    if len(vecinos) > 0:
        print("✓ Vecinos obtenidos correctamente")
        return True
    else:
        print("⚠ Advertencia: El nodo no tiene vecinos (puede ser normal)")
        return True


def test_grado_nodo():
    """Test: Obtener grado de un nodo específico"""
    print("\n=== Test 6: Grado de Nodo Específico ===")
    
    grafo = grafo_wrapper.PyGrafoDisperso()
    grafo.cargar_datos("data/sample_data.txt")
    
    nodo = 0
    grado = grafo.obtener_grado(nodo)
    
    print(f"  Grado del nodo {nodo}: {grado}")
    
    if grado >= 0:
        print("✓ Grado obtenido correctamente")
        return True
    else:
        print("❌ FALLO: Grado inválido")
        return False


def test_bfs_profundidades():
    """Test: BFS con diferentes profundidades"""
    print("\n=== Test 7: BFS con Diferentes Profundidades ===")
    
    grafo = grafo_wrapper.PyGrafoDisperso()
    grafo.cargar_datos("data/sample_data.txt")
    
    nodo_inicio = 0
    
    for prof in [1, 2, 3]:
        resultado = grafo.bfs(nodo_inicio, prof)
        print(f"  Profundidad {prof}: {len(resultado)} nodos encontrados")
    
    print("✓ BFS con diferentes profundidades ejecutado")
    return True


def test_todas_las_aristas():
    """Test: Obtener todas las aristas"""
    print("\n=== Test 8: Obtener Todas las Aristas ===")
    
    grafo = grafo_wrapper.PyGrafoDisperso()
    grafo.cargar_datos("data/sample_data.txt")
    
    aristas = grafo.get_todas_las_aristas()
    
    print(f"  Total de aristas: {len(aristas)}")
    print(f"  Primeras 5 aristas: {aristas[:5]}")
    
    if len(aristas) > 0:
        print("✓ Aristas obtenidas correctamente")
        return True
    else:
        print("❌ FALLO: No se obtuvieron aristas")
        return False


def main():
    """Ejecuta todos los tests"""
    print("=" * 60)
    print("SUITE DE PRUEBAS PARA NEURONET")
    print("=" * 60)
    
    tests = [
        test_carga_datos,
        test_metricas_basicas,
        test_nodo_mayor_grado,
        test_bfs,
        test_vecinos,
        test_grado_nodo,
        test_bfs_profundidades,
        test_todas_las_aristas,
    ]
    
    resultados = []
    
    for test in tests:
        try:
            resultado = test()
            resultados.append(resultado)
        except Exception as e:
            print(f"❌ ERROR en {test.__name__}: {e}")
            resultados.append(False)
    
    # Resumen
    print("\n" + "=" * 60)
    print("RESUMEN DE PRUEBAS")
    print("=" * 60)
    
    exitosos = sum(resultados)
    total = len(resultados)
    
    print(f"Tests exitosos: {exitosos}/{total}")
    print(f"Tests fallidos: {total - exitosos}/{total}")
    
    if exitosos == total:
        print("\n🎉 ¡TODOS LOS TESTS PASARON!")
        return 0
    else:
        print("\n⚠ ALGUNOS TESTS FALLARON")
        return 1


if __name__ == "__main__":
    sys.exit(main())
