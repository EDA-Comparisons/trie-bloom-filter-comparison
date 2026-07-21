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
- Não dinânimaco

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

- get "Nome do usuário" -> Existe ou Não Existe
- add "Nome do usuário" -> Adiciona usuário
- suggest "Nome do usuário" -> Nome lexicograficamente disponível mais próximo

## Testes

### teste 1

- Query em 10M de usuários que não existem

### teste 2

- Query em 10M de usuário que existem

### teste 3

- Adicionar o mesmo usuário 10M de vezes

### teste 4

- Adicionar um usuário e Query 10M de vezes

### teste 5

- Adicionar 10M de usuários e Query 10M de vezes

### teste 6

- 10% read 90% write (Amostra 10M) [Ordem Aleatória] (100 runs)

### teste 7

- 20% read 80% write (Amostra 10M) [Ordem Aleatória] (100 runs)

### teste 8

- 30% read 70% write (Amostra 10M) [Ordem Aleatória] (100 runs)

### teste 9

- 40% read 60% write (Amostra 10M) [Ordem Aleatória] (100 runs)

### teste 10

- 50% read 50% write (Amostra 10M) [Ordem Aleatória] (100 runs)

### teste 11

- 60% read 40% write (Amostra 10M) [Ordem Aleatória] (100 runs)

### teste 12

- 70% read 30% write (Amostra 10M) [Ordem Aleatória] (100 runs)

### teste 13

- 80% read 20% write (Amostra 10M) [Ordem Aleatória] (100 runs)

### teste 14

- 90% read 10% write (Amostra 10M) [Ordem Aleatória] (100 runs)
