from typing import Dict, Tuple, Optional

def le_arquivo(caminho_arquivo: str) -> Tuple[Dict[int, Tuple[float, float]], Dict[int, int], int, int]:
    """
    lê uma instância CVRP no formato TSPLIB como estabelecido pelos testes e retorna:
    - coords: dicionário {nó: (x, y)}
    - demands: dicionário {nó: demanda}
    - capacity: capacidade máxima do veículo
    - depot: identificador do depósito
    
    argumentos:
        caminho_arquivo (str): caminho para o arquivo da instância.
    retorna:
        Tuple[Dict[int, Tuple[float, float]], Dict[int, int], int, int]
    """
    coords: Dict[int, Tuple[float, float]] = {}
    demands: Dict[int, int] = {}
    capacity: Optional[int] = None
    depot: Optional[int] = None

    modo: Optional[str] = None

    with open(caminho_arquivo, "r") as f:
        for linha in f:
            linha = linha.strip()
            if not linha or linha == "EOF":
                continue

            if linha.startswith("CAPACITY"):
                capacity = int(linha.split(":")[1]) if ":" in linha else int(linha.split()[1])
                continue
            if linha.startswith("NODE_COORD_SECTION"):
                modo = "coords"; continue
            if linha.startswith("DEMAND_SECTION"):
                modo = "demand"; continue
            if linha.startswith("DEPOT_SECTION"):
                modo = "depot"; continue
            if any(linha.startswith(key) for key in ["NAME", "COMMENT", "TYPE", "DIMENSION", "EDGE_WEIGHT_TYPE"]):
                continue

            partes = linha.split()
            if modo == "coords" and len(partes) >= 3:
                idx, x, y = int(partes[0]), float(partes[1]), float(partes[2])
                coords[idx] = (x, y)
            elif modo == "demand" and len(partes) >= 2:
                idx, demand = int(partes[0]), int(partes[1])
                demands[idx] = demand
            elif modo == "depot" and partes[0] != "-1":
                depot = int(partes[0])

    if capacity is None or depot is None:
        raise ValueError("Arquivo de instância inválido: falta CAPACITY ou DEPOT_SECTION")

    return coords, demands, capacity, depot
