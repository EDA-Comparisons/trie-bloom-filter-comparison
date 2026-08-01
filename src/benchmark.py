import asyncio
import sys

from src.settings import TXT_DIR
from src.run_rust import run_rust
from src.generator_scripts.utils import load_str

TEST_FILES = 10

async def run_benchmark(load, interval, verbose):
    for i in range(1, TEST_FILES):
        read_ratio = i * 10
        setsug_ratio = 100 - read_ratio
        result_file_name =  "benchmark_" + str(read_ratio) + str(setsug_ratio) + "_" + load_str(load)
        file_path = TXT_DIR / f"{result_file_name}.txt"
        await run_rust(file_path, interval, result_file_name, verbose)

async def main():
    load = int(sys.argv[1])
    interval = sys.argv[2] if len(sys.argv) > 2 else "-1"
    verbose = sys.argv[3] if len(sys.argv) > 3 else ""   
    await run_benchmark(load, interval, verbose)

if __name__ == "__main__":
    asyncio.run(main())