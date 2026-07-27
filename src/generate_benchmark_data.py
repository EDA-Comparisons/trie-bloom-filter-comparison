import random
import sys

from src.generate_test_data import generate_usernames
from src.settings import TXT_DIR

def generate_benchmark_files(total_ops, seed=0, prefix=""):
    """
    Gera os arquivos de teste para o experimento do projeto.

    Args:
        total_ops: Número total de operações
        seed: Seed para reprodutibilidade
        prefix: Prefixo para todos os usernames
    """

    usernames = generate_usernames(int(total_ops * 0.1), seed=seed, prefix=prefix)

    for ratio in range(1, 10):
        read_radio = ratio * 10
        addsug_ratio = 100 - read_radio
        output_file = "experiment" + str(read_radio) + str(addsug_ratio)  + ".txt"

        with open(TXT_DIR / output_file, "w") as f:
            for i in range(total_ops):
                if random.random() < addsug_ratio :
                    op = random.choice(["GET", "SUG"])
                    username = random.choice(usernames)
                else:
                    op = "SET"
                    username = random.choice(usernames)

                f.write(f"{op} {username}\n")

if __name__ == "__main__":
    if len(sys.argv) == 0:
        print(
            "Usage: python generate_benchmark_data <total_operations> [seed] [prefix]"
        )
        print("Example: python generate_benchmark_data 1000000 42 test")
        sys.exit(1)

    total_ops = int(sys.argv[1])
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else random.randint(0, 100)
    prefix = sys.argv[3] if len(sys.argv) > 5 else ""

    print(f"Gerando 10 arquivos para realização do benchmark")
    generate_benchmark_files(total_ops, seed, prefix)
    print(f"Arquivos gerados com sucesso!")