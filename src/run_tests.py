"""
Definições declarativas de todos os testes de carga.

Cada teste chama build_operations() do core com uma configuração específica.
Os comentários explicam o objetivo do teste e as estruturas relevantes.

Escala: 1.000.000 operações por teste (configurável via TOTAL_OPS).
"""

from src.generate_tests import build_operations, write_test_file

TOTAL_OPS = 1_000_000

# ---------------------------------------------------------------------------
# Edge cases / Cenários extremos
# ---------------------------------------------------------------------------

# Teste 1: Apenas GETs em usuários inexistentes
# Objetivo: Medir performance de busca negativa e taxa de falsos positivos
# do Bloom Filter. Trie e HashSet devem ter 0% falsos positivos.
# Estruturas relevantes: bloom_filter (falsos positivos), trie, hashset
TEST_01 = ("test_01_only_gets_nonexistent", build_operations({
    "total_ops": TOTAL_OPS,
    "ops": ["GET"],
    "ratios": [1.0],
    "seed": 42,
    "nonexistent": True,
    "username_pool_size": TOTAL_OPS,
}))

# Teste 2: Apenas GETs em usuários existentes
# Objetivo: Pre-popula com 500K usuários, depois faz apenas GETs neles.
# Medir performance de busca positiva. Todas as estruturas devem ter 100% hits.
# Estruturas relevantes: bloom_filter, trie, hashset
TEST_02 = ("test_02_only_gets_existing", build_operations({
    "total_ops": TOTAL_OPS,
    "ops": ["GET"],
    "ratios": [1.0],
    "seed": 42,
    "pre_populate": 500_000,
    "username_pool_size": 500_000,
}))

# Teste 3: SET do mesmo username repetido 1M vezes
# Objetivo: Medir overhead de inserção duplicada. Bloom Filter e HashSet
# devem rejeitar duplicatas rapidamente. Trie também.
# Estruturas relevantes: bloom_filter, trie, hashset
TEST_03 = ("test_03_repeated_set_same", build_operations({
    "total_ops": TOTAL_OPS,
    "ops": ["SET"],
    "ratios": [1.0],
    "seed": 42,
    "unique_usernames": False,
    "username_pool_size": 1,
}))

# Teste 4: Adiciona 1 usuário, faz 999.999 GETs nele
# Objetivo: Medir custo de lookup repetido do mesmo elemento.
# Bloom Filter deve responder rapidamente. Trie e HashSet também.
# Estruturas relevantes: bloom_filter, trie, hashset
TEST_04 = ("test_04_set_one_get_many", build_operations({
    "total_ops": TOTAL_OPS,
    "ops": ["SET", "GET"],
    "ratios": [0.000001, 0.999999],
    "seed": 42,
    "unique_usernames": False,
    "username_pool_size": 1,
    "pre_populate": 1,
}))

# Teste 5: 500K SETs + 500K GETs intercalados (balanceado realista)
# Objetivo: Cenário balanceado realista com inserções e buscas misturadas.
# Medir performance em carga mista típica.
# Estruturas relevantes: bloom_filter, trie, hashset
TEST_05 = ("test_05_half_set_half_get", build_operations({
    "total_ops": TOTAL_OPS,
    "ops": ["SET", "GET"],
    "ratios": [0.5, 0.5],
    "seed": 42,
    "username_pool_size": 500_000,
}))

# ---------------------------------------------------------------------------
# Razões read/write (do CENARY.md)
# ---------------------------------------------------------------------------

# Teste 6: 10% read, 90% write
# Objetivo: Cenário com predominância de escrita. Medir throughput de SET.
# Estruturas relevantes: bloom_filter, trie, hashset
TEST_06 = ("test_06_10r_90w", build_operations({
    "total_ops": TOTAL_OPS,
    "ops": ["GET", "SET"],
    "ratios": [0.1, 0.9],
    "seed": 42,
    "username_pool_size": TOTAL_OPS,
}))

# Teste 7: 20% read, 80% write
# Objetivo: Cenário com alta proporção de escrita.
# Estruturas relevantes: bloom_filter, trie, hashset
TEST_07 = ("test_07_20r_80w", build_operations({
    "total_ops": TOTAL_OPS,
    "ops": ["GET", "SET"],
    "ratios": [0.2, 0.8],
    "seed": 42,
    "username_pool_size": TOTAL_OPS,
}))

# Teste 8: 30% read, 70% write
# Objetivo: Cenário com maioria de escrita.
# Estruturas relevantes: bloom_filter, trie, hashset
TEST_08 = ("test_08_30r_70w", build_operations({
    "total_ops": TOTAL_OPS,
    "ops": ["GET", "SET"],
    "ratios": [0.3, 0.7],
    "seed": 42,
    "username_pool_size": TOTAL_OPS,
}))

# Teste 9: 40% read, 60% write
# Objetivo: Cenário com leve maioria de escrita.
# Estruturas relevantes: bloom_filter, trie, hashset
TEST_09 = ("test_09_40r_60w", build_operations({
    "total_ops": TOTAL_OPS,
    "ops": ["GET", "SET"],
    "ratios": [0.4, 0.6],
    "seed": 42,
    "username_pool_size": TOTAL_OPS,
}))

# Teste 10: 50% read, 50% write
# Objetivo: Cenário perfeitamente balanceado entre leitura e escrita.
# Estruturas relevantes: bloom_filter, trie, hashset
TEST_10 = ("test_10_50r_50w", build_operations({
    "total_ops": TOTAL_OPS,
    "ops": ["GET", "SET"],
    "ratios": [0.5, 0.5],
    "seed": 42,
    "username_pool_size": TOTAL_OPS,
}))

# Teste 11: 60% read, 40% write
# Objetivo: Cenário com leve maioria de leitura.
# Estruturas relevantes: bloom_filter, trie, hashset
TEST_11 = ("test_11_60r_40w", build_operations({
    "total_ops": TOTAL_OPS,
    "ops": ["GET", "SET"],
    "ratios": [0.6, 0.4],
    "seed": 42,
    "username_pool_size": TOTAL_OPS,
}))

# Teste 12: 70% read, 30% write
# Objetivo: Cenário com maioria de leitura.
# Estruturas relevantes: bloom_filter, trie, hashset
TEST_12 = ("test_12_70r_30w", build_operations({
    "total_ops": TOTAL_OPS,
    "ops": ["GET", "SET"],
    "ratios": [0.7, 0.3],
    "seed": 42,
    "username_pool_size": TOTAL_OPS,
}))

# Teste 13: 80% read, 20% write
# Objetivo: Cenário com alta proporção de leitura.
# Estruturas relevantes: bloom_filter, trie, hashset
TEST_13 = ("test_13_80r_20w", build_operations({
    "total_ops": TOTAL_OPS,
    "ops": ["GET", "SET"],
    "ratios": [0.8, 0.2],
    "seed": 42,
    "username_pool_size": TOTAL_OPS,
}))

# Teste 14: 90% read, 10% write
# Objetivo: Cenário com predominância de leitura. Medir throughput de GET.
# Estruturas relevantes: bloom_filter, trie, hashset
TEST_14 = ("test_14_90r_10w", build_operations({
    "total_ops": TOTAL_OPS,
    "ops": ["GET", "SET"],
    "ratios": [0.9, 0.1],
    "seed": 42,
    "username_pool_size": TOTAL_OPS,
}))

# ---------------------------------------------------------------------------
# Operações mistas com SUG e NEW
# ---------------------------------------------------------------------------

# Teste 15: Homogêneo — 25% SET, 25% GET, 25% SUG, 25% NEW
# Objetivo: Mistura homogênea de todas as operações. SUG não faz sentido
# em Bloom Filter (retorna string vazia). NEW verifica disponibilidade de nome.
# Estruturas relevantes: bloom_filter (SUG vazio), trie (SUG eficiente), hashset
TEST_15 = ("test_15_homogeneous", build_operations({
    "total_ops": TOTAL_OPS,
    "ops": ["SET", "GET", "SUG", "NEW"],
    "ratios": [0.25, 0.25, 0.25, 0.25],
    "seed": 42,
    "username_pool_size": TOTAL_OPS,
}))

# ---------------------------------------------------------------------------
# Variações de ordem
# ---------------------------------------------------------------------------

# Teste 16: 50% SET + 50% GET em ordem alfabética (sorted)
# Objetivo: Medir impacto de localidade/cache quando operações seguem ordem
# lexicográfica. Pode beneficiar Trie (traversal ordenado) vs HashSet.
# Estruturas relevantes: bloom_filter, trie, hashset
TEST_16 = ("test_16_sorted_order", build_operations({
    "total_ops": TOTAL_OPS,
    "ops": ["SET", "GET"],
    "ratios": [0.5, 0.5],
    "seed": 42,
    "order": "sorted",
    "username_pool_size": TOTAL_OPS,
}))

# Teste 17: Operações agrupadas por prefixo comum (clustered)
# Objetivo: Medir impacto de agrupamento por prefixo. Trie pode se beneficiar
# por acessar os mesmos nós repetidamente. HashSet e Bloom Filter menos afetados.
# Estruturas relevantes: bloom_filter, trie, hashset
TEST_17 = ("test_17_clustered_order", build_operations({
    "total_ops": TOTAL_OPS,
    "ops": ["SET", "GET"],
    "ratios": [0.5, 0.5],
    "seed": 42,
    "order": "clustered",
    "username_pool_size": TOTAL_OPS,
}))

# ---------------------------------------------------------------------------
# Lista de todos os testes
# ---------------------------------------------------------------------------

ALL_TESTS = [
    TEST_01, TEST_02, TEST_03, TEST_04, TEST_05,
    TEST_06, TEST_07, TEST_08, TEST_09, TEST_10,
    TEST_11, TEST_12, TEST_13, TEST_14, TEST_15,
    TEST_16, TEST_17,
]


def generate_all_tests():
    """Gera todos os arquivos de teste definidos em ALL_TESTS."""
    for name, operations in ALL_TESTS:
        filepath = write_test_file(name, operations)
        print(f"  Gerado: {filepath.name} ({len(operations)} operações)")


if __name__ == "__main__":
    generate_all_tests()
