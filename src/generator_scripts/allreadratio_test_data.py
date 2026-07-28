import random
import sys

from src.generator_scripts.usernames import generate_usernames
from ..settings import TXT_DIR

def generate_benchmark_data(total_ops, seed=0, prefix=""):
    """
    Gera os arquivos de teste para o experimento variando os tipos das operações

    Args:
        total_ops: Número total de operações
        seed: Seed para reprodutibilidade
        prefix: Prefixo para todos os usernames
    """

    usernames = generate_usernames(int(total_ops * 0.1), seed=seed, prefix=prefix)

    for ratio in range(1, 10):
        read_ratio = ratio * 10
        set_ratio = 100 - read_ratio
        output_file = "benchmark_" + str(read_ratio) + str(set_ratio) + "_" + str(total_ops) + ".txt"

        with open(TXT_DIR / output_file, "w") as f:
            for i in range(total_ops):
                if random.random() < (read_ratio / 100) :
                    op = random.choice(["GET", "SUG"])
                    username = random.choice(usernames)
                else:
                    op = "SET"
                    username = random.choice(usernames)

                f.write(f"{op} {username}\n")

        print(f"Arquivo gerado com {read_ratio}% leituras e {set_ratio}% de adições e sugestoes")

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print(
            "Usage: python allreadratio_test_data <total_operations> <seed> <prefix>"
        )
        print("Example: python allreadratio_test_data 1000000 42 test")
        sys.exit(1)

    total_ops = int(sys.argv[1])
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 42
    prefix = sys.argv[3] if len(sys.argv) > 3 else ""

    print(f"Gerando arquivos para realização de benchmark de tipos de operações")
    generate_benchmark_data(total_ops, seed, prefix)
    print(f"Arquivos gerados com sucesso!")