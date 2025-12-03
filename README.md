Sistema de Grafos – Estrutura de Dados 
Este repositório contém a implementação completa de um sistema de grafos aplicado ao caso de uso Mapa de Cidades, incluindo interface gráfica, algoritmos clássicos de busca e cálculo de caminhos mínimos.
 
  1. Descrição do Projeto
Este trabalho implementa um sistema de grafos que representa cidades e distâncias entre elas.
Foi desenvolvido para atender aos requisitos da disciplina Estrutura de Dados, incluindo:
Criação e manipulação de vértices (cidades)
Criação e manipulação de arestas com peso (estradas/distâncias)
Execução dos algoritmos:
BFS (Busca em Largura)
DFS (Busca em Profundidade)
Dijkstra (Caminho Mínimo)
Bellman-Ford (Caminho Mínimo com pesos gerais)
Visualização gráfica do grafo
Carregamento e salvamento via arquivo JSON
Interface gráfica completa para demonstração interativa
O foco do projeto é demonstrar domínio de implementação de grafos, algoritmos de busca e caminhos mínimos, além de boas práticas de organização de projeto.
 
  2. Estrutura do Repositório
/src/
│── main.py           → ponto de entrada da aplicação (executa a interface)
│── graph.py          → implementação da classe Grafo
│── algorithms.py     → algoritmos BFS, DFS, Dijkstra e Bellman-Ford
│── gui.py            → interface gráfica (Tkinter + NetworkX)

/examples/
│── mapa_cidades.json → arquivo com grafo exemplo usado nos testes

README.md             → documentação do projeto

Python 3.12
Tkinter (interface gráfica)
NetworkX (estrutura e visualização do grafo)
Matplotlib (renderização do grafo)
 
  4. Como Executar o Projeto
1) Instalar dependências
pip install networkx matplotlib
Tkinter já vem instalado no macOS.
2) Executar a aplicação
python3 src/main.py
A interface gráfica será aberta automaticamente.
  5. Exemplos de Entrada / Saída
Arquivo JSON carregado pelo programa
{
  "direcionado": false,
  "vertices": ["São Paulo", "Campinas", "Jundiaí", "Americana", "Limeira", "Rio Claro"],
  "arestas": [
    ["São Paulo", "Campinas", 90],
    ["São Paulo", "Jundiaí", 60],
    ["Campinas", "Americana", 45],
    ["Campinas", "Jundiaí", 40],
    ["Americana", "Limeira", 25],
    ["Limeira", "Rio Claro", 30]
  ]
}
Exemplo de Saída – BFS
BFS ordem:
São Paulo -> Campinas -> Jundiaí -> Americana -> Limeira -> Rio Claro
Exemplo de Saída – DFS
DFS ordem:
São Paulo -> Campinas -> Americana -> Limeira -> Rio Claro -> Jundiaí
Exemplo de Saída – Dijkstra/Bellman-Ford
São Paulo -> Limeira  
distância = 160  
caminho = ['São Paulo', 'Campinas', 'Americana', 'Limeira']
Ambos algoritmos retornaram resultados idênticos, pois o grafo não contém arestas negativas.

  6. Vídeo Demonstrativo
  Link do vídeo no YouTube  https://youtu.be/INsIeFleIr0

  8. Requisitos Atendidos 
✔ Requisitos Mínimos
Representação de grafo (lista de adjacência)
Inserção de vértices e arestas
Leitura de arquivo JSON
BFS e DFS implementados
Algoritmo de caminho mínimo (Dijkstra ou Bellman-Ford)
Código organizado em /src/
✔ Requisitos Avançados (Entregues)
Interface gráfica completa (Tkinter)
Visualização gráfica do grafo (NetworkX + Matplotlib)
Implementação de Dijkstra e Bellman-Ford
Exibição de distância + caminho mínimo
Logs automáticos
Sistema completo de entrada/saída JSON

  9. Autoria
Nome: João Pedro Lima Barbosa
matricula: 12401919
Disciplina: Estrutura de Dados – Grafos
Instituição: Centro universitario Santo Agostinho
Ano: 2025
