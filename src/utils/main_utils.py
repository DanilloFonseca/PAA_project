import os
import time
from typing import List, Tuple, Dict
import networkx as nx

from utils.file_reader import le_arquivo
from utils.graph_constructor import constroi_grafo
from heuristicas.clarke_wright import clarke_wright
from exatos.branch_and_bound import cvrp_branch_and_bound
from meta_heuristicas.grasp import grasp_cvrp


def selecionar_instancia(diretorio: str) -> str:
    """
    vai todas as instâncias .vrp disponíveis e permite o usuário escolher uma.
    """
    base_dir: str = os.path.dirname(__file__)
    full_dir: str = os.path.join(os.path.dirname(base_dir), diretorio)

    arquivos: List[str] = sorted(
        [f for f in os.listdir(full_dir) if f.endswith(".vrp")]
    )
    if not arquivos:
        raise FileNotFoundError(f"Nenhum arquivo .vrp encontrado em {full_dir}")

    print("\nInstâncias disponíveis:\n")
    for i, nome in enumerate(arquivos, start=1):
        print(f"{i:2d}. {nome}")

    while True:
        try:
            escolha: int = int(input("\nSelecione o número da instância que deseja rodar: "))
            if 1 <= escolha <= len(arquivos):
                return os.path.join(full_dir, arquivos[escolha - 1])
            else:
                print("Número inválido. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Digite um número válido.")


def selecionar_algoritmo() -> str:
    """
    permite o usuário escolher qual algoritmo será executado
    """
    print("\nSelecione o algoritmo para execução:\n")
    print("1. Clarke & Wright (Heurístico)")
    print("2. Branch and Bound (Exato)")
    print("3. GRASP (Meta-heurística)")

    while True:
        try:
            opcao: int = int(input("\nDigite o número da opção desejada: "))

            if opcao == 1:
                return "clarke_wright"
            elif opcao == 2:
                return "branch_and_bound"
            elif opcao == 3:
                return "grasp"
            else:
                print("Número inválido. Escolha 1, 2 ou 3.")
        except ValueError:
            print("Entrada inválida. Digite um número válido.")


def executar_algoritmo(G: nx.Graph,
                       demands: Dict[int, int],
                       depot: int,
                       capacity: int,
                       algoritmo: str) -> Tuple[List[List[int]], float]:
    """
    Executa o algoritmo selecionado e retorna as rotas e o custo total
    """

    if algoritmo == "clarke_wright":
        rotas, custo = clarke_wright(G, demands, depot, capacity)
        return rotas, custo

    elif algoritmo == "branch_and_bound":
        rotas, custo = cvrp_branch_and_bound(G, demands, depot, capacity)
        return rotas, custo

    elif algoritmo == "grasp":
        print("\n---- Configuração do GRASP ----")
        try:
            max_it = int(input("Número de iterações: "))
        except Exception:
            max_it = 10
            print("Número de iterações inválido, usando 10")
        try:
            alpha_in = input("Entre com o valor do alpha: ").strip()
            if alpha_in == "":
                alpha = 0.5
            else:
                alpha = float(alpha_in)
                if not (0.0 <= alpha <= 1.0):
                    print("Alpha fora do intervalo; usando 0.5")
                    alpha = 0.5
        except Exception:
            alpha = 0.5
            print("Entrada inválida para alpha; usando 0.5")

        rotas, custo = grasp_cvrp(
            G=G,
            demands=demands,
            depot=depot,
            capacity=capacity,
            alpha=alpha,
            max_iterations=max_it,
        )
        return rotas, custo

    else:
        raise ValueError("Opção inválida")



def imprimir_resultados(
    rotas: List[List[int]],
    custo_total: float,
    depot: int,
    tempo_total: float
) -> None:
    """
    exibe as rotas, custo total e tempo de execução
    """
    print("\nRotas encontradas:\n")
    for idx, rota in enumerate(rotas, start=1):
        rota_completa: List[int] = [depot] + rota + [depot]
        print(f" Rota {idx}: {' ---> '.join(map(str, rota_completa))}")

    print(f"\nCusto total: {custo_total:.2f}")
    print(f"Veículos utilizados: {len(rotas)}")
    print(f"Tempo total de execução: {tempo_total:.4f} segundos\n")


def main() -> None:
    """
    executa o fluxo principal:
      1. seleciona instância
      2. escolhe algoritmo
      3. lê arquivo .vrp
      4. constrói grafo
      5. executa algoritmo
      6. mostra resultados
    """
    while True:
        print("\n" + "##" * 40)
        controlador: str = input(
            "\n\nBem-vindo aos testes!!\n\nDigite 1 para continuar ou 0 para encerrar: "
        ).strip()

        if controlador == "0":
            print("\nEncerrando o programa...\n")
            break
        elif controlador != "1":
            continue

        caminho_arquivo: str = selecionar_instancia("instancias")
        print(f"\nLendo instância: {caminho_arquivo}\n")

        coords, demands, capacity, depot = le_arquivo(caminho_arquivo)
        G: nx.Graph = constroi_grafo(coords)

        algoritmo: str = selecionar_algoritmo()

        inicio: float = time.time()
        rotas, custo_total = executar_algoritmo(G, demands, depot, capacity, algoritmo)
        fim: float = time.time()

        imprimir_resultados(rotas, custo_total, depot, fim - inicio)
