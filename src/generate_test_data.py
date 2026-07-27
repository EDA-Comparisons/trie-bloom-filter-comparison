import random
import string
import sys

from src.settings import TXT_DIR


def generate_usernames(count, seed=0, prefix=""):
    """Gera nomes de usuário aleatórios, podendo ter um prefixo inicial ou não"""
    random.seed(seed)
    usernames = set()
    while len(usernames) < count:
        username = "".join(
            random.choices(string.ascii_lowercase, k=random.randint(3, 10))
        )
        username = prefix + username
        usernames.add(username)
    return list(usernames)



# TODO (@pagmaia): Alterar lógica de geração de arquivos de teste
# TODO (@pagmaia): Adicionar checagem de resultado para cada teste através de "--verbose"
def generate_test_file(output_file, total_ops, read_ratio=0.5, seed=0, prefix=""):
    """
    Gera arquivo de teste com operações aleatórias

    Args:
        output_file: Caminho do arquivo de saída
        total_ops: Número total de operações
        read_ratio: Proporção de leituras (0.0-1.0)
        seed: Seed para reprodutibilidade
        prefix: Prefixo para todos os usernames
    """
    random.seed(seed)

    usernames = generate_usernames(int(total_ops * 0.1), seed=seed, prefix=prefix)

    with open(TXT_DIR / output_file, "w") as f:
        for i in range(total_ops):
            if random.random() < read_ratio:
                op = random.choice(["GET", "SUG"])
                username = random.choice(usernames)
            else:
                op = "SET"
                username = random.choice(usernames)

            f.write(f"{op} {username}\n")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(
            "Usage: python generate_test_data.py <output_file> <total_operations> [read_ratio] [seed] [prefix]"
        )
        print("Example: python generate_test_data.py test_data.txt 1000000 0.5 42 test")
        sys.exit(1)

    output_file = sys.argv[1]
    total_ops = int(sys.argv[2])
    read_ratio = float(sys.argv[3]) if len(sys.argv) > 3 else 0.5
    seed = int(sys.argv[4]) if len(sys.argv) > 4 else 42
    prefix = sys.argv[5] if len(sys.argv) > 5 else ""

    print(f"Gerando {total_ops} operações com {read_ratio * 100:.0f}% leituras...")
    generate_test_file(output_file, total_ops, read_ratio, seed, prefix)
    print(f"Arquivo '{output_file}' gerado com sucesso!")
