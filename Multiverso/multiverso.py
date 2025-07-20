import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import networkx as nx
import numpy as np
from matplotlib.patches import FancyArrowPatch

# --------- ESTRUCTURA DE DATOS ---------
class Nodo:
    def __init__(self, valor, centro=None):
        self.valor = valor
        self.siguiente = None
        self.anterior = None
        self.centro = centro

class Anillo:
    def __init__(self, nombre):
        self.nombre = nombre
        self.centro = None
        self.primero = None
        self.tamano = 0
        self.anillo_conectado = None

    def insertar(self, valor):
        nuevo = Nodo(valor)
        if self.tamano == 0:
            self.centro = nuevo
            nuevo.siguiente = nuevo
            nuevo.anterior = nuevo
            nuevo.centro = nuevo
            self.primero = nuevo
        else:
            ultimo = self.primero.anterior
            nuevo.anterior = ultimo
            nuevo.siguiente = self.primero
            nuevo.centro = self.centro
            ultimo.siguiente = nuevo
            self.primero.anterior = nuevo
        self.tamano += 1

    def eliminar_ultimo(self):
        if self.tamano <= 1:
            return
        ultimo = self.primero.anterior
        penultimo = ultimo.anterior
        penultimo.siguiente = self.primero
        self.primero.anterior = penultimo
        self.tamano -= 1

    def nodos(self):
        nodos = []
        actual = self.primero
        for _ in range(self.tamano):
            nodos.append(actual)
            actual = actual.siguiente
        return nodos

# --------- GRAFICADOR ---------
def dibujar_flecha_curva(ax, pos_src, pos_dst, color='black', rad=0.3):
    arrow = FancyArrowPatch(
        posA=pos_src,
        posB=pos_dst,
        connectionstyle=f"arc3,rad={rad}",
        arrowstyle='-|>',
        color=color,
        linewidth=2,
        mutation_scale=20
    )
    ax.add_patch(arrow)

def graficar(anillos):
    G = nx.DiGraph()
    pos = {}
    num_anillos = len(anillos)
    radio_grande = 8 + num_anillos * 1.5  # Aumenta dinámicamente para evitar solapamiento
    radio_anillo = 3
    offset_global = np.pi / 6

    for i, anillo in enumerate(anillos):
        nodos = anillo.nodos()
        centro = anillo.centro
        nodos_no_centro = [n for n in nodos if n != centro]
        G.add_node(centro.valor)

        angle_centro = 2 * np.pi * i / max(1, num_anillos) + offset_global
        cx = radio_grande * np.cos(angle_centro)
        cy = radio_grande * np.sin(angle_centro)
        pos[centro.valor] = (cx, cy)

        for j, nodo in enumerate(nodos_no_centro):
            G.add_node(nodo.valor)
            angle = 2 * np.pi * j / len(nodos_no_centro)
            x = cx + radio_anillo * np.cos(angle)
            y = cy + radio_anillo * np.sin(angle)
            pos[nodo.valor] = (x, y)
            G.add_edge(nodo.valor, centro.valor)

        for j in range(len(nodos_no_centro)):
            u = nodos_no_centro[j].valor
            v = nodos_no_centro[(j+1) % len(nodos_no_centro)].valor
            G.add_edge(u, v)

        if anillo.anillo_conectado:
            G.add_edge(anillo.centro.valor, anillo.anillo_conectado.centro.valor)

    # Cerrar la conexión entre el último y el primero
    if len(anillos) > 1:
        G.add_edge(anillos[-1].centro.valor, anillos[0].centro.valor)

    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_aspect('equal')
    ax.axis('off')

    for u, v in G.edges():
        dibujar_flecha_curva(ax, pos[u], pos[v], color='gray', rad=0.3)

    for n in G.nodes():
        x, y = pos[n]
        ax.plot(x, y, 'o', color='orange' if n.startswith("C") else 'skyblue', markersize=20)
        ax.text(x, y, n, fontsize=10, ha='center', va='center')

    all_x = [x for x, y in pos.values()]
    all_y = [y for x, y in pos.values()]
    margin = 5
    ax.set_xlim(min(all_x) - margin, max(all_x) + margin)
    ax.set_ylim(min(all_y) - margin, max(all_y) + margin)

    return fig

# --------- INTERFAZ TKINTER ---------
class App:
    def __init__(self, root):
        self.anillos = []
        self.contador = 1

        anillo_inicial = Anillo("Anillo 1")
        anillo_inicial.insertar(f"C1")
        self.anillos.append(anillo_inicial)

        frame = tk.Frame(root)
        frame.pack()

        btn_add = tk.Button(frame, text="Agregar Nodo", command=self.agregar_nodo)
        btn_add.grid(row=0, column=0, padx=5, pady=5)

        btn_del = tk.Button(frame, text="Eliminar Nodo", command=self.eliminar_nodo)
        btn_del.grid(row=0, column=1, padx=5, pady=5)

        self.fig = None
        self.canvas = None
        self.toolbar = None

        self.graficar_canvas(root)

    def graficar_canvas(self, root):
        if self.canvas:
            self.canvas.get_tk_widget().pack_forget()
            self.toolbar.pack_forget()

        self.fig = graficar(self.anillos)
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        self.toolbar = NavigationToolbar2Tk(self.canvas, root)
        self.toolbar.update()
        self.toolbar.pack()
        self.toolbar.pan()

    def agregar_nodo(self):
        anillo_actual = self.anillos[-1]
        if anillo_actual.tamano >= 6:
            nuevo_anillo = Anillo(f"Anillo {len(self.anillos) + 1}")
            nuevo_centro = f"C{len(self.anillos) + 1}"
            nuevo_anillo.insertar(nuevo_centro)
            anillo_actual.anillo_conectado = nuevo_anillo
            self.anillos.append(nuevo_anillo)
        else:
            anillo_actual.insertar(f"N{self.contador}")
            self.contador += 1
        self.graficar_canvas(root)

    def eliminar_nodo(self):
        if not self.anillos:
            return

        anillo_actual = self.anillos[-1]
        if anillo_actual.tamano > 1:
            anillo_actual.eliminar_ultimo()
        elif len(self.anillos) > 1:
            self.anillos.pop()
            self.anillos[-1].anillo_conectado = None

        self.graficar_canvas(root)

# --------- EJECUCIÓN ---------
if __name__ == '__main__':
    root = tk.Tk()
    root.title("Editor de Anillos Dinámicos")
    app = App(root)
    root.geometry("1000x900")
    root.mainloop()