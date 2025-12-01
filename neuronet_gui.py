#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NeuroNet: Interfaz Gráfica de Usuario
Sistema de análisis y visualización de grafos masivos
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import sys
import os

# Intentar importar el módulo compilado de Cython
try:
    import grafo_wrapper
except ImportError:
    messagebox.showerror(
        "Error de Importación",
        "No se pudo importar el módulo 'grafo_wrapper'.\n\n"
        "Por favor, compila el módulo primero ejecutando:\n"
        "python setup.py build_ext --inplace"
    )
    sys.exit(1)

# Importar librerías de visualización
try:
    import networkx as nx
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    from matplotlib.figure import Figure
except ImportError:
    messagebox.showerror(
        "Error de Importación",
        "Faltan dependencias. Instala con:\n"
        "pip install networkx matplotlib"
    )
    sys.exit(1)


class NeuroNetGUI:
    """Interfaz gráfica principal para NeuroNet"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("NeuroNet - Análisis de Grafos Masivos")
        self.root.geometry("1200x800")
        
        # Instancia del grafo C++
        self.grafo = None
        self.archivo_cargado = None
        
        # Configurar estilo
        self.configurar_estilo()
        
        # Crear interfaz
        self.crear_widgets()
        
    def configurar_estilo(self):
        """Configura el estilo visual de la aplicación"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Colores personalizados
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'), foreground='#2c3e50')
        style.configure('Subtitle.TLabel', font=('Arial', 11, 'bold'), foreground='#34495e')
        style.configure('Info.TLabel', font=('Arial', 10), foreground='#7f8c8d')
        style.configure('Action.TButton', font=('Arial', 10, 'bold'))
        
    def crear_widgets(self):
        """Crea todos los widgets de la interfaz"""
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # ===== SECCIÓN 1: TÍTULO =====
        title_label = ttk.Label(
            main_frame,
            text="🧠 NeuroNet - Análisis de Redes Masivas",
            style='Title.TLabel'
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        # ===== SECCIÓN 2: CONTROLES =====
        control_frame = ttk.LabelFrame(main_frame, text="Controles", padding="10")
        control_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N), padx=(0, 5))
        
        # Botón cargar archivo
        ttk.Button(
            control_frame,
            text="📁 Cargar Dataset",
            command=self.cargar_archivo,
            style='Action.TButton'
        ).grid(row=0, column=0, columnspan=2, pady=5, sticky=(tk.W, tk.E))
        
        # Label archivo cargado
        self.label_archivo = ttk.Label(control_frame, text="Ningún archivo cargado", style='Info.TLabel')
        self.label_archivo.grid(row=1, column=0, columnspan=2, pady=5)
        
        # Separador
        ttk.Separator(control_frame, orient='horizontal').grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        # Controles BFS
        ttk.Label(control_frame, text="Nodo Inicio:", style='Subtitle.TLabel').grid(row=3, column=0, sticky=tk.W, pady=2)
        self.entry_nodo_inicio = ttk.Entry(control_frame, width=15)
        self.entry_nodo_inicio.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=2)
        self.entry_nodo_inicio.insert(0, "0")
        
        ttk.Label(control_frame, text="Profundidad:", style='Subtitle.TLabel').grid(row=4, column=0, sticky=tk.W, pady=2)
        self.entry_profundidad = ttk.Entry(control_frame, width=15)
        self.entry_profundidad.grid(row=4, column=1, sticky=(tk.W, tk.E), pady=2)
        self.entry_profundidad.insert(0, "2")
        
        ttk.Button(
            control_frame,
            text="🔍 Ejecutar BFS",
            command=self.ejecutar_bfs,
            style='Action.TButton'
        ).grid(row=5, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))
        
        # ===== SECCIÓN 3: MÉTRICAS =====
        metrics_frame = ttk.LabelFrame(main_frame, text="Métricas del Grafo", padding="10")
        metrics_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N), padx=(5, 0))
        
        self.label_nodos = ttk.Label(metrics_frame, text="Nodos: -", style='Info.TLabel')
        self.label_nodos.grid(row=0, column=0, sticky=tk.W, pady=2)
        
        self.label_aristas = ttk.Label(metrics_frame, text="Aristas: -", style='Info.TLabel')
        self.label_aristas.grid(row=1, column=0, sticky=tk.W, pady=2)
        
        self.label_memoria = ttk.Label(metrics_frame, text="Memoria: -", style='Info.TLabel')
        self.label_memoria.grid(row=2, column=0, sticky=tk.W, pady=2)
        
        self.label_max_grado = ttk.Label(metrics_frame, text="Nodo Mayor Grado: -", style='Info.TLabel')
        self.label_max_grado.grid(row=3, column=0, sticky=tk.W, pady=2)
        
        # ===== SECCIÓN 4: VISUALIZACIÓN =====
        viz_frame = ttk.LabelFrame(main_frame, text="Visualización del Grafo", padding="10")
        viz_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        viz_frame.columnconfigure(0, weight=1)
        viz_frame.rowconfigure(0, weight=1)
        
        # Canvas de matplotlib
        self.fig = Figure(figsize=(10, 6), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title("Esperando datos...")
        self.ax.axis('off')
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=viz_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
    def cargar_archivo(self):
        """Carga un archivo de dataset"""
        filename = filedialog.askopenfilename(
            title="Seleccionar archivo de dataset",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        
        if not filename:
            return
        
        try:
            # Crear nueva instancia del grafo
            self.grafo = grafo_wrapper.PyGrafoDisperso()
            
            # Cargar datos
            exito = self.grafo.cargar_datos(filename)
            
            if exito:
                self.archivo_cargado = os.path.basename(filename)
                self.label_archivo.config(text=f"✓ {self.archivo_cargado}")
                
                # Actualizar métricas
                self.actualizar_metricas()
                
                # Limpiar visualización
                self.ax.clear()
                self.ax.set_title("Datos cargados. Ejecuta BFS para visualizar.")
                self.ax.axis('off')
                self.canvas.draw()
                
                messagebox.showinfo("Éxito", f"Dataset cargado correctamente.\n\n"
                                             f"Nodos: {self.grafo.get_num_nodos():,}\n"
                                             f"Aristas: {self.grafo.get_num_aristas():,}")
            else:
                messagebox.showerror("Error", "No se pudo cargar el archivo.")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar el archivo:\n{str(e)}")
    
    def actualizar_metricas(self):
        """Actualiza las métricas mostradas"""
        if self.grafo is None:
            return
        
        try:
            num_nodos = self.grafo.get_num_nodos()
            num_aristas = self.grafo.get_num_aristas()
            memoria = self.grafo.get_memoria_estimada()
            nodo_max, grado_max = self.grafo.get_nodo_mayor_grado()
            
            self.label_nodos.config(text=f"Nodos: {num_nodos:,}")
            self.label_aristas.config(text=f"Aristas: {num_aristas:,}")
            self.label_memoria.config(text=f"Memoria: {memoria / (1024*1024):.2f} MB")
            self.label_max_grado.config(text=f"Nodo Mayor Grado: {nodo_max} (grado: {grado_max})")
            
        except Exception as e:
            print(f"Error actualizando métricas: {e}")
    
    def ejecutar_bfs(self):
        """Ejecuta BFS y visualiza el resultado"""
        if self.grafo is None:
            messagebox.showwarning("Advertencia", "Primero debes cargar un dataset.")
            return
        
        try:
            nodo_inicio = int(self.entry_nodo_inicio.get())
            profundidad = int(self.entry_profundidad.get())
            
            if profundidad < 1:
                messagebox.showwarning("Advertencia", "La profundidad debe ser al menos 1.")
                return
            
            # Ejecutar BFS
            resultado = self.grafo.bfs(nodo_inicio, profundidad)
            
            if not resultado:
                messagebox.showwarning("Advertencia", f"El nodo {nodo_inicio} no existe en el grafo.")
                return
            
            # Visualizar resultado
            self.visualizar_bfs(nodo_inicio, resultado)
            
        except ValueError:
            messagebox.showerror("Error", "Nodo inicio y profundidad deben ser números enteros.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al ejecutar BFS:\n{str(e)}")
    
    def visualizar_bfs(self, nodo_inicio, resultado):
        """Visualiza el resultado del BFS"""
        # Crear grafo de NetworkX solo para visualización
        G = nx.DiGraph()
        
        # Agregar nodos con sus distancias
        nodos_por_nivel = {}
        for nodo, distancia in resultado:
            G.add_node(nodo, nivel=distancia)
            if distancia not in nodos_por_nivel:
                nodos_por_nivel[distancia] = []
            nodos_por_nivel[distancia].append(nodo)
        
        # Agregar aristas desde el grafo original
        for nodo, distancia in resultado:
            if distancia > 0:  # No procesar el nodo inicial
                vecinos = self.grafo.get_vecinos(nodo)
                for vecino in vecinos:
                    if G.has_node(vecino):
                        G.add_edge(vecino, nodo)
        
        # Limpiar y configurar el gráfico
        self.ax.clear()
        
        # Crear layout jerárquico por niveles
        pos = {}
        max_nivel = max(nodos_por_nivel.keys())
        
        for nivel, nodos in nodos_por_nivel.items():
            y = max_nivel - nivel  # Invertir para que el inicio esté arriba
            num_nodos = len(nodos)
            for i, nodo in enumerate(nodos):
                x = (i - num_nodos / 2) * 1.5
                pos[nodo] = (x, y)
        
        # Colores por nivel
        colores = []
        for nodo in G.nodes():
            nivel = G.nodes[nodo]['nivel']
            if nivel == 0:
                colores.append('#e74c3c')  # Rojo para nodo inicial
            elif nivel == 1:
                colores.append('#3498db')  # Azul para nivel 1
            else:
                colores.append('#2ecc71')  # Verde para otros niveles
        
        # Dibujar el grafo
        nx.draw_networkx_nodes(G, pos, node_color=colores, node_size=500, ax=self.ax, alpha=0.9)
        nx.draw_networkx_edges(G, pos, edge_color='#95a5a6', arrows=True, 
                               arrowsize=15, ax=self.ax, alpha=0.6, width=1.5)
        nx.draw_networkx_labels(G, pos, font_size=8, font_weight='bold', ax=self.ax)
        
        self.ax.set_title(f"BFS desde Nodo {nodo_inicio} (Profundidad {max_nivel})\n"
                         f"Nodos encontrados: {len(resultado)}", 
                         fontsize=12, fontweight='bold')
        self.ax.axis('off')
        self.fig.tight_layout()
        self.canvas.draw()


def main():
    """Función principal"""
    root = tk.Tk()
    app = NeuroNetGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
