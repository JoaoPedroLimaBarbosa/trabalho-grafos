# graph.py
# Estrutura do grafo (suporta pesos e grafos direcionados ou não)

class Grafo:
    def __init__(self, direcionado=False):
        self.direcionado = direcionado
        # adj: {vertice: [(vizinho, peso), ...], ...}
        self.adj = {}

    def adicionar_vertice(self, v):
        if v not in self.adj:
            self.adj[v] = []

    def adicionar_aresta(self, u, v, peso=1):
        self.adicionar_vertice(u)
        self.adicionar_vertice(v)

        # evita múltiplas arestas idênticas: atualiza peso se já existir
        def _add(orig, dest, w):
            for i, (d, p) in enumerate(self.adj[orig]):
                if d == dest:
                    self.adj[orig][i] = (dest, w)
                    return
            self.adj[orig].append((dest, w))

        _add(u, v, peso)
        if not self.direcionado:
            _add(v, u, peso)

    def remover_vertice(self, v):
        if v in self.adj:
            del self.adj[v]
        for origem in list(self.adj.keys()):
            self.adj[origem] = [(d, p) for (d, p) in self.adj[origem] if d != v]

    def remover_aresta(self, u, v):
        if u in self.adj:
            self.adj[u] = [(d, p) for (d, p) in self.adj[u] if d != v]
        if not self.direcionado and v in self.adj:
            self.adj[v] = [(d, p) for (d, p) in self.adj[v] if d != u]

    def exibir(self):
        print("\n=== Estrutura do Grafo ===")
        for origem in self.adj:
            print(f"{origem}: {self.adj[origem]}")
        print("==========================\n")

    def vertices(self):
        return list(self.adj.keys())

    def arestas(self):
        # retorna lista de (u, v, peso)
        edges = []
        seen = set()
        for u in self.adj:
            for v, p in self.adj[u]:
                if self.direcionado:
                    edges.append((u, v, p))
                else:
                    key = tuple(sorted((u, v)))
                    if key not in seen:
                        seen.add(key)
                        edges.append((u, v, p))
        return edges
