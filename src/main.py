# main.py
from gui import GrafoGUI

def main():
    app = GrafoGUI()
    # opcional: pre-carregar um grafo de exemplo (padrão)
    # Exemplo já construído como demonstração:
    ex = [
        ("São Paulo", "Campinas", 90),
        ("Campinas", "Americana", 45),
        ("Campinas", "Jundiaí", 40),
        ("Jundiaí", "São Paulo", 60),
        ("Americana", "Limeira", 25),
        ("Limeira", "Rio Claro", 30)
    ]
    for u, v, p in ex:
        app.grafo.adicionar_aresta(u, v, p)
    app.draw_graph()
    app.mainloop()

if __name__ == "__main__":
    main()
