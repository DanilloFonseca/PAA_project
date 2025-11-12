from typing import Dict, List, Tuple, Iterable
import itertools
import math
import networkx as nx


def calcular_distancia(G: nx.Graph, a: int, b: int) -> float:
    """retorna a distância (peso da aresta) entre dois nós"""
    return G[a][b]['weight']


def custo_rota(G: nx.Graph, rota: Tuple[int, ...], depot: int) -> float:
    """
    calcula o custo total de uma rota, incluindo ida e volta ao depósito
    """

    # caso especial aqui
    if len(rota) == 1:
        c = rota[0]
        return calcular_distancia(G, depot, c) + calcular_distancia(G, c, depot)

    custo = calcular_distancia(G, depot, rota[0])
    for a, b in zip(rota, rota[1:]):
        custo += calcular_distancia(G, a, b)
    custo += calcular_distancia(G, rota[-1], depot)
    return custo


def gerar_rotas_factiveis(
    G: nx.Graph, clientes: List[int], demands: Dict[int, int],
    depot: int, capacity: int
) -> List[Tuple[List[int], float]]:
    """
    gera todas as rotas factíveis, ou seja, conjuntos de clientes cuja soma de demandas é menor ou igual a capacidade do veículo. pra cada rota válida, calcula o custo mínimo de percorrer os clientes em qualquer ordem (permutações)
    """
    rotas = []
    for r in range(1, len(clientes) + 1):
        for comb in itertools.combinations(clientes, r):
            if sum(demands[c] for c in comb) <= capacity:
                melhor = math.inf
                for perm in itertools.permutations(comb):
                    custo = custo_rota(G, perm, depot)
                    if custo < melhor:
                        melhor = custo
                rotas.append((list(comb), melhor))
    rotas.sort(key=lambda x: x[1] / len(x[0]))  # priorizar custo médio
    return rotas


def mapear_clientes_para_rotas(
    clientes: List[int],
    rotas: List[Tuple[List[int], float]]
) -> Dict[int, List[int]]:
    """
    gera um dicionário que, para cada cliente, lista os índices das rotas que contêm ele
    """
    rotas_por_cliente = {c: [] for c in clientes}
    for idx, (rota, _) in enumerate(rotas):
        for c in rota:
            rotas_por_cliente[c].append(idx)
    return rotas_por_cliente


def custo_minimo_por_cliente(
    clientes: List[int],
    rotas: List[Tuple[List[int], float]],
    rotas_por_cliente: Dict[int, List[int]]
) -> Dict[int, float]:
    """
    Pra cada cliente, calcula o menor custo médio (custo total / num. de clientes) entre todas as rotas que o incluem. Usado para o cálculo do lower bound.
    """
    min_cost = {}
    for c in clientes:
        custos_medios = [
            rotas[i][1] / len(rotas[i][0])
            for i in rotas_por_cliente[c]
        ]
        min_cost[c] = min(custos_medios) if custos_medios else math.inf
    return min_cost


def calcular_lower_bound(
    clientes_restantes: Iterable[int],
    min_cost_per_customer: Dict[int, float]
) -> float:
    """
    retorna uma cota inferior do custo adicional mínimo necessário para atender os clientes restantes.
    """
    return sum(min_cost_per_customer[c] for c in clientes_restantes)
