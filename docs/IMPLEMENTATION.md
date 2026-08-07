# Implementação - Benchmark de Estruturas de Dados

## Requisitos Atendidos

### 1. Camada Rust

- Implementação de 3 estruturas de dados via crates e std
- **HashSet**: Usa `std::collections::HashSet`
- **Trie**: Usa crate `radix_trie` (trie compactada)
- **Bloom Filter**: Usa crate `fastbloom` (bitset otimizado)
- CLI com `clap`: `<file_path> <measure_interval> <test_id> <save_path> [OPTIONS]`
- Flags seletivas: `--bloom`, `--trie`, `--hashset`, `--verbose`
- Leitura de arquivo `.txt` com operações (SET, GET, SUG, NEW)
- Medição de memória com `deepsize` (por estrutura individual)
- Saída JSON com métricas

### 2. Medição de Memória

- Usa crate `deepsize` (não GlobalAlloc)
- Mede apenas a estrutura testada, não o processo inteiro
- Delta de memória (diferença entre inicial e atual)
- Intervalo configurável:
  - `-1`: Mede apenas no final
  - `> 0`: Mede a cada N operações
- Evolução de memória registrada no JSON
- Ground Truth HashSet não é medido

### 3. Medição de Tempo

- `Instant::now()` apenas envolvendo a operação da estrutura
- Operações no Ground Truth ficam fora do timer
- `time_evolution`: tempo decorrido a cada N operações
- `ops_per_second`: operações por segundo

### 4. Operações

- `SET <username>`: Adiciona um usuário
- `GET <username>`: Verifica se existe (true/false)
- `SUG <prefix>`: Autocomplete - retorna nome existente com o prefixo
- `NEW <username>`: Retorna nome disponível (tenta username, username1, username2, ...)

#### Implementação por Estrutura

| Operação | Bloom Filter                                                                           | Trie                                                                                          | HashSet                                                                                  |
| -------- | -------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| **SET**  | `filter.insert(key)` — insere no filtro com 1% taxa de falso positivo                  | `trie.insert(key, true)` — insere chave com valor booleano                                    | `set.insert(key)` — insere string no conjunto                                            |
| **GET**  | `filter.contains(key)` — verifica presença (pode ter falsos positivos)                 | `trie.get(key).is_some()` — busca exata na árvore                                             | `set.contains(key)` — busca exata no hash                                                |
| **SUG**  | Retorna string vazia — Bloom Filter não armazena chaves                                | `trie.iter().find(\|k\| k.starts_with(prefix))` — itera e encontra primeira chave com prefixo | `set.iter().sort().find(\|c\| c.starts_with(prefix))` — ordena e encontra primeira chave |
| **NEW**  | Loop: testa `key`, `key1`, `key2`... até encontrar não presente em `filter.contains()` | Loop: testa `key`, `key1`, `key2`... até encontrar não presente em `trie.get()`               | Loop: testa `key`, `key1`, `key2`... até encontrar não presente em `set.contains()`      |

### 5. Ground Truth HashSet

- HashSet paralelo como fonte da verdade para todas as estruturas
- Compara resposta da estrutura com o GT a cada GET
- Conta falsos positivos (estrutura diz true, GT diz false)
- `false_positive_rate` = false_positives / hits
- GT não é medido em memória nem em tempo

### 6. Output Verbose

- Cada operação imprime resultado:
  - **SET**: Newline
  - **GET**: `true` ou `false`
  - **SUG**: Nome existente ou vazio
  - **NEW**: Nome disponível
- Tabular para análise posterior

### 7. Documentação

- [README.md](./README.md) - Visão geral do projeto
- [CENARY.md](./CENARY.md) - Cenário que o projeto busca resolver
- [IMPLEMENTATION.md](./IMPLEMENTATION.md) - Este arquivo

## Componentes Principais

### `rust/src/structure.rs`

- Trait `DataStructure`: interface comum para todas as estruturas
- Métodos: `add()`, `contains()`, `suggest()`, `new_name()`, `name()`
- Supertrait: `DeepSizeOf` (para medir memória)

### `rust/src/main.rs`

- CLI com `clap::Parser`
- Função `parse_operations()`: Lê arquivo `.txt`
- Função `run_benchmark<S: DataStructure>()`: Loop genérico
  - Mede memória inicial via `deep_size_of()`
  - Processa operações (SET, GET, SUG, NEW)
  - Mantém Ground Truth HashSet (não medido)
  - Registra evolução de memória e tempo a cada N ops
  - Conta hits, misses, falsos positivos
  - Calcula ops_per_second e false_positive_rate

### `rust/src/bloom_filter.rs`

- `BloomFilterStructure`: Wrapper para `fastbloom::BloomFilter`
- Configurado para 10M elementos com 1% de falsos positivos
- `DeepSizeOf` manual: mede `num_bits() / 8` (bitset)

### `rust/src/trie.rs`

- `TrieStructure`: Wrapper para `radix_trie::Trie<String, bool>`
- `suggest()`: iter sobre chaves, filtra por prefixo
- `DeepSizeOf` manual: soma chaves + overhead por nó

### `rust/src/hashset.rs`

- `HashSetStructure`: Wrapper para `std::collections::HashSet<String>`
- `DeepSizeOf` via `#[derive(DeepSizeOf)]`

### `src/generate_test_data.py`

- Gera operações SET, GET, SUG, NEW
- Configurável: total de ops, proporção leitura/escrita, seed, prefixo

## Exemplo de Uso

### Compilar

```bash
cd rust && cargo build --release && cd ..
```

### Gerar dados

```bash
uv run -m src.generate_test_data test_100k.txt 100000 0.5
```

### Executar

```bash
./rust/target/release/benchmark \
  data/tests/txt/test_100k.txt \
  10000 \
  test_100k \
  data/tests/json \
  --verbose
```

### Executar apenas Bloom Filter

```bash
./rust/target/release/benchmark \
  data/tests/txt/test_100k.txt \
  10000 \
  test_bloom \
  data/tests/json \
  --bloom
```

### Resultado

```json
{
  "test_id": "test_100k",
  "total_operations": 100000,
  "results": {
    "bloom_filter": {
      "structure": "bloom_filter",
      "hits": 50000,
      "misses": 50000,
      "false_positives": 120,
      "false_positive_rate": 0.0024,
      "total_time_ms": 1234.56,
      "ops_per_second": 81000.0,
      "final_memory_mb": 11.9,
      "memory_evolution": [...],
      "time_evolution": [...]
    },
    ...
  }
}
```

## Características Técnicas

### Medição de Memória

- **Método**: `deepsize` crate (não GlobalAlloc)
- **Precisão**: Mede apenas a estrutura testada
- **Overhead**: Mínimo (apenas quando chamado)
- **Ground Truth**: Não medido

### Medição de Tempo

- **Método**: `std::time::Instant`
- **Precisão**: Nanosegundos
- **Conversão**: Para milissegundos no JSON
- **GT**: Operações no GT ficam fora do timer

### Crates Usadas

- **HashSet**: `std::collections::HashSet<String>`
- **Trie**: `radix_trie::Trie<String, bool>` (trie compactada)
- **Bloom Filter**: `fastbloom::BloomFilter` (bitset otimizado)
- **CLI**: `clap` (derive)
- **Memória**: `deepsize` (DeepSizeOf trait)
- **Serialization**: `serde` / `serde_json`
