# PROJETO E ANÁLISE DE ALGORITMOS

Este projeto implementa a **heurística de Clarke & Wright** e o **algoritmo exato de Branch and Bound** para o **Problema de Roteamento de Veículos**, utilizando Python e a biblioteca **NetworkX** para modolagem de grafos.

---

## Tecnologias e dependências principais

- **Python** ≥ 3.12  
- **uv** (gerenciador de ambientes e pacotes)  
- **NetworkX**  
- **typing / type hints** para tipagem estática  

---

## Como configurar o ambiente

### 1. Instale o `uv`

---

### 2. Crie o ambiente Python

O `uv` cria e gerencia o ambiente automaticamente com base no arquivo `pyproject.toml`:

```bash
uv sync
```

> Isso instalará automaticamente o Python da versão correta (definida em `.python-version` ou `pyproject.toml`) e todas as dependências.

Para ativar o ambiente:
```bash
source .venv/bin/activate
```

---

## Estrutura do projeto

```
prv_project/
├── pyproject.toml
├── README.md
├── uv.lock
├── src/
│   ├── main.py
|   |
|   ├── exatos/
|   |   └── branch_and_bound.py
│   │
│   ├── heuristicas/
│   │   └── clarke_wright.py
│   │
│   ├── utils/
│   │   ├── file_reader.py
│   │   ├── graph_constructor.py
|   |   ├── bb_utils.py
|   |   └── main_utils.py
│   │
│   └── instancias/
│       ├── A-n32-k5.vrp
│       ├── A-n32-k5.sol
│       ├── A-n33-k5.vrp
│       ├── A-n33-k5.sol
│       ├── ...
│       └── mini-n8-k2.vrp
│
└── .venv/

```

---

## Como rodar o projeto

### 1. Execute o programa principal

```bash
uv run python src/main.py
```

O script irá te perguntar se deseja fazer testes, se sim, ele vai listar todas as instâncias disponíveis na pasta `src/instancias/` e você poderá escolher qual deseja rodar e também qual algoritmo, por exemplo:

```
Selecione uma instância:
1 - A-n32-k5.vrp
2 - A-n33-k5.vrp
...
37 - mini-n8-k2.vrp
Digite o número: 1

Selecione o algoritmo para execução:
1. Clarke & Wright (Heurístico)
2. Branch and Bound (Exato)
```
Para testar o algoritmo de Branch and Bound, recomendamos escolher as instâncias com prefixo "mini". Ainda assim, algumas instâncias desse tipo variam seu tempo de execução entre poucos segundos até 3 horas de processamento para encontrar o resultado exato.
---

## Estrutura lógica

| Arquivo | Responsabilidade |
|----------|------------------|
| `utils/file_reader.py` | Lê o arquivo `.vrp` e extrai coordenadas, demandas, capacidade e depósito |
| `utils/graph_constructor.py` | Cria o grafo ponderado com as distâncias euclidianas entre clientes |
| `utils/bb_utils.py` | Cria funções necessárias para a execução do algoritmo de Branch and Bound |
| `utils/main_utils.py` | Cria funções necessárias para o iniciar o projeto |
| `exatos/branch_and_bound.py` | Implementa o algoritmo exato de Branch and Bound |
| `heuristicas/clarke_wright.py` | Implementa a heurística de Clarke & Wright |
| `src/main.py` | Orquestra a execução |

---

## Autores

**Danillo Fonseca**  
**Pedro Miguel Varela** 