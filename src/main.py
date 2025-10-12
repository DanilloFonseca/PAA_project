import os
from utils.file_reader import le_arquivo
from utils.graph_constructor import constroi_grafo
from heuristicas.clarke_wright import clarke_wright


def selecionar_instancia(diretorio: str) -> str:
    """
    vai todas as instâncias .vrp disponíveis e permite o usuário escolher uma.
    """
    arquivos = sorted(
        [f for f in os.listdir(diretorio) if f.endswith(".vrp")]
    )
    if not arquivos:
        raise FileNotFoundError(f"Nenhum arquivo .vrp encontrado em {diretorio}")

    print("\nInstâncias disponíveis:\n")
    for i, nome in enumerate(arquivos, start=1):
        print(f"{i:2d}. {nome}")

    while True:
        try:
            escolha = int(input("\nSelecione o número da instância que deseja rodar: "))
            if 1 <= escolha <= len(arquivos):
                return os.path.join(diretorio, arquivos[escolha - 1])
            else:
                print("Número inválido. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Digite um número válido.")


def main() -> None:
    """
    executa o fluxo principal com o controlador:
      1. seleciona instância
      2. lê arquivo .vrp
      3. constrói grafo
      4. executa clarke & wright
      5. exibe resultados
    """
    while True:
        print("\n")
        print('##' * 40)
        controlador: int = int(input("Bem-vindo aos testes!!\n\nDigite 1 para continuar ou 0 para encerrar: "))
        if controlador == 0:
            break
        if controlador != 1:
            continue

        caminho_arquivo: str = selecionar_instancia("instancias")

        print(f"\nLendo instância: {caminho_arquivo}\n")
        coords, demands, capacity, depot = le_arquivo(caminho_arquivo)
        G = constroi_grafo(coords)

        rotas, custo_total = clarke_wright(G, demands, depot, capacity)

        print("\nRotas encontradas:\n")
        for idx, rota in enumerate(rotas, start=1):
            rota_completa = [depot] + rota + [depot]
            print(f" Rota {idx}: {' ---> '.join(map(str, rota_completa))}")

        print(f"\nCusto total: {custo_total:.2f}")
        print(f"Veículos utilizados: {len(rotas)}\n")


if __name__ == "__main__":
    main()
