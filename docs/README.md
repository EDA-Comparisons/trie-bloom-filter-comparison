# Benchmark de Estruturas de Dados - Validação de Usernames

A ideia desse projeto é realizar um experimento bem elaborado que visa contrapor soluções possíveis para o seguinte [Cenario](./CENARY.md)

Sistema de benchmark para comparar **Bloom Filter**, **Trie** e **HashSet** em cenários de validação de usernames únicos com alta concorrência.

## Uso do projeto

### 1. Compilar

```bash
cargo build --release
```

### 2. Gerar dados de teste

```bash
uv run -m src.generate_test_data test_data.txt 1000000 0.5
```

Parâmetros:

- `test_data.txt`: Arquivo de saída
- `1000000`: Número total de operações
- `0.5`: Proporção de leituras (0.0-1.0)

### 3. Executar benchmark

```bash
./target/release/benchmark <file_path> <measure_interval> <test_id> <save_path> [--verbose]
```

Parâmetros:

- `file_path`: Arquivo de operações
- `measure_interval`: Intervalo de medição de memória (-1 = apenas final)
- `test_1`: ID do teste (gera `test_1.json`)
- `save_path`: Caminho para salvar os Jsons
- `--verbose`: (Opcional) Imprime resultados na stdout

### 4. Analisar resultados

TODO @(pagmaia): documentar as analises

## Formato de Dados

### Arquivo de Operações (entrada)

Cada linha: `<OPERAÇÃO> <DADO>`

```
SET alice
GET alice
SUG al
SET bob
GET bob
GET charlie
```

**Operações:**

- `SET <username>`: Adiciona um usuário
- `GET <username>`: Verifica se existe (retorna true/false)
- `SUG <username>`: Sugere próximo username disponível

### Arquivo de Resultados (saída)

Arquivo JSON com métricas de cada estrutura:

```json
{
  "test_id": "test_1",
  "total_operations": 1000000,
  "results": {
    "hashset": {
      "structure": "hashset",
      "hits": 500000,
      "misses": 500000,
      "total_time_ms": 1234.56,
      "final_memory_mb": 45.2,
      "memory_evolution": [
        {"operation": 10000, "delta_memory_mb": 0.5},
        {"operation": 20000, "delta_memory_mb": 1.2}
      ]
    },
    "trie": { ... },
    "bloom_filter": { ... }
  }
}
```

## Medição de Memória

### Como funciona

1. **Carregamento**: Arquivo é carregado em memória
2. **Baseline**: Memória inicial é registrada
3. **Processamento**: Operações são executadas
4. **Medições**: A cada intervalo N, memória é medida
5. **Delta**: Diferença entre memória inicial e atual

### Intervalo de Medição

- **N > 0**: Mede memória a cada N operações
- **N = -1**: Mede apenas no final
- **N = 0**: Não mede (não recomendado)

### Precisão

Usa `GlobalAlloc` em Rust para rastreamento preciso de alocações:

- Conta cada `alloc()` e `dealloc()`
- Não inclui overhead do sistema operacional
- Não inclui stack memory

## Exemplos de Testes

TODO @(pagmaia): documentar e adicionar exemplos de testes

## Estruturas Implementadas

### HashSet

- **Vantagens**: Rápido para GET, suporte a SUG
- **Desvantagens**: Alto consumo de memória, lento para SUG em grandes datasets
- **Caso de uso**: Datasets pequenos a médios com muitas leituras

### Trie

- **Vantagens**: Bom para SUG, memória razoável
- **Desvantagens**: Mais lento que HashSet para GET puro
- **Caso de uso**: Quando SUG é importante, datasets médios

### Bloom Filter

- **Vantagens**: Muito baixo consumo de memória, rápido
- **Desvantagens**: Falsos positivos, sem SUG, sem remoção
- **Caso de uso**: Verificação rápida com tolerância a falsos positivos

### Memória não muda

Esperado para Bloom Filter (tamanho fixo). Para HashSet/Trie, verifique se está fazendo SET operations.

## IMPORTANTE!

- **Compilação**: Release mode (`--release`) para resultados realistas
- **Reprodutibilidade**: Use seed fixo em `generate_test_data.py`
- **Múltiplas runs**: Execute cada teste várias vezes para média

## Referências

- [Bloom Filter](https://en.wikipedia.org/wiki/Bloom_filter)
- [Trie Data Structure](https://en.wikipedia.org/wiki/Trie)
- [Rust GlobalAlloc](https://doc.rust-lang.org/std/alloc/trait.GlobalAlloc.html)
  TODO @(pagmaia): Assumindo que vai usar pandas, caso não remover
- [Pandas Documentation](https://pandas.pydata.org/docs/)
