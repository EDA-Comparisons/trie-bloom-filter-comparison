"""
Definições declarativas de todos os testes de carga.

Cada teste chama build_operations() do core com uma configuração específica.
Os comentários explicam o objetivo do teste e as estruturas relevantes.

Escala: 1.000.000 operações por teste (configurável via TOTAL_OPS).
"""
import sys
from src.generate_tests import build_operations, write_test_file, generate_usernames


def format_ops(total_ops):
    if total_ops < 1000:
        return str(int(total_ops))
    elif total_ops < 1000000:
        return str(int(total_ops / 1000)) + "k"
    
    return str(int(total_ops / 1000000)) + "m"
    
def create_tests(TOTAL_OPS=1000000, seed=42):
    pool = generate_usernames(TOTAL_OPS, seed=seed)
    # ---------------------------------------------------------------------------
    # Edge cases / Cenários extremos
    # ---------------------------------------------------------------------------

    # Teste 1: Apenas GETs em usuários inexistentes
    # Objetivo: Medir performance de busca negativa e taxa de falsos positivos
    # do Bloom Filter. Trie e HashSet devem ter 0% falsos positivos.
    # Estruturas relevantes: bloom_filter (falsos positivos), trie, hashset
    TEST_01 = (f"test_01_only_gets_nonexistent_{format_ops(TOTAL_OPS)}", build_operations({
        "total_ops": TOTAL_OPS,
        "ops": ["GET"],
        "ratios": [1.0],
        "seed": seed,
        "nonexistent": True,
        "username_pool_size": TOTAL_OPS,
    }, pool))

    # Teste 2: Apenas GETs em usuários existentes
    # Objetivo: Pre-popula com 500K usuários, depois faz apenas GETs neles.
    # Medir performance de busca positiva. Todas as estruturas devem ter 100% hits.
    # Estruturas relevantes: bloom_filter, trie, hashset
    TEST_02 = (f"test_02_only_gets_existing_{format_ops(TOTAL_OPS)}", build_operations({
        "total_ops": TOTAL_OPS,
        "ops": ["GET"],
        "ratios": [1.0],
        "seed": seed,
        "pre_populate": 500_000,
        "username_pool_size": 500_000,
    }, pool))

    # Teste 3: SET do mesmo username repetido TOTAL_OPS vezes
    # Objetivo: Medir overhead de inserção duplicada. Bloom Filter e HashSet
    # devem rejeitar duplicatas rapidamente. Trie também.
    # Estruturas relevantes: bloom_filter, trie, hashset
    TEST_03 = (f"test_03_repeated_set_same_{format_ops(TOTAL_OPS)}", build_operations({
        "total_ops": TOTAL_OPS,
        "ops": ["SET"],
        "ratios": [1.0],
        "seed": seed,
        "unique_usernames": False,
        "username_pool_size": 1,
    }, pool))

    # Teste 4: Adiciona 1 usuário, faz TOTAL_OPS GETs nele
    # Objetivo: Medir custo de lookup repetido do mesmo elemento.
    # Bloom Filter deve responder rapidamente. Trie e HashSet também.
    # Estruturas relevantes: bloom_filter, trie, hashset
    TEST_04 = (f"test_04_set_one_get_many_{format_ops(TOTAL_OPS)}", build_operations({
        "total_ops": TOTAL_OPS,
        "ops": ["SET", "GET"],
        "ratios": [0.000001, 0.999999],
        "seed": seed,
        "unique_usernames": False,
        "username_pool_size": 1,
        "pre_populate": 1,
    }, pool))


    # ---------------------------------------------------------------------------
    # Razões read/write (do CENARY.md)
    # ---------------------------------------------------------------------------

    # Teste 5: 10% read, 90% write
    # Objetivo: Cenário com predominância de escrita. Medir throughput de SET.
    # Estruturas relevantes: bloom_filter, trie, hashset
    TEST_05 = (f"test_05_10r_90w_{format_ops(TOTAL_OPS)}", build_operations({
        "total_ops": TOTAL_OPS,
        "ops": ["GET", "SET"],
        "ratios": [0.1, 0.9],
        "seed": seed,
        "username_pool_size": TOTAL_OPS,
    }, pool))

    # Teste 6: 20% read, 80% write
    # Objetivo: Cenário com alta proporção de escrita.
    # Estruturas relevantes: bloom_filter, trie, hashset
    TEST_06 = (f"test_06_20r_80w_{format_ops(TOTAL_OPS)}", build_operations({
        "total_ops": TOTAL_OPS,
        "ops": ["GET", "SET"],
        "ratios": [0.2, 0.8],
        "seed": seed,
        "username_pool_size": TOTAL_OPS,
    }, pool))

    # Teste 7: 30% read, 70% write
    # Objetivo: Cenário com maioria de escrita.
    # Estruturas relevantes: bloom_filter, trie, hashset
    TEST_07 = (f"test_07_30r_70w_{format_ops(TOTAL_OPS)}", build_operations({
        "total_ops": TOTAL_OPS,
        "ops": ["GET", "SET"],
        "ratios": [0.3, 0.7],
        "seed": seed,
        "username_pool_size": TOTAL_OPS,
    }, pool))

    # Teste 8: 40% read, 60% write
    # Objetivo: Cenário com leve maioria de escrita.
    # Estruturas relevantes: bloom_filter, trie, hashset
    TEST_08 = (f"test_08_40r_60w_{format_ops(TOTAL_OPS)}", build_operations({
        "total_ops": TOTAL_OPS,
        "ops": ["GET", "SET"],
        "ratios": [0.4, 0.6],
        "seed": seed,
        "username_pool_size": TOTAL_OPS,
    }, pool))

    # Teste 9: 50% read, 50% write
    # Objetivo: Cenário perfeitamente balanceado entre leitura e escrita.
    # Estruturas relevantes: bloom_filter, trie, hashset
    TEST_09 = (f"test_09_50r_50w_{format_ops(TOTAL_OPS)}", build_operations({
        "total_ops": TOTAL_OPS,
        "ops": ["GET", "SET"],
        "ratios": [0.5, 0.5],
        "seed": seed,
        "username_pool_size": TOTAL_OPS,
    }, pool))

    # Teste 10: 60% read, 40% write
    # Objetivo: Cenário com leve maioria de leitura.
    # Estruturas relevantes: bloom_filter, trie, hashset
    TEST_10 = (f"test_10_60r_40w_{format_ops(TOTAL_OPS)}", build_operations({
        "total_ops": TOTAL_OPS,
        "ops": ["GET", "SET"],
        "ratios": [0.6, 0.4],
        "seed": seed,
        "username_pool_size": TOTAL_OPS,
    }, pool))

    # Teste 11: 70% read, 30% write
    # Objetivo: Cenário com maioria de leitura.
    # Estruturas relevantes: bloom_filter, trie, hashset
    TEST_11 = (f"test_11_70r_30w_{format_ops(TOTAL_OPS)}", build_operations({
        "total_ops": TOTAL_OPS,
        "ops": ["GET", "SET"],
        "ratios": [0.7, 0.3],
        "seed": seed,
        "username_pool_size": TOTAL_OPS,
    }, pool))

    # Teste 12: 80% read, 20% write
    # Objetivo: Cenário com alta proporção de leitura.
    # Estruturas relevantes: bloom_filter, trie, hashset
    TEST_12 = (f"test_12_80r_20w_{format_ops(TOTAL_OPS)}", build_operations({
        "total_ops": TOTAL_OPS,
        "ops": ["GET", "SET"],
        "ratios": [0.8, 0.2],
        "seed": seed,
        "username_pool_size": TOTAL_OPS,
    }, pool))

    # Teste 13: 90% read, 10% write
    # Objetivo: Cenário com predominância de leitura. Medir throughput de GET.
    # Estruturas relevantes: bloom_filter, trie, hashset
    TEST_13 = (f"test_13_90r_10w_{format_ops(TOTAL_OPS)}", build_operations({
        "total_ops": TOTAL_OPS,
        "ops": ["GET", "SET"],
        "ratios": [0.9, 0.1],
        "seed": seed,
        "username_pool_size": TOTAL_OPS,
    }, pool))

    # ---------------------------------------------------------------------------
    # Operações mistas com SUG e NEW
    # ---------------------------------------------------------------------------

    # Teste 14: Homogêneo — 25% SET, 25% GET, 25% SUG, 25% NEW
    # Objetivo: Mistura homogênea de todas as operações. SUG não faz sentido
    # em Bloom Filter (retorna string vazia). NEW verifica disponibilidade de nome.
    # Estruturas relevantes: bloom_filter (SUG vazio), trie (SUG eficiente), hashset
    TEST_14 = (f"test_14_homogeneous_{format_ops(TOTAL_OPS)}", build_operations({
        "total_ops": TOTAL_OPS,
        "ops": ["SET", "GET", "SUG", "NEW"],
        "ratios": [0.25, 0.25, 0.25, 0.25],
        "seed": seed,
        "username_pool_size": TOTAL_OPS,
    }, pool))

    # ---------------------------------------------------------------------------
    # Variações de ordem
    # ---------------------------------------------------------------------------

    # Teste 15: 50% SET + 50% GET em ordem alfabética (sorted)
    # Objetivo: Medir impacto de localidade/cache quando operações seguem ordem
    # lexicográfica. Pode beneficiar Trie (traversal ordenado) vs HashSet.
    # Estruturas relevantes: bloom_filter, trie, hashset
    TEST_15 = (f"test_15_sorted_order_{format_ops(TOTAL_OPS)}", build_operations({
        "total_ops": TOTAL_OPS,
        "ops": ["SET", "GET"],
        "ratios": [0.5, 0.5],
        "seed": seed,
        "order": "sorted",
        "username_pool_size": TOTAL_OPS,
    }, pool))

    # Teste 16: Operações agrupadas por prefixo comum do username (clustered)
    # Objetivo: Medir impacto de agrupamento por prefixo. Trie pode se beneficiar
    # por acessar os mesmos nós repetidamente. HashSet e Bloom Filter menos afetados.
    # Estruturas relevantes: bloom_filter, trie, hashset
    TEST_16 = (f"test_16_clustered_order_{format_ops(TOTAL_OPS)}", build_operations({
        "total_ops": TOTAL_OPS,
        "ops": ["SET", "GET"],
        "ratios": [0.5, 0.5],
        "seed": seed,
        "order": "clustered",
        "username_pool_size": TOTAL_OPS,
    }, pool))

    # Teste 17: SET em diferentes
    # Objetivo: Medir impacto de agrupamento por prefixo. Trie pode se beneficiar
    # por acessar os mesmos nós repetidamente. HashSet e Bloom Filter menos afetados.
    # Estruturas relevantes: bloom_filter, trie, hashset
    TEST_17 = (f"test_17_onlyset_{format_ops(TOTAL_OPS)}", build_operations({
        "total_ops": TOTAL_OPS,
        "ops": ["SET"],
        "ratios": [1.0],
        "seed": seed,
        "username_pool_size": TOTAL_OPS,
    }, pool))

    # ---------------------------------------------------------------------------
    # Lista de todos os testes
    # ---------------------------------------------------------------------------

    ALL_TESTS = [
        TEST_01, TEST_02, TEST_03, TEST_04, TEST_05,
        TEST_06, TEST_07, TEST_08, TEST_09, TEST_10,
        TEST_11, TEST_12, TEST_13,
        TEST_15, TEST_16, TEST_17
    ]
    return ALL_TESTS


def generate_all_tests(total_ops, seed):
    """Gera todos os arquivos de teste definidos em ALL_TESTS."""
    tests = create_tests(total_ops, seed)
    for name, operations in tests:
        filepath = write_test_file(name, operations)
        print(f"  Gerado: {filepath.name} ({len(operations)} operações)")


if __name__ == "__main__":
    if(len(sys.argv)) < 2:
        print("Usage: uv run -m src.run_tests 10000")
        sys.exit(1)
    total_ops = int(sys.argv[1])
    seed = int(sys.argv[2])
    generate_all_tests(total_ops, seed)
