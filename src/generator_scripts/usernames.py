import random
import string

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
