from typing import Dict, Tuple
import math
import networkx as nx

def distancia_euclides(a: Tuple[float, float], b: Tuple[float, float]) -> int:
    """
    calcula a distância euclidiana arredondada, exigência do file pra testes.
    """
    return int(round(math.hypot(a[0] - b[0], a[1] - b[1])))

def constroi_grafo(coords: Dict[int, Tuple[float, float]]) -> nx.Graph:
    """
    constrói um grafo não-direcionado com pesos de aresta baseados na distância euclidiana.
    
    argumentos:
        coords: dicionário {nó: (x, y)}.
    retorna:
        Grafo NetworkX com atributo 'weight' nas arestas.
    """
    G = nx.Graph()
    for i, coord_i in coords.items():
        for j, coord_j in coords.items():
            if i != j:
                distancia = distancia_euclides(coord_i, coord_j)
                G.add_edge(i, j, weight=distancia)
    return G
