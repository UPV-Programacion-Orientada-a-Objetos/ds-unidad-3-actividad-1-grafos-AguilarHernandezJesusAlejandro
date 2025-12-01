# distutils: language = c++
# cython: language_level=3

from libcpp.vector cimport vector
from libcpp.pair cimport pair
from libcpp.string cimport string

# Declaración de la clase C++ GrafoDisperso
cdef extern from "../src/GrafoDisperso.h":
    cdef cppclass GrafoDisperso:
        GrafoDisperso() except +
        bint cargarDatos(const string& nombreArchivo)
        vector[pair[int, int]] BFS(int nodoInicio, int profundidadMaxima)
        int obtenerGrado(int nodo)
        vector[int] getVecinos(int nodo)
        int getNumNodos()
        int getNumAristas()
        pair[int, int] getNodoMayorGrado()
        size_t getMemoriaEstimada()
        vector[pair[int, int]] getTodasLasAristas()
