#ifndef GRAFO_BASE_H
#define GRAFO_BASE_H

#include <vector>
#include <string>

/**
 * Clase abstracta base que define la interfaz para grafos.
 * Utiliza polimorfismo para permitir diferentes implementaciones.
 */
class GrafoBase {
public:
    virtual ~GrafoBase() {}
    
    /**
     * Carga datos desde un archivo de lista de aristas.
     * @param nombreArchivo Ruta al archivo de datos
     * @return true si la carga fue exitosa, false en caso contrario
     */
    virtual bool cargarDatos(const std::string& nombreArchivo) = 0;
    
    /**
     * Realiza una búsqueda en anchura (BFS) desde un nodo inicial.
     * @param nodoInicio Nodo desde donde comenzar la búsqueda
     * @param profundidadMaxima Profundidad máxima de búsqueda
     * @return Vector de pares (nodo, distancia) encontrados
     */
    virtual std::vector<std::pair<int, int>> BFS(int nodoInicio, int profundidadMaxima) = 0;
    
    /**
     * Obtiene el grado (número de conexiones) de un nodo específico.
     * @param nodo ID del nodo
     * @return Grado del nodo
     */
    virtual int obtenerGrado(int nodo) = 0;
    
    /**
     * Obtiene los vecinos de un nodo específico.
     * @param nodo ID del nodo
     * @return Vector con los IDs de los nodos vecinos
     */
    virtual std::vector<int> getVecinos(int nodo) = 0;
    
    /**
     * Obtiene el número total de nodos en el grafo.
     * @return Número de nodos
     */
    virtual int getNumNodos() const = 0;
    
    /**
     * Obtiene el número total de aristas en el grafo.
     * @return Número de aristas
     */
    virtual int getNumAristas() const = 0;
    
    /**
     * Encuentra el nodo con el mayor grado en el grafo.
     * @return Par (nodo_id, grado)
     */
    virtual std::pair<int, int> getNodoMayorGrado() = 0;
    
    /**
     * Estima la memoria utilizada por la estructura del grafo.
     * @return Memoria estimada en bytes
     */
    virtual size_t getMemoriaEstimada() const = 0;
};

#endif // GRAFO_BASE_H
