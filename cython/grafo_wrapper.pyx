# distutils: language = c++
# cython: language_level=3

from grafo_wrapper cimport GrafoDisperso
from libcpp.vector cimport vector
from libcpp.pair cimport pair
from libcpp.string cimport string

cdef class PyGrafoDisperso:
    """
    Wrapper de Python para la clase C++ GrafoDisperso.
    Permite usar el motor de grafos C++ desde Python.
    """
    cdef GrafoDisperso* c_grafo  # Puntero a la instancia C++
    
    def __cinit__(self):
        """Constructor: crea una instancia del grafo C++"""
        self.c_grafo = new GrafoDisperso()
    
    def __dealloc__(self):
        """Destructor: libera la memoria del grafo C++"""
        del self.c_grafo
    
    def cargar_datos(self, str nombre_archivo):
        """
        Carga datos desde un archivo de lista de aristas.
        
        Args:
            nombre_archivo: Ruta al archivo de datos
            
        Returns:
            True si la carga fue exitosa, False en caso contrario
        """
        cdef string cpp_nombre = nombre_archivo.encode('utf-8')
        return self.c_grafo.cargarDatos(cpp_nombre)
    
    def bfs(self, int nodo_inicio, int profundidad_maxima):
        """
        Realiza una búsqueda en anchura (BFS) desde un nodo inicial.
        
        Args:
            nodo_inicio: Nodo desde donde comenzar la búsqueda
            profundidad_maxima: Profundidad máxima de búsqueda
            
        Returns:
            Lista de tuplas (nodo, distancia) encontrados
        """
        cdef vector[pair[int, int]] resultado_cpp = self.c_grafo.BFS(nodo_inicio, profundidad_maxima)
        
        # Convertir resultado C++ a lista de Python
        resultado_python = []
        cdef pair[int, int] item
        for item in resultado_cpp:
            resultado_python.append((item.first, item.second))
        
        return resultado_python
    
    def obtener_grado(self, int nodo):
        """
        Obtiene el grado (número de conexiones) de un nodo.
        
        Args:
            nodo: ID del nodo
            
        Returns:
            Grado del nodo
        """
        return self.c_grafo.obtenerGrado(nodo)
    
    def get_vecinos(self, int nodo):
        """
        Obtiene los vecinos de un nodo específico.
        
        Args:
            nodo: ID del nodo
            
        Returns:
            Lista con los IDs de los nodos vecinos
        """
        cdef vector[int] vecinos_cpp = self.c_grafo.getVecinos(nodo)
        
        # Convertir a lista de Python
        return [v for v in vecinos_cpp]
    
    def get_num_nodos(self):
        """Obtiene el número total de nodos en el grafo."""
        return self.c_grafo.getNumNodos()
    
    def get_num_aristas(self):
        """Obtiene el número total de aristas en el grafo."""
        return self.c_grafo.getNumAristas()
    
    def get_nodo_mayor_grado(self):
        """
        Encuentra el nodo con el mayor grado en el grafo.
        
        Returns:
            Tupla (nodo_id, grado)
        """
        cdef pair[int, int] resultado = self.c_grafo.getNodoMayorGrado()
        return (resultado.first, resultado.second)
    
    def get_memoria_estimada(self):
        """
        Estima la memoria utilizada por la estructura del grafo.
        
        Returns:
            Memoria estimada en bytes
        """
        return self.c_grafo.getMemoriaEstimada()
    
    def get_todas_las_aristas(self):
        """
        Obtiene todas las aristas del grafo.
        
        Returns:
            Lista de tuplas (origen, destino)
        """
        cdef vector[pair[int, int]] aristas_cpp = self.c_grafo.getTodasLasAristas()
        
        # Convertir a lista de Python
        aristas_python = []
        cdef pair[int, int] arista
        for arista in aristas_cpp:
            aristas_python.append((arista.first, arista.second))
        
        return aristas_python
