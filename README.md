# PROJETO E ANÁLISE DE ALGORITMOS

Este projeto implementa a **heurística de Clarke & Wright** para o **Problema de Roteamento de Veículos**, utilizando Python e a biblioteca **NetworkX** para modelagem de grafos.

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
│   │
│   ├── heuristicas/
│   │   └── clarke_wright.py
│   │
│   ├── utils/
│   │   ├── file_reader.py
│   │   └── graph_constructor.py
│   │
│   └── instancias/
│       ├── A-n32-k5.vrp
│       ├── A-n32-k5.sol
│       ├── A-n33-k5.vrp
│       ├── A-n33-k5.sol
│       ├── ...
│       └── A-n80-k10.vrp
│
└── .venv/

```

---

## Como rodar o projeto

### 1. Execute o programa principal

```bash
uv run python src/main.py
```

O script irá te perguntar se deseja fazer testes, se sim, ele vai listar todas as instâncias disponíveis na pasta `src/instancias/` e você poderá escolher qual deseja rodar, por exemplo:

```
Selecione uma instância:
1 - A-n32-k5.vrp
2 - A-n33-k5.vrp
...
Digite o número: 1
```
---

## Estrutura lógica

| Arquivo | Responsabilidade |
|----------|------------------|
| `utils/file_reader.py` | Lê o arquivo `.vrp` e extrai coordenadas, demandas, capacidade e depósito |
| `utils/graph_constructor.py` | Cria o grafo ponderado com as distâncias euclidianas entre clientes |
| `heuristicas/clarke_wright.py` | Implementa a heurística de Clarke & Wright |
| `src/main.py` | Orquestra a execução: lê instância, constrói grafo, executa heurística e imprime resultados |

---

## Autores

**Danillo Fonseca**  
**Pedro Miguel Varela** 