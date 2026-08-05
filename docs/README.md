# Benchmark de Estruturas de Dados - Validação de Usernames

A ideia desse projeto é realizar um experimento bem elaborado que visa contrapor soluções possíveis para o seguinte [Cenario](./CENARY.md)

Sistema de benchmark para comparar **Bloom Filter**, **Trie** e **HashSet** em cenários de validação de usernames únicos com alta concorrência.

## Uso do projeto

### 1. Compilar

```bash
cargo build --manifest-path rust/Cargo.toml --release 
```

### 2. Executar o experimento

```bash
chmod +x benchmark.sh
```
```bash
./benchmark.sh <load> <seed> <measure-interval> [--verbose]
```

Parâmetros posicionais:

- `load`: Quantidade de operações totais realizadas no experimento
- `seed`: Seed para reprodutibilidade
- `measure_interval`: Intervalo de medição de memória (-1 = apenas final) 
- `--verbose`: (Opcional) Imprime resultados na stdout


### 3. Analisar resultados

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
NEW username
```

**Operações:**

- `SET <username>`: Adiciona um usuário
- `GET <username>`: Verifica se existe (retorna true/false)
- `SUG <username>`: Autocomplete - retorna nome existente com esse prefixo
- `NEW <username>`: Retorna um nome disponível (tenta username, username1, username2, ...)

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
      "false_positives": 0,
      "false_positive_rate": 0.0,
      "total_time_ms": 1234.56,
      "ops_per_second": 810000.0,
      "final_memory_mb": 45.2,
      "memory_evolution": [
        {"operation": 10000, "delta_memory_mb": 0.5},
        {"operation": 20000, "delta_memory_mb": 1.2}
      ],
      "time_evolution": [
        {"operation": 10000, "elapsed_ms": 12.3},
        {"operation": 20000, "elapsed_ms": 25.6}
      ]
    },
    "trie": { ... },
    "bloom_filter": { ... }
  }
}
```

## Medição de Memória

### Como funciona

1. **Baseline**: Memória inicial da estrutura (vazia) é registrada via `deepsize`
2. **Processamento**: Operações são executadas
3. **Medições**: A cada intervalo N, `deep_size_of()` mede apenas a estrutura
4. **Delta**: Diferença entre memória inicial e atual

### Intervalo de Medição

- **N > 0**: Mede memória e tempo a cada N operações
- **N = -1**: Mede apenas no final

### Precisão

Usa crate `deepsize` para medir memória de cada estrutura individualmente:

- Mede apenas a estrutura testada (não o processo inteiro)
- Ground Truth HashSet não é medido (existe apenas para validar falsos positivos)
- Bloom Filter: mede o bitset (`num_bits / 8` bytes)
- Trie: mede chaves + overhead estimado por nó
- HashSet: medido via `#[derive(DeepSizeOf)]`

## Exemplos de Testes

TODO @(pagmaia): documentar e adicionar exemplos de testes

## Estruturas Implementadas

### HashSet

- Usa `std::collections::HashSet`
- **Vantagens**: Rápido para GET, suporte a SUG e NEW
- **Desvantagens**: Alto consumo de memória, lento para SUG em grandes datasets
- **Caso de uso**: Datasets pequenos a médios com muitas leituras

### Trie

- Usa crate `radix_trie` (trie compactada)
- **Vantagens**: Bom para SUG (autocomplete), memória razoável
- **Desvantagens**: Mais lento que HashSet para GET puro
- **Caso de uso**: Quando SUG é importante, datasets médios

### Bloom Filter

- Usa crate `fastbloom` (bitset otimizado)
- **Vantagens**: Muito baixo consumo de memória, rápido
- **Desvantagens**: Falsos positivos, sem SUG, sem remoção
- **Caso de uso**: Verificação rápida com tolerância a falsos positivos
- **Falsos positivos**: Mensurados via Ground Truth HashSet paralelo

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
