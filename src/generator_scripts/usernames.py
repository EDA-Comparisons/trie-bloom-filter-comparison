import random
import string

def generate_usernames(count, seed=0):
    """Gera nomes de usuário aleatórios"""
    random.seed(seed)
    usernames = set()
    while len(usernames) < count:
        username = "".join(
            random.choices(string.ascii_lowercase, k=random.randint(3, 10))
        )
        usernames.add(username)
    return list(usernames)
