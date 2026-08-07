import random
import subprocess
import asyncio
import sys

from src.run_tests import write_test_file, format_ops
from src.generate_test_data import generate_usernames
from src.settings import RUST_BINARY, JSON_DIR


def create_test_pools(total_ops, seed=42):
    random.seed(seed)
    pool = generate_usernames(total_ops, seed)
    return pool

def pre_populate(pool):
    pre_populate_usernames = [f"SET {u}" for u in pool[:len(pool) // 2]]
    return pre_populate_usernames

def write_ops(pool):
    ops = [f"GET {u}" for u in pool[len(pool) // 2:]]
    return pre_populate(pool) + ops

def write_files(total_ops, seed=42):
    pool = create_test_pools(total_ops, seed)
    test = (f"test_bloom_filter_precision_pool_{format_ops(total_ops)}", write_ops(pool))
    filepath = write_test_file(test[0], test[1])
    print(f"Arquivo de teste gerado! -> {filepath}")

    return filepath

async def run_benchmark(file_path):
    cmd = [str(RUST_BINARY), str(file_path), str(-1), file_path.stem, str(JSON_DIR), "--bloom"]

    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    if stdout:
        print(stdout.decode().strip())
    if stderr:
        print(stderr.decode().strip())

async def run_benchmarks(total_ops, seed=42):
    print(f"\n{'=' * 60}")
    print(f"Executando benchmark para verificar a precisão do Bloom Filter")
    print(f"{'=' * 60}\n")
    filepath = write_files(total_ops, seed)
    await run_benchmark(filepath)


if __name__ == "__main__":
    if(len(sys.argv) < 3):
        print("Usage: uv run -m src.bloom_filter_precision <total_ops> <seed>")
        sys.exit(1)
    total_ops = int(sys.argv[1])
    seed = int(sys.argv[2])
    asyncio.run(run_benchmarks(total_ops, seed))
        


    


    

