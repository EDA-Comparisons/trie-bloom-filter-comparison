import random
import string

from src.settings import TXT_DIR


def generate_usernames(count, seed=0, prefix=""):
    """Gera nomes de usuário aleatórios únicos, podendo ter um prefixo inicial."""
    random.seed(seed)
    usernames = set()
    while len(usernames) < count:
        username = "".join(
            random.choices(string.ascii_lowercase, k=random.randint(3, 10))
        )
        usernames.add(prefix + username)
    return list(usernames)


def generate_nonexistent_usernames(count, existing, seed=0):
    """Gera usernames garantidamente não presentes em `existing`."""
    random.seed(seed)
    existing_set = set(existing)
    usernames = set()
    while len(usernames) < count:
        username = "".join(
            random.choices(string.ascii_lowercase, k=random.randint(3, 10))
        )
        if username not in existing_set:
            usernames.add(username)
    return list(usernames)


def _order_random(ops, seed=42):
    """Embaralha a lista de operações mantendo reprodutibilidade."""
    random.seed(seed)
    result = list(ops)
    random.shuffle(result)
    return result


def _order_sorted(ops):
    """Ordena operações alfabeticamente pelo username (segundo campo)."""
    return sorted(ops, key=lambda line: line.split(" ", 1)[1] if " " in line else line)


def _order_clustered(ops, prefix_len=2):
    """Agrupa operações por prefixo comum do username para testar localidade de cache."""
    groups = {}
    for line in ops:
        parts = line.split(" ", 1)
        key = (
            parts[1][:prefix_len]
            if len(parts) > 1 and len(parts[1]) >= prefix_len
            else "zz"
        )
        groups.setdefault(key, []).append(line)
    result = []
    for key in sorted(groups):
        result.extend(groups[key])
    return result


def build_operations(config):
    """
    Função central do core: recebe um dict de configuração e retorna lista de strings "OP username".

    Parâmetros do config:
        total_ops (int): Número total de operações a gerar.
        ops (list[str]): Operações permitidas, ex: ["SET", "GET"].
        ratios (list[float]): Proporção de cada operação em `ops`. Deve somar ~1.0.
        seed (int): Seed para reprodutibilidade.
        prefix (str): Prefixo para todos os usernames.
        order (str): "random" | "sorted" | "clustered".
        unique_usernames (bool): Se True, cada SET usa username único. Se False, reutiliza.
        pre_populate (int): Número de SETs iniciais antes de contar as operações.
        username_pool_size (int): Tamanho do pool de usernames.
        nonexistent (bool): Se True, gera usernames que não estarão na estrutura (para GETs negativos).
    """
    total_ops = config.get("total_ops", 1_000_000)
    ops_list = config["ops"]
    ratios = config.get("ratios", [1.0 / len(ops_list)] * len(ops_list))
    seed = config.get("seed", 42)
    prefix = config.get("prefix", "")
    order = config.get("order", "random")
    unique_usernames = config.get("unique_usernames", True)
    pre_populate = config.get("pre_populate", 0)
    pool_size = config.get("username_pool_size", max(total_ops, 100_000))
    nonexistent = config.get("nonexistent", False)

    random.seed(seed)

    pool = generate_usernames(pool_size, seed=seed, prefix=prefix)

    if nonexistent:
        nonexistent_pool = generate_nonexistent_usernames(
            pool_size, pool, seed=seed + 1
        )
        pool = nonexistent_pool

    pre_populate_usernames = []
    if pre_populate > 0:
        pre_pool = generate_usernames(pre_populate, seed=seed, prefix=prefix)
        pre_populate_usernames = [f"SET {u}" for u in pre_pool]

    operations = []
    set_idx = 0
    for i in range(total_ops):
        r = random.random()
        cumulative = 0.0
        chosen_op = ops_list[-1]
        for op, ratio in zip(ops_list, ratios):
            cumulative += ratio
            if r < cumulative:
                chosen_op = op
                break

        if chosen_op == "SET":
            if unique_usernames and set_idx < len(pool):
                username = pool[set_idx % len(pool)]
                set_idx += 1
            else:
                username = random.choice(pool)
        else:
            username = random.choice(pool)

        operations.append(f"{chosen_op} {username}")

    measured_ops = operations

    if order == "sorted":
        measured_ops = _order_sorted(measured_ops)
    elif order == "clustered":
        measured_ops = _order_clustered(measured_ops)
    else:
        measured_ops = _order_random(measured_ops, seed=seed)

    return pre_populate_usernames + measured_ops


def write_test_file(filename, operations):
    """Escreve lista de operações em data/tests/txt/{filename}.txt."""
    filepath = TXT_DIR / f"{filename}.txt"
    with open(filepath, "w") as f:
        f.writelines(line + "\n" for line in operations)
    return filepath
