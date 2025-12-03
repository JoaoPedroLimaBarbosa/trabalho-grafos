# algorithms.py
# Algoritmos clássicos: BFS, DFS, Dijkstra, Bellman-Ford e utilitários

from collections import deque
import heapq

def bfs(grafo, inicio):
    """Retorna (ordem, prev) onde prev é dicionário para reconstruir caminhos."""
    if inicio not in grafo.adj:
        return [], {}
    visitados = set()
    fila = deque([inicio])
    ordem = []
    prev = {inicio: None}
    while fila:
        u = fila.popleft()
        if u in visitados:
            continue
        visitados.add(u)
        ordem.append(u)
        for v, _ in grafo.adj.get(u, []):
            if v not in visitados and v not in fila:
                prev[v] = u
                fila.append(v)
    return ordem, prev

def dfs(grafo, inicio):
    """Retorna (ordem, prev)."""
    if inicio not in grafo.adj:
        return [], {}
    visitados = set()
    ordem = []
    prev = {inicio: None}
    def dfs_rec(u):
        visitados.add(u)
        ordem.append(u)
        for v, _ in grafo.adj.get(u, []):
            if v not in visitados:
                prev[v] = u
                dfs_rec(v)
    dfs_rec(inicio)
    return ordem, prev

def dijkstra(grafo, inicio):
    """Retorna (dist, prev). dist: dict de distâncias mínimas (peso >=0)."""
    if inicio not in grafo.adj:
        return {}, {}
    dist = {v: float('inf') for v in grafo.adj}
    prev = {v: None for v in grafo.adj}
    dist[inicio] = 0
    pq = [(0, inicio)]
    while pq:
        d_u, u = heapq.heappop(pq)
        if d_u > dist[u]:
            continue
        for v, peso in grafo.adj.get(u, []):
            nd = d_u + peso
            if nd < dist[v]:
                dist[v] = nd
                prev[v] = u
                heapq.heappush(pq, (nd, v))
    return dist, prev

def bellman_ford(grafo, inicio):
    """
    Retorna (dist, prev, has_negative_cycle)
    Distâncias podem ser inf se não alcançáveis.
    Detecta ciclo negativo e retorna has_negative_cycle=True se existir.
    """
    if inicio not in grafo.adj:
        return {}, {}, False
    # Inicializar distâncias
    dist = {v: float('inf') for v in grafo.adj}
    prev = {v: None for v in grafo.adj}
    dist[inicio] = 0
    # Relaxar |V|-1 vezes
    vertices = list(grafo.adj.keys())
    for _ in range(len(vertices) - 1):
        changed = False
        for u in vertices:
            if dist[u] == float('inf'):
                continue
            for v, peso in grafo.adj.get(u, []):
                if dist[u] + peso < dist[v]:
                    dist[v] = dist[u] + peso
                    prev[v] = u
                    changed = True
        if not changed:
            break
    # Verificar ciclo negativo
    has_negative_cycle = False
    for u in vertices:
        if dist[u] == float('inf'):
            continue
        for v, peso in grafo.adj.get(u, []):
            if dist[u] + peso < dist[v]:
                has_negative_cycle = True
                break
        if has_negative_cycle:
            break
    return dist, prev, has_negative_cycle

def reconstruir_caminho(prev, destino):
    """Reconstrói caminho usando prev dict. Retorna lista do início até destino (ou [])."""
    if destino not in prev:
        return []
    caminho = []
    cur = destino
    while cur is not None:
        caminho.append(cur)
        cur = prev.get(cur)
    caminho.reverse()
    return caminho
