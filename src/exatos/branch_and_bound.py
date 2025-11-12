from typing import Dict, List, Tuple, Set
import math
import networkx as nx
from utils.graph_constructor import constroi_grafo
from utils.bb_utils import (
    gerar_rotas_factiveis,
    mapear_clientes_para_rotas,
    custo_minimo_por_cliente,
    calcular_lower_bound
)



def cvrp_branch_and_bound(
    G: nx.Graph,
    demands: Dict[int, int],
    depot: int,
    capacity: int
) -> Tuple[List[List[int]], float]:
    """
    Algoritmo exato com a lógica do branch and bound para o CVRP
    Retorna:
        (rotas, custo_total)
    """

    # lista de clientes
    clientes = [n for n in G.nodes if n != depot]
    if not clientes:
        return [], 0.0

   
    rotas = gerar_rotas_factiveis(G, clientes, demands, depot, capacity)
    routes_by_client = mapear_clientes_para_rotas(clientes, rotas)
    min_cost_per_client = custo_minimo_por_cliente(clientes, rotas, routes_by_client)

    # aqui decidimos representar as rotas como um conjunto e extraimos seus custos
    route_sets: List[Set[int]] = [set(rota) for rota, _ in rotas]
    route_costs: List[float] = [cost for _, cost in rotas]

    ALL_SET: Set[int] = set(clientes)

    # memoização: chave = frozenset(clientes_restantes) -> melhor custo observado
    memo_best: Dict[frozenset, float] = {}
    best_cost = math.inf
    best_solution: List[List[int]] = []

   
    # escolhemos o cliente entre os restantes com menor número de rotas possíveis, pra não abrir muitos ramos de uma vez
    def escolher_cliente(restantes: Set[int]) -> int:
        candidato = None
        min_ops = math.inf
        for c in restantes:
            ops = len(routes_by_client.get(c, []))
            if ops < min_ops:
                min_ops = ops
                candidato = c
        # candidato nunca será None se instância é viável
        return candidato if candidato is not None else next(iter(restantes))

    # função recursiva de branch and bound, a dfs vai testar todas as possibilidades que não foram podadas e o lb vai proteger o ramo com a solução exata que queremos
    def dfs(restantes: Set[int], current_routes: List[int], current_cost: float):
        nonlocal best_cost, best_solution

        # caso base: todos atendidos
        if not restantes:
            if current_cost < best_cost:
                best_cost = current_cost
                best_solution = [list(rotas[r][0]) for r in current_routes]
            return

        key = frozenset(restantes)
        prev = memo_best.get(key)
        if prev is not None and current_cost >= prev:
            # já visitamos este conjunto com custo melhor; pode podar
            return

        memo_best[key] = current_cost

        # poda por lower bound
        lb = current_cost + calcular_lower_bound(restantes, min_cost_per_client)
        if lb >= best_cost:
            return

        # escolher cliente para ramificar
        cliente = escolher_cliente(restantes)

        # para cada rota que contenha esse cliente, e que esteja contida nos restantes
        for ridx in routes_by_client.get(cliente, []):
            rset = route_sets[ridx]
            if rset.issubset(restantes):
                new_restantes = restantes - rset
                new_cost = current_cost + route_costs[ridx]

                # poda direta
                if new_cost >= best_cost:
                    continue
                # poda por lower bound no novo estado
                if new_cost + calcular_lower_bound(new_restantes, min_cost_per_client) >= best_cost:
                    continue

                current_routes.append(ridx)
                dfs(new_restantes, current_routes, new_cost)
                current_routes.pop()

    # inicia busca
    dfs(ALL_SET, [], 0.0)

    return best_solution, best_cost
