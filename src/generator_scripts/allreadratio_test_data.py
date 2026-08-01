import random
import sys

from src.generator_scripts.utils import generate_usernames, load_str
from ..settings import TXT_DIR

def generate_benchmark_data(load, seed):
    """
    Gera os arquivos de teste para o experimento variando os tipos das operações

    Args:
        load: Número total de operações
        seed: Seed para reprodutibilidade
    """

    usernames = generate_usernames(int(load * 0.1), seed)

    for ratio in range(1, 10):
        read_ratio = ratio * 10
        set_ratio = 100 - read_ratio
        output_file = "benchmark_" + str(read_ratio) + str(set_ratio) + "_" + load_str(load) + ".txt"

        with open(TXT_DIR / output_file, "w") as f:
            for i in range(load):
                if random.random() < (read_ratio / 100) :
                    op = "GET"
                    username = random.choice(usernames)
                else:
                    op = "SET"
                    username = random.choice(usernames)

                f.write(f"{op} {username}\n")

        print(f"Arquivo gerado com {read_ratio}% leituras e {set_ratio}% de adições e sugestoes")

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print(
            "Usage: python allreadratio_test_data <load> <seed>"
        )
        print("Example: python allreadratio_test_data 1000000 42")
        sys.exit(1)

    load = int(sys.argv[1])
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 42

    print(f"Gerando arquivos para realização de benchmark de tipos de operações")
    generate_benchmark_data(load, seed)
    print(f"Arquivos gerados com sucesso!")