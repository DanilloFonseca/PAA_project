import random
from typing import List, Dict
import networkx as nx
from .bb_utils import custo_rota


def custo_total(G: nx.Graph, rotas: List[List[int]], depot: int) -> float:
    """ 
    retorna o custo total do conjunto de rotas 
    """
    return sum(custo_rota(G, r, depot) for r in rotas)


def numero_veiculos_estimado(demands: Dict[int, int], capacity: int) -> int:
    """
    faz uma estimativa do número necessário de veículos baseada apenas no volume total de demanda dividido pela capacidade
    """
    total = sum(demands.values())
    n = total // capacity
    if total % capacity != 0:
        n += 1
    return max(1, n)

def criar_LRC(alpha: float, G: nx.Graph, current_node: int, candidatos: List[int]) -> List[int]:
    """
    constrói a Lista Restrita de Candidatos (LRC)
    """
    if not candidatos:
        return []
    distancias = []
    for c in candidatos:
        distancias.append((c, G[current_node][c]['weight']))
    distancias.sort(key=lambda x: x[1])
    dists = [d for (_, d) in distancias]
    dmin = dists[0]
    dmax = dists[-1]
    limite = dmin + alpha * (dmax - dmin)
    lrc = [c for (c, d) in distancias if d <= limite]
    if not lrc:
        lrc = [distancias[0][0]]
    return lrc


def escolher_da_LRC_random(lrc: List[int]) -> int:
    return random.choice(lrc)

def pode_adicionar(demand: int, capacidade_restante: int) -> bool:
    """
    verifica se a demanda de um cliente cabe na capacidade restante do veículo
    """
    return demand <= capacidade_restante
