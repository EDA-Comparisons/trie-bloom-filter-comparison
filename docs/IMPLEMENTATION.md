# Implementação - Benchmark de Estruturas de Dados

## Requisitos Atendidos

### 1. Camada Rust

- Implementação de 3 estruturas de dados
- **HashSet**: Usa `std::collections::HashSet`
- **Trie**: Usa `std::collections::BTreeMap`
- **Bloom Filter**: Usa `Vec<bool>`
- CLI com argumentos: `<file_path> <measure_interval> <test_id> <save_path> [--verbose]`
- Leitura de arquivo `.txt` com operações (SET, GET, SUG)
- Medição de memória com `GlobalAlloc`
- Saída JSON com métricas

### 2. Medição de Memória

- Rastreamento em tempo real com `GlobalAlloc`
- Delta de memória (diferença entre inicial e atual)
- Intervalo configurável:
- `-1`: Mede apenas no final
- `> 0`: Mede a cada N operações
- Evolução de memória registrada no JSON

### 3. I/O de Dados

- Entrada: Arquivo `.txt` com formato `<OP> <DATA>`
- Saída: JSON com métricas detalhadas
- Sem interferência em memória ou runtime
- Diretório de saída configurável via argumento

### 4. Output Verbose

- Cada operação imprime resultado:
- **SET**: Newline (confirmação)
- **GET**: `true` ou `false`
- **SUG**: Nome sugerido ou vazio
- Tabular para análise posterior

### 5. Documentação

- [README.md](./README.md) - Visão geral do projeto
- [CENARY.md](./CENARY.md) - Cenário que o projeto busca resolver
- [IMPLEMENTATION.md](./IMPLEMENTATION.md) - Este arquivo

## Componentes Principais

### `rust/src/main.rs`

- Função `main()`: Processa argumentos CLI
- Função `parse_operations()`: Lê arquivo `.txt`
- Função `run_benchmark()`: Executa benchmark para uma estrutura
  - Mede memória inicial
  - Processa operações
  - Registra evolução de memória
  - Calcula tempo total
  - Conta hits/misses

### `rust/src/memory.rs`

- `TrackingAllocator`: Implementa `GlobalAlloc`
- Rastreia alocações/desalocações
- `get_allocated_bytes()`: Retorna total alocado

### `rust/src/hashset.rs`

- `HashSetStructure`: Wrapper para `HashSet<String>`
- `add()`: Insere elemento
- `contains()`: Verifica existência
- `suggest()`: Retorna próximo lexicograficamente

### `rust/src/trie.rs`

- `TrieNode`: Nó com `BTreeMap<char, Box<TrieNode>>`
- `TrieStructure`: Trie completa
- `add()`: Insere string
- `contains()`: Verifica existência
- `suggest()`: Retorna próxima palavra no trie

### `rust/src/bloom_filter.rs`

- `BloomFilter`: Usa `Vec<bool>` e hash duplo
- `add()`: Marca bits
- `contains()`: Verifica bits
- `suggest()`: Retorna vazio (não suportado)

### `src/generate_test_data.py`

- `generate_usernames()`: Cria nomes aleatórios
- `generate_test_file()`: Cria arquivo com operações
  - Configurável: total de ops, proporção leitura/escrita, seed

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

### Resultado

```json
{
  "test_id": "test_100k",
  "total_operations": 100000,
  "results": {
    "hashset": {
      "structure": "hashset",
      "hits": 50000,
      "misses": 50000,
      "total_time_ms": 1234.56,
      "final_memory_mb": 45.2,
      "memory_evolution": [...]
    },
    ...
  }
}
```

## Características Técnicas

### Medição de Memória

- **Método**: `GlobalAlloc` em Rust
- **Precisão**: Byte-level
- **Overhead**: Mínimo (apenas contadores atômicos)
- **Não inclui**: Stack memory, overhead do SO

### Medição de Tempo

- **Método**: `std::time::Instant`
- **Precisão**: Nanosegundos
- **Conversão**: Para milissegundos no JSON

### Estruturas Built-in

- **HashSet**: `std::collections::HashSet<String>`
- **Trie**: `std::collections::BTreeMap<char, Box<TrieNode>>`
- **Bloom Filter**: `Vec<bool>` (simples e eficiente)

## Performance

### Compilação

- Release mode: ~0.7s
- Sem warnings (após limpeza)

### Execução (100k operações)

- HashSet: ~30ms
- Trie: ~30ms
- Bloom Filter: ~20ms

### Memória (100k operações)

- HashSet: ~0.5MB
- Trie: ~0.5MB
- Bloom Filter: ~10MB (tamanho fixo)

## Notas de Implementação

1. **Simplicidade**: Código simples e direto, sem abstrações desnecessárias
2. **Built-in**: Todas as estruturas usam STL do Rust
3. **Sem GC**: Rust não tem garbage collector, memória é determinística
4. **Reprodutibilidade**: Seed fixo em gerador de dados
5. **Flexibilidade**: Intervalo de medição configurável
6. **Rastreabilidade**: Cada teste gera JSON com ID único

## Verificação

Todos os componentes foram testados:

- Compilação sem erros
- Execução com dados pequenos
- Execução com dados grandes (100k+)
- Saída JSON válida
- Medição de memória funciona
- Output verbose correto
- Diferentes intervalos de medição

## Próximas Melhorias (Opcional)

- Suporte a múltiplos threads
- Comparação automática de resultados
- Gráficos de evolução de memória
- Benchmark de operações específicas
- Cache de resultados
