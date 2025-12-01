#ifndef GRAFO_DISPERSO_H
#define GRAFO_DISPERSO_H

#include "GrafoBase.h"
#include <map>
#include <string>
#include <vector>


/**
 * Implementación concreta de un grafo usando formato CSR (Compressed Sparse
 * Row). Esta estructura es eficiente en memoria para grafos dispersos (sparse
 * graphs).
 */
class GrafoDisperso : public GrafoBase {
private:
  // Formato CSR para almacenar la matriz de adyacencia dispersa
  std::vector<int> row_ptr;     // Punteros de inicio de fila
  std::vector<int> col_indices; // Índices de columna (vecinos)

  int numNodos;   // Número total de nodos
  int numAristas; // Número total de aristas

  std::map<int, int> nodoAIndice; // Mapeo de ID de nodo a índice interno
  std::vector<int> indiceANodo;   // Mapeo inverso: índice a ID de nodo

  /**
   * Construye la estructura CSR a partir de una lista de aristas.
   * @param aristas Vector de pares (origen, destino)
   */
  void construirCSR(const std::vector<std::pair<int, int>> &aristas);

  /**
   * Convierte un ID de nodo externo a índice interno.
   * @param nodoId ID del nodo
   * @return Índice interno del nodo
   */
  int nodoAIdx(int nodoId) const;

  /**
   * Convierte un índice interno a ID de nodo externo.
   * @param idx Índice interno
   * @return ID del nodo
   */
  int idxANodo(int idx) const;

public:
  GrafoDisperso();
  virtual ~GrafoDisperso();

  // Implementación de métodos virtuales de GrafoBase
  bool cargarDatos(const std::string &nombreArchivo) override;
  std::vector<std::pair<int, int>> BFS(int nodoInicio,
                                       int profundidadMaxima) override;
  int obtenerGrado(int nodo) override;
  std::vector<int> getVecinos(int nodo) override;
  int getNumNodos() const override;
  int getNumAristas() const override;
  std::pair<int, int> getNodoMayorGrado() override;
  size_t getMemoriaEstimada() const override;

  /**
   * Obtiene todas las aristas del grafo.
   * @return Vector de pares (origen, destino)
   */
  std::vector<std::pair<int, int>> getTodasLasAristas() const;
};

#endif // GRAFO_DISPERSO_H
