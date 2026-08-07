# Cenário

Você tem um sistema que precisa cadastrar um usuário. Para isso você precisa garantir que cada nome de usuário seja único. Portanto no momento em que o usuário submeter um cadastro é necessário verificar a unicidade desse registro.

Porém há mais de 100 mil requisições/s, o que faz com que abordagens tradicionais como "Unique" em SQL sejam obsoletas. Além de dever poder lidar com arquitetura distribuída.

## Nosso objetivo

- Nosso objetivo é criar uma estrutura de dados que seja capaz de lidar com esse cenário de forma eficiente.

## Problemas encarados

### Bloom Filter:

- Falsos positivos
- Não permite remoção de elementos
- Não facilmente expansível
- Não dinâmico

- Economia de memória
- Performance
- Hash é distribuível (Testar)
- Paralelização (Testar)

### Trie

- Alto consumo de meória
- Difícil de parelelizar

- Sugestões de nomes

### HashSet

- Alto consumo de memória
- Difícil de parelelizar

## Plano de Execução

### Operações

- GET "Nome do usuário" -> Existe ou Não Existe
- ADD "Nome do usuário" -> Adiciona usuário
- SUG "Nome do usuário" -> Nome existente com o prefixo "Nome do usuário"
- NEW "Nome do usuário" -> Nome lexicograficamente disponível mais próximo

## Testes

TOTAL_OPS = Quantidade de operações escolhida, para esse experimento, foram escolhidas as cargas 10 mil, 100 mil, 500 mil e 1 milhão.

### Teste 1

- TOTAL_OPS operações GET em usuários que não existem

Objetivo: Medir performance de busca negativa e taxa de falsos positivos do Bloom Filter. Trie e HashSet devem ter 0% falsos positivos.

Estruturas relevantes: bloom_filter (falsos positivos), trie, hashset

### Teste 2

- Adicionar 500 mil usuários
- TOTAL_OPS operações GET em usuários que existem

Objetivo: Medir performance de busca positiva. Todas as estruturas devem ter 100% hits.

Estruturas relevantes: bloom_filter, trie, hashset

### Teste 3

- Adicionar o mesmo usuário (SET) para TOTAL_OPS operações

Objetivo: Medir overhead de inserção duplicada. Bloom Filter e HashSet , devem rejeitar duplicatas rapidamente. Trie também.

Estruturas relevantes: bloom_filter, trie, hashset

### Teste 4

- Adicionar um usuário (SET) e GET para TOTAL_OPS operações

Objetivo: Medir custo de lookup repetido do mesmo elemento. Bloom Filter deve responder rapidamente. Trie e HashSet também.

Estruturas relevantes: bloom_filter, trie, hashset


### Teste 5

- 10% read (GET) 90% write (SET) para TOTAL_OPS operações [Ordem Aleatória] 

Objetivo: Cenário com predominância de escrita. Medir throughput de SET.

Estruturas relevantes: bloom_filter, trie, hashset

### Teste 6

- 20% read (GET) 80% write (SET) para TOTAL_OPS operações [Ordem Aleatória] 

Objetivo: Cenário com alta proporção de escrita.

Estruturas relevantes: bloom_filter, trie, hashset


### Teste 7

- 30% read (GET) 70% write (SET) para TOTAL_OPS operações [Ordem Aleatória] 

Objetivo: Cenário com maioria de escrita.

Estruturas relevantes: bloom_filter, trie, hashset

### Teste 8

- 40% read (GET) 60% write (SET) para TOTAL_OPS operações [Ordem Aleatória] 

Objetivo: Cenário com leve maioria de escrita.

Estruturas relevantes: bloom_filter, trie, hashset


### Teste 9

- 50% read (GET) 50% write (SET) para TOTAL_OPS operações [Ordem Aleatória] 

Objetivo: Cenário perfeitamente balanceado entre leitura e escrita.

Estruturas relevantes: bloom_filter, trie, hashset


### Teste 10

- 60% read (GET) 40% write (SET) para TOTAL_OPS operações [Ordem Aleatória] 

Objetivo: Cenário com leve maioria de leitura.

Estruturas relevantes: bloom_filter, trie, hashset

### Teste 11

- 70% read (GET) 30% write (SET) para TOTAL_OPS operações [Ordem Aleatória] 

Objetivo: Cenário com maioria de leitura.

Estruturas relevantes: bloom_filter, trie, hashset

### Teste 12

- 80% read (GET) 20% write (SET) para TOTAL_OPS operações [Ordem Aleatória] 

Objetivo: Cenário com alta proporção de leitura.

Estruturas relevantes: bloom_filter, trie, hashset

### Teste 13

- 90% read (GET) 10% write (SET) para TOTAL_OPS operações [Ordem Aleatória] 

Objetivo: Cenário com predominância de leitura. Medir throughput de GET.

Estruturas relevantes: bloom_filter, trie, hashset

### Teste 14

- 25% GET, 25% SET, 25% SUG, 25% NEW para TOTAL_OPS operações [Ordem Aleatória] 

Objetivo: Mistura homogênea de todas as operações. SUG não faz sentido em Bloom Filter (retorna string vazia). NEW verifica disponibilidade de nome.

Estruturas relevantes: bloom_filter (SUG vazio), trie (SUG eficiente), hashset

### Teste 15

- 50% GET, 50% SET para TOTAL_OPS operações [Nomes ordenados alfabeticamente] 

Objetivo: Medir impacto de localidade/cache quando operações seguem ordem lexicográfica. Pode beneficiar Trie (traversal ordenado) vs HashSet.

Estruturas relevantes: bloom_filter, trie, hashset

### Teste 16

- 50% GET, 50% SET para TOTAL_OPS operações [Nomes agrupados por prefixo] 

Objetivo: Medir impacto de agrupamento por prefixo. Trie pode se beneficiar por acessar os mesmos nós repetidamente. HashSet e Bloom Filter menos afetados.

Estruturas relevantes: bloom_filter, trie, hashset

### Teste 17

- 100% SET para TOTAL_OPS operações

Objetivo: Medir impacto geral da adição nas estrturas. HashSet e Bloom filter devem ser rápidos e Trie mais lenta no final.

Estruturas relevantes: bloom_filter, trie, hashset

### Teste Adicional

- 50% SET E 50% GET com nomes que não foram colocados para TOTAL_OPS operações

Objetivo: Medir taxa de falsos positivos do Bloom Filter

Estruturas relevantes: bloom_filter