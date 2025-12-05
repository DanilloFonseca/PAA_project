from typing import Dict, List, Tuple
import networkx as nx

from utils.grasp_utils import (
    criar_LRC, 
    escolher_da_LRC_random, 
    custo_rota, 
    custo_total,
    numero_veiculos_estimado, 
    pode_adicionar
)

def greedy_search(G: nx.Graph, demands: Dict[int, int], depot: int, capacity: int, alpha: float) -> List[List[int]]:
    clientes = [n for n in G.nodes() if n != depot]
    clientes_nao_visitados = set(clientes)
    n_veiculos = numero_veiculos_estimado(demands, capacity)

    rotas: List[List[int]] = [[] for _ in range(n_veiculos)]

    for k in range(n_veiculos):
        capacidade_restante = capacity
        ultimo = depot
        while True:
            candidatos = [c for c in clientes_nao_visitados if pode_adicionar(demands.get(c, 0), capacidade_restante)]
            if not candidatos:
                break
            lrc = criar_LRC(alpha, G, ultimo, candidatos)
            escolhido = escolher_da_LRC_random(lrc)
            rotas[k].append(escolhido)
            capacidade_restante -= demands.get(escolhido, 0)
            clientes_nao_visitados.remove(escolhido)
            ultimo = escolhido
        if not clientes_nao_visitados:
            break

    while clientes_nao_visitados:
        rotas.append([])
        capacidade_restante = capacity
        ultimo = depot
        while True:
            candidatos = [c for c in clientes_nao_visitados if pode_adicionar(demands.get(c, 0), capacidade_restante)]
            if not candidatos:
                break
            lrc = criar_LRC(alpha, G, ultimo, candidatos)
            escolhido = escolher_da_LRC_random(lrc)
            rotas[-1].append(escolhido)
            capacidade_restante -= demands.get(escolhido, 0)
            clientes_nao_visitados.remove(escolhido)
            ultimo = escolhido

    rotas = [r for r in rotas if r]
    return rotas

def local_search(G: nx.Graph, rotas: List[List[int]], depot: int) -> List[List[int]]:
    """
    percorre a lista pra fazer trocas adjacentes
    """
    melhor = [r[:] for r in rotas]
    improved = True
    while improved:
        improved = False
        for k, rota in enumerate(melhor):
            for i in range(len(rota) - 1):
                antes = custo_rota(G, rota, depot)
                rota[i], rota[i+1] = rota[i+1], rota[i]
                depois = custo_rota(G, rota, depot)
                if depois < antes:
                    improved = True
                else:
                    rota[i], rota[i+1] = rota[i+1], rota[i]
            melhor[k] = rota
    return melhor

def grasp_cvrp(
    G: nx.Graph,
    demands: Dict[int, int],
    depot: int,
    capacity: int,
    alpha: float = 0.5,
    max_iterations: int = 10,
) -> Tuple[List[List[int]], float]:

    best_solution = None
    best_cost = float('inf')

    for _ in range(max_iterations):
        candidatoGreedy = greedy_search(G, demands, depot, capacity, alpha)
        candidato = local_search(G, candidatoGreedy, depot)
        custo = custo_total(G, candidato, depot)
        if custo < best_cost:
            best_cost = custo
            best_solution = candidato

    if best_solution is None:
        return [], 0.0
    return best_solution, best_cost
