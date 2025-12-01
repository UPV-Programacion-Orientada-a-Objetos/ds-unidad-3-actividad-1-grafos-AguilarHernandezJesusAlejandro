#include "GrafoDisperso.h"
#include <algorithm>
#include <chrono>
#include <fstream>
#include <iostream>
#include <queue>
#include <set>
#include <sstream>


GrafoDisperso::GrafoDisperso() : numNodos(0), numAristas(0) {
  std::cout << "[C++ Core] Inicializando GrafoDisperso..." << std::endl;
}

GrafoDisperso::~GrafoDisperso() {
  // Los vectores se limpian automáticamente
}

bool GrafoDisperso::cargarDatos(const std::string &nombreArchivo) {
  std::cout << "[C++ Core] Cargando dataset '" << nombreArchivo << "'..."
            << std::endl;

  auto inicio = std::chrono::high_resolution_clock::now();

  std::ifstream archivo(nombreArchivo);
  if (!archivo.is_open()) {
    std::cerr << "[C++ Core] Error: No se pudo abrir el archivo "
              << nombreArchivo << std::endl;
    return false;
  }

  std::vector<std::pair<int, int>> aristas;
  std::set<int> nodosUnicos;
  std::string linea;

  // Leer archivo línea por línea
  while (std::getline(archivo, linea)) {
    // Ignorar líneas vacías o comentarios
    if (linea.empty() || linea[0] == '#') {
      continue;
    }

    std::istringstream iss(linea);
    int origen, destino;

    if (iss >> origen >> destino) {
      aristas.push_back({origen, destino});
      nodosUnicos.insert(origen);
      nodosUnicos.insert(destino);
    }
  }

  archivo.close();

  numAristas = aristas.size();
  numNodos = nodosUnicos.size();

  // Crear mapeo de IDs de nodos a índices consecutivos
  int idx = 0;
  for (int nodo : nodosUnicos) {
    nodoAIndice[nodo] = idx;
    indiceANodo.push_back(nodo);
    idx++;
  }

  // Construir estructura CSR
  construirCSR(aristas);

  auto fin = std::chrono::high_resolution_clock::now();
  auto duracion =
      std::chrono::duration_cast<std::chrono::milliseconds>(fin - inicio);

  std::cout << "[C++ Core] Carga completa. Nodos: " << numNodos
            << " | Aristas: " << numAristas << std::endl;
  std::cout << "[C++ Core] Estructura CSR construida. Memoria estimada: "
            << (getMemoriaEstimada() / (1024 * 1024)) << " MB." << std::endl;
  std::cout << "[C++ Core] Tiempo de carga: " << duracion.count() << " ms."
            << std::endl;

  return true;
}

void GrafoDisperso::construirCSR(
    const std::vector<std::pair<int, int>> &aristas) {
  // Crear lista de adyacencia temporal
  std::vector<std::vector<int>> listaAdyacencia(numNodos);

  for (const auto &arista : aristas) {
    int origenIdx = nodoAIdx(arista.first);
    int destinoIdx = nodoAIdx(arista.second);
    listaAdyacencia[origenIdx].push_back(destinoIdx);
  }

  // Ordenar vecinos para cada nodo (opcional, pero útil)
  for (auto &vecinos : listaAdyacencia) {
    std::sort(vecinos.begin(), vecinos.end());
    // Eliminar duplicados
    vecinos.erase(std::unique(vecinos.begin(), vecinos.end()), vecinos.end());
  }

  // Construir formato CSR
  row_ptr.resize(numNodos + 1);
  row_ptr[0] = 0;

  for (int i = 0; i < numNodos; i++) {
    row_ptr[i + 1] = row_ptr[i] + listaAdyacencia[i].size();
    for (int vecino : listaAdyacencia[i]) {
      col_indices.push_back(vecino);
    }
  }
}

int GrafoDisperso::nodoAIdx(int nodoId) const {
  auto it = nodoAIndice.find(nodoId);
  if (it != nodoAIndice.end()) {
    return it->second;
  }
  return -1;
}

int GrafoDisperso::idxANodo(int idx) const {
  if (idx >= 0 && idx < static_cast<int>(indiceANodo.size())) {
    return indiceANodo[idx];
  }
  return -1;
}

std::vector<std::pair<int, int>> GrafoDisperso::BFS(int nodoInicio,
                                                    int profundidadMaxima) {
  std::cout << "[Cython] Solicitud recibida: BFS desde Nodo " << nodoInicio
            << ", Profundidad " << profundidadMaxima << "." << std::endl;
  std::cout << "[C++ Core] Ejecutando BFS nativo..." << std::endl;

  auto inicio = std::chrono::high_resolution_clock::now();

  std::vector<std::pair<int, int>> resultado;

  int inicioIdx = nodoAIdx(nodoInicio);
  if (inicioIdx == -1) {
    std::cerr << "[C++ Core] Error: Nodo " << nodoInicio
              << " no existe en el grafo." << std::endl;
    return resultado;
  }

  std::vector<int> distancia(numNodos, -1);
  std::queue<int> cola;

  cola.push(inicioIdx);
  distancia[inicioIdx] = 0;
  resultado.push_back({nodoInicio, 0});

  while (!cola.empty()) {
    int actualIdx = cola.front();
    cola.pop();

    int distActual = distancia[actualIdx];

    // Si alcanzamos la profundidad máxima, no exploramos más desde este nodo
    if (distActual >= profundidadMaxima) {
      continue;
    }

    // Explorar vecinos usando la estructura CSR
    int inicio = row_ptr[actualIdx];
    int fin = row_ptr[actualIdx + 1];

    for (int i = inicio; i < fin; i++) {
      int vecinoIdx = col_indices[i];

      if (distancia[vecinoIdx] == -1) {
        distancia[vecinoIdx] = distActual + 1;
        cola.push(vecinoIdx);
        resultado.push_back({idxANodo(vecinoIdx), distActual + 1});
      }
    }
  }

  auto fin = std::chrono::high_resolution_clock::now();
  auto duracion =
      std::chrono::duration_cast<std::chrono::microseconds>(fin - inicio);

  std::cout << "[C++ Core] Nodos encontrados: " << resultado.size()
            << ". Tiempo ejecución: " << (duracion.count() / 1000.0) << "ms."
            << std::endl;
  std::cout << "[Cython] Retornando lista de adyacencia local a Python."
            << std::endl;

  return resultado;
}

int GrafoDisperso::obtenerGrado(int nodo) {
  int idx = nodoAIdx(nodo);
  if (idx == -1) {
    return 0;
  }

  return row_ptr[idx + 1] - row_ptr[idx];
}

std::vector<int> GrafoDisperso::getVecinos(int nodo) {
  std::vector<int> vecinos;

  int idx = nodoAIdx(nodo);
  if (idx == -1) {
    return vecinos;
  }

  int inicio = row_ptr[idx];
  int fin = row_ptr[idx + 1];

  for (int i = inicio; i < fin; i++) {
    vecinos.push_back(idxANodo(col_indices[i]));
  }

  return vecinos;
}

int GrafoDisperso::getNumNodos() const { return numNodos; }

int GrafoDisperso::getNumAristas() const { return numAristas; }

std::pair<int, int> GrafoDisperso::getNodoMayorGrado() {
  int maxGrado = 0;
  int nodoMaxGrado = -1;

  for (int i = 0; i < numNodos; i++) {
    int grado = row_ptr[i + 1] - row_ptr[i];
    if (grado > maxGrado) {
      maxGrado = grado;
      nodoMaxGrado = idxANodo(i);
    }
  }

  return {nodoMaxGrado, maxGrado};
}

size_t GrafoDisperso::getMemoriaEstimada() const {
  size_t memoria = 0;

  // Vectores CSR
  memoria += row_ptr.capacity() * sizeof(int);
  memoria += col_indices.capacity() * sizeof(int);

  // Mapeos
  memoria +=
      nodoAIndice.size() * (sizeof(int) + sizeof(int)); // aproximado para map
  memoria += indiceANodo.capacity() * sizeof(int);

  // Otros miembros
  memoria += sizeof(numNodos) + sizeof(numAristas);

  return memoria;
}

std::vector<std::pair<int, int>> GrafoDisperso::getTodasLasAristas() const {
  std::vector<std::pair<int, int>> aristas;

  for (int i = 0; i < numNodos; i++) {
    int nodoOrigen = idxANodo(i);
    int inicio = row_ptr[i];
    int fin = row_ptr[i + 1];

    for (int j = inicio; j < fin; j++) {
      int nodoDestino = idxANodo(col_indices[j]);
      aristas.push_back({nodoOrigen, nodoDestino});
    }
  }

  return aristas;
}
