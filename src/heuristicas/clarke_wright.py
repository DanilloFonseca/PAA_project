from typing import Dict, List, Tuple
import networkx as nx

def clarke_wright(
    G: nx.Graph,
    demands: Dict[int, int],
    depot: int,
    capacity: int
) -> Tuple[List[List[int]], float]:
    """
    executa a heurística de Clarke & Wright.
    
    argumentos:
        G: grafo com pesos 'weight' nas arestas
        demands: dicionário {nó: demanda}
        depot: nó do depósito
        capacity: capacidade máxima do veículo
    retorna:
        (rotas, custo_total)
    """

    # inicialização do alg.
    clientes: List[int] = [n for n in G.nodes if n != depot]
    rotas: Dict[int, List[int]] = {i: [i] for i in clientes}
    rota_capacidade: Dict[int, int] = {i: demands[i] for i in clientes}
    rota_de: Dict[int, int] = {i: i for i in clientes}

    # aqui fazemos o cálculo das economias
    savings: List[Tuple[float, int, int]] = []
    for i in clientes:
        for j in clientes:
            if i < j:
                s_ij = G[depot][i]['weight'] + G[depot][j]['weight'] - G[i][j]['weight']
                savings.append((s_ij, i, j))
    savings.sort(reverse=True, key=lambda x: x[0])

    # mergeamos as sequências que nos ajudam na economia e excluímos as que não servem mais
    for _, i, j in savings:
        ri, rj = rota_de[i], rota_de[j]
        if ri == rj:
            continue
        capacidade_i, capacidade_j = rota_capacidade[ri], rota_capacidade[rj]
        if capacidade_i + capacidade_j > capacity:
            continue

        rota_i, rota_j = rotas[ri], rotas[rj]
        pode_mergear = False
        rota_mergeada: List[int] = []

        if rota_i[-1] == i and rota_j[0] == j:
            rota_mergeada = rota_i + rota_j; pode_mergear = True
        elif rota_i[0] == i and rota_j[-1] == j:
            rota_mergeada = rota_j + rota_i; pode_mergear = True
        elif rota_i[0] == i and rota_j[0] == j:
            rota_mergeada = list(reversed(rota_i)) + rota_j; pode_mergear = True
        elif rota_i[-1] == i and rota_j[-1] == j:
            rota_mergeada = rota_i + list(reversed(rota_j)); pode_mergear = True

        if pode_mergear:
            novo_id = min(ri, rj)
            rotas[novo_id] = rota_mergeada
            rota_capacidade[novo_id] = capacidade_i + capacidade_j
            for c in rota_mergeada:
                rota_de[c] = novo_id
            # remove rotas antigas pra limpar a lista
            for velho_id in (ri, rj):
                if velho_id != novo_id:
                    rotas.pop(velho_id, None)
                    rota_capacidade.pop(velho_id, None)

    # calcular custo total
    def custo_rota(rota: List[int]) -> float:
        if not rota:
            return 0.0
        custo = G[depot][rota[0]]['weight']
        for a, b in zip(rota, rota[1:]):
            custo += G[a][b]['weight']
        custo += G[rota[-1]][depot]['weight']
        return custo

    final_rotas = list(rotas.values())
    total_custo = sum(custo_rota(r) for r in final_rotas)
    return final_rotas, total_custo
