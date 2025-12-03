# gui.py
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from graph import Grafo
from algorithms import bfs, dfs, dijkstra, bellman_ford, reconstruir_caminho

class FullGrafoGUI(tk.Tk):
    """
    Interface completa alinhada ao PDF:
    - operações básicas (add/remove vértice/aresta)
    - mostrar grafo
    - BFS, DFS, Dijkstra, Bellman-Ford
    - carregar/salvar JSON, exportar imagem
    - caso de uso demonstrativo (mapa de cidades)
    """
    def __init__(self):
        super().__init__()
        self.title("Trabalho Grafos - Interface Completa (PDF)")
        self.geometry("1100x700")
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.grafo = Grafo(direcionado=False)

        self._build_left_panel()
        self._build_right_canvas()
        self._load_example_default()

    # ---------------- UI ----------------
    def _build_left_panel(self):
        left = ttk.Frame(self, padding=8)
        left.pack(side=tk.LEFT, fill=tk.Y)

        # Seção: vértices
        ttk.Label(left, text="VÉRTICES / ARESTAS", font=("Segoe UI", 11, "bold")).pack(anchor=tk.W, pady=(0,6))
        ttk.Label(left, text="Vértice:").pack(anchor=tk.W)
        self.entry_vert = ttk.Entry(left, width=28)
        self.entry_vert.pack(anchor=tk.W, pady=2)

        btn_add_v = ttk.Button(left, text="Adicionar Vértice", command=self.add_vertice)
        btn_add_v.pack(fill=tk.X, pady=2)

        btn_rem_v = ttk.Button(left, text="Remover Vértice", command=self.remove_vertice)
        btn_rem_v.pack(fill=tk.X, pady=2)

        ttk.Separator(left).pack(fill=tk.X, pady=6)

        ttk.Label(left, text="Aresta (u, v, peso):").pack(anchor=tk.W)
        self.entry_u = ttk.Entry(left, width=12); self.entry_u.pack(anchor=tk.W, pady=1)
        self.entry_v = ttk.Entry(left, width=12); self.entry_v.pack(anchor=tk.W, pady=1)
        self.entry_peso = ttk.Entry(left, width=12); self.entry_peso.insert(0, "1"); self.entry_peso.pack(anchor=tk.W, pady=1)

        btn_add_e = ttk.Button(left, text="Adicionar Aresta", command=self.add_aresta)
        btn_add_e.pack(fill=tk.X, pady=2)
        btn_rem_e = ttk.Button(left, text="Remover Aresta", command=self.remove_aresta)
        btn_rem_e.pack(fill=tk.X, pady=2)

        ttk.Separator(left).pack(fill=tk.X, pady=6)

        # Seção: opções de grafo
        self.var_direc = tk.BooleanVar(value=False)
        chk_dir = ttk.Checkbutton(left, text="Direcionado", variable=self.var_direc, command=self.toggle_direcionado)
        chk_dir.pack(anchor=tk.W, pady=2)

        btn_show = ttk.Button(left, text="Exibir/Atualizar Grafo", command=self.draw_graph)
        btn_show.pack(fill=tk.X, pady=4)

        btn_export = ttk.Button(left, text="Exportar imagem (PNG)", command=self.export_image)
        btn_export.pack(fill=tk.X, pady=2)

        ttk.Separator(left).pack(fill=tk.X, pady=6)

        # Seção: algoritmos
        ttk.Label(left, text="ALGORITMOS", font=("Segoe UI", 11, "bold")).pack(anchor=tk.W, pady=(0,6))
        ttk.Label(left, text="Vértice início:").pack(anchor=tk.W)
        self.entry_start = ttk.Entry(left, width=20)
        self.entry_start.pack(anchor=tk.W, pady=2)

        btn_bfs = ttk.Button(left, text="BFS (Busca em Largura)", command=self.run_bfs)
        btn_bfs.pack(fill=tk.X, pady=2)
        btn_dfs = ttk.Button(left, text="DFS (Busca em Profundidade)", command=self.run_dfs)
        btn_dfs.pack(fill=tk.X, pady=2)
        btn_dij = ttk.Button(left, text="Dijkstra (pesos >=0)", command=self.run_dijkstra)
        btn_dij.pack(fill=tk.X, pady=2)
        btn_bf = ttk.Button(left, text="Bellman-Ford (pesos negativos)", command=self.run_bellman_ford)
        btn_bf.pack(fill=tk.X, pady=2)

        ttk.Separator(left).pack(fill=tk.X, pady=6)

        # Seção: IO
        ttk.Label(left, text="ENTREGA / EXEMPLOS", font=("Segoe UI", 11, "bold")).pack(anchor=tk.W, pady=(0,6))
        btn_load = ttk.Button(left, text="Carregar JSON (examples/)", command=self.load_json)
        btn_load.pack(fill=tk.X, pady=2)
        btn_save = ttk.Button(left, text="Salvar grafo para JSON", command=self.save_json)
        btn_save.pack(fill=tk.X, pady=2)

        btn_case = ttk.Button(left, text="Carregar caso de uso (mapa de cidades)", command=self._load_example_default)
        btn_case.pack(fill=tk.X, pady=4)

        btn_clear = ttk.Button(left, text="Limpar grafo", command=self.clear_graph)
        btn_clear.pack(fill=tk.X, pady=6)

        ttk.Separator(left).pack(fill=tk.X, pady=6)

        # Seção: saída
        ttk.Label(left, text="Saída / Logs:", font=("Segoe UI", 10, "bold")).pack(anchor=tk.W)
        self.txt_out = tk.Text(left, width=38, height=16, wrap=tk.WORD)
        self.txt_out.pack(fill=tk.BOTH, pady=4)

    def _build_right_canvas(self):
        right = ttk.Frame(self, padding=6)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.fig, self.ax = plt.subplots(figsize=(7,6))
        plt.tight_layout()
        self.canvas = FigureCanvasTkAgg(self.fig, master=right)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # ---------------- 操作 do grafo ----------------
    def log(self, text):
        self.txt_out.insert(tk.END, str(text) + "\n")
        self.txt_out.see(tk.END)

    def add_vertice(self):
        v = self.entry_vert.get().strip()
        if not v:
            messagebox.showwarning("Aviso", "Digite um nome de vértice.")
            return
        self.grafo.adicionar_vertice(v)
        self.log(f"Vértice '{v}' adicionado.")
        self.draw_graph()

    def remove_vertice(self):
        v = self.entry_vert.get().strip()
        if not v:
            messagebox.showwarning("Aviso", "Digite um vértice para remover.")
            return
        self.grafo.remover_vertice(v)
        self.log(f"Vértice '{v}' removido (se existia).")
        self.draw_graph()

    def add_aresta(self):
        u = self.entry_u.get().strip()
        v = self.entry_v.get().strip()
        peso_text = self.entry_peso.get().strip()
        if not u or not v:
            messagebox.showwarning("Aviso", "Digite u e v.")
            return
        try:
            peso = float(peso_text)
        except:
            messagebox.showwarning("Aviso", "Peso inválido.")
            return
        self.grafo.adicionar_aresta(u, v, peso)
        self.log(f"Aresta '{u}' -> '{v}' (peso={peso}) adicionada.")
        self.draw_graph()

    def remove_aresta(self):
        u = self.entry_u.get().strip()
        v = self.entry_v.get().strip()
        if not u or not v:
            messagebox.showwarning("Aviso", "Digite u e v da aresta a remover.")
            return
        self.grafo.remover_aresta(u, v)
        self.log(f"Aresta '{u}' -> '{v}' removida (se existia).")
        self.draw_graph()

    def toggle_direcionado(self):
        self.grafo.direcionado = self.var_direc.get()
        self.log(f"Modo direcionado = {self.grafo.direcionado}")
        self.draw_graph()

    def clear_graph(self):
        self.grafo = Grafo(direcionado=self.var_direc.get())
        self.log("Grafo limpo.")
        self.draw_graph()

    # ---------------- IO ----------------
    def load_json(self):
        path = filedialog.askopenfilename(initialdir="../examples", filetypes=[("JSON files","*.json"), ("All files","*.*")])
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            direc = data.get("direcionado", False)
            g = Grafo(direcionado=direc)
            for v in data.get("vertices", []):
                g.adicionar_vertice(v)
            for e in data.get("arestas", []):
                u, v, p = e
                g.adicionar_aresta(u, v, p)
            self.grafo = g
            self.var_direc.set(direc)
            self.log(f"Exemplo carregado: {path}")
            self.draw_graph()
        except Exception as ex:
            messagebox.showerror("Erro", f"Falha ao carregar JSON:\n{ex}")

    def save_json(self):
        path = filedialog.asksaveasfilename(defaultextension=".json", initialdir="../examples", filetypes=[("JSON","*.json")])
        if not path:
            return
        data = {
            "direcionado": self.grafo.direcionado,
            "vertices": self.grafo.vertices(),
            "arestas": self.grafo.arestas()
        }
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            self.log(f"Grafo salvo em: {path}")
        except Exception as ex:
            messagebox.showerror("Erro", f"Falha ao salvar JSON:\n{ex}")

    def export_image(self):
        path = filedialog.asksaveasfilename(defaultextension=".png", initialdir=".", filetypes=[("PNG","*.png")])
        if not path:
            return
        try:
            self.fig.savefig(path, dpi=150, bbox_inches="tight")
            self.log(f"Imagem exportada: {path}")
        except Exception as ex:
            messagebox.showerror("Erro", f"Falha ao exportar imagem:\n{ex}")

    # ---------------- Algoritmos ----------------
    def run_bfs(self):
        inicio = self.entry_start.get().strip()
        if not inicio:
            messagebox.showwarning("Aviso", "Insira vértice inicial.")
            return
        ordem, prev = bfs(self.grafo, inicio)
        if not ordem:
            self.log("Vertice inicial não existe ou grafo vazio.")
            return
        self.log("BFS ordem: " + " -> ".join(ordem))
        for v in ordem:
            caminho = reconstruir_caminho(prev, v)
            self.log(f"Caminho ({inicio} -> {v}): {caminho}")

    def run_dfs(self):
        inicio = self.entry_start.get().strip()
        if not inicio:
            messagebox.showwarning("Aviso", "Insira vértice inicial.")
            return
        ordem, prev = dfs(self.grafo, inicio)
        if not ordem:
            self.log("Vertice inicial não existe ou grafo vazio.")
            return
        self.log("DFS ordem: " + " -> ".join(ordem))
        for v in ordem:
            caminho = reconstruir_caminho(prev, v)
            self.log(f"Caminho ({inicio} -> {v}): {caminho}")

    def run_dijkstra(self):
        inicio = self.entry_start.get().strip()
        if not inicio:
            messagebox.showwarning("Aviso", "Insira vértice inicial.")
            return
        dist, prev = dijkstra(self.grafo, inicio)
        if not dist:
            self.log("Vertice inicial não existe ou grafo vazio.")
            return
        self.log("Dijkstra - distâncias mínimas:")
        for v in sorted(dist.keys()):
            d = dist[v]
            caminho = reconstruir_caminho(prev, v)
            self.log(f"{inicio} -> {v} | dist = {d} | caminho = {caminho}")

    def run_bellman_ford(self):
        inicio = self.entry_start.get().strip()
        if not inicio:
            messagebox.showwarning("Aviso", "Insira vértice inicial.")
            return
        dist, prev, neg = bellman_ford(self.grafo, inicio)
        if not dist:
            self.log("Vertice inicial não existe ou grafo vazio.")
            return
        if neg:
            self.log("Bellman-Ford: ciclo negativo detectado! (Resultados podem ser inválidos)")
        self.log("Bellman-Ford - distâncias:")
        for v in sorted(dist.keys()):
            d = dist[v]
            caminho = reconstruir_caminho(prev, v)
            self.log(f"{inicio} -> {v} | dist = {d} | caminho = {caminho}")

    # ---------------- Desenho ----------------
    def draw_graph(self):
        self.ax.clear()
        G = nx.DiGraph() if self.grafo.direcionado else nx.Graph()

        for v in self.grafo.vertices():
            G.add_node(v)
        for u, v, p in self.grafo.arestas():
            G.add_edge(u, v, weight=p)

        if len(G) == 0:
            self.canvas.draw()
            return

        pos = nx.spring_layout(G, seed=42)
        nx.draw_networkx_nodes(G, pos, ax=self.ax, node_size=700)
        nx.draw_networkx_labels(G, pos, ax=self.ax)
        nx.draw_networkx_edges(G, pos, ax=self.ax, connectionstyle='arc3,rad=0.1' if self.grafo.direcionado else 'arc3,rad=0.0', arrows=self.grafo.direcionado)
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=self.ax)
        self.ax.set_axis_off()
        self.canvas.draw()

    # ---------------- Casos de uso / Exemplo ----------------
    def _load_example_default(self):
        # mapa de cidades (caso de uso sugerido no PDF)
        ex = [
            ("São Paulo", "Campinas", 90),
            ("Campinas", "Americana", 45),
            ("Campinas", "Jundiaí", 40),
            ("Jundiaí", "São Paulo", 60),
            ("Americana", "Limeira", 25),
            ("Limeira", "Rio Claro", 30)
        ]
        self.grafo = Grafo(direcionado=False)
        for u, v, p in ex:
            self.grafo.adicionar_aresta(u, v, p)
        self.log("Caso de uso 'Mapa de Cidades' carregado.")
        self.draw_graph()

    def on_close(self):
        if messagebox.askokcancel("Sair", "Deseja fechar a aplicação?"):
            self.destroy()

# Para compatibilidade com main.py existente que importa GrafoGUI
class GrafoGUI(FullGrafoGUI):
    pass
