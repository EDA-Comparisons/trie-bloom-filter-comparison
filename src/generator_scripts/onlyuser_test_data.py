import random
import string
import sys

from ..settings import TXT_DIR

def generate_onlyuser_queries(username, output_file, total_ops, seed=0):
    random.seed(seed)
    with open(TXT_DIR / output_file, "w") as f:
            f.write(f"SET {username}\n")
            for i in range(total_ops):
                op = "GET"
                f.write(f"{op} {username}\n")

def generate_onlyuser_set(username, output_file, total_ops, seed=0):
    random.seed(seed)

    with open(TXT_DIR / output_file, "w") as f:
            for i in range(total_ops):
                op = "SET"
                f.write(f"{op} {username}\n")    

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print(
            "Usage: python onlyuser_test_data.py <type> <output_file> <total_operations> <seed>"
        )
        print("Example: python onlyuser_test_data.py 1 test_data.txt 1000000 42")
        sys.exit(1)

    type = sys.argv[1]
    output_file = sys.argv[2]
    total_ops = int(sys.argv[3])
    seed = int(sys.argv[4]) if len(sys.argv) > 4 else 42

    username = "".join(
            random.choices(string.ascii_lowercase, k=random.randint(3, 10))
        )

    if type == "1":
        print(f"Gerando {total_ops} operações para realização de benchmark com queries em apenas um user")
        generate_onlyuser_queries(username, output_file, total_ops, seed)
    elif type == "2":
        print(f"Gerando {total_ops} operações para realização de benchmark com apenas adições")
        generate_onlyuser_set(username, output_file, total_ops, seed)

    print(f"Arquivo '{output_file}' gerado com sucesso!")