import asyncio
from asyncio import subprocess

from src.settings import JSON_DIR, RUST_BINARY, TXT_DIR

RUNS = 20
TEST_FILES = 10

async def run_benchmark(interval, verbose=""):
    for i in range(1, TEST_FILES):
        read_ratio = i * 10
        setsug_ratio = 100 - read_ratio
        test_file_name =  "benchmark_" + str(read_ratio) + str(setsug_ratio)
        file_path = TXT_DIR / f"{test_file_name}.txt"
        await run_rust(file_path, interval, test_file_name, verbose)

async def run_rust(file_path, interval, test_file_name, verbose):
    for i in range(1, RUNS + 1):
            process = await asyncio.create_subprocess_exec(
                RUST_BINARY,
                str(file_path),
                interval,
                test_file_name + "_run_" + str(i),
                JSON_DIR,
                verbose,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            stdout, stderr = await process.communicate()
            if stdout:
                print(stdout.decode())
            if stderr:
                print(stderr.decode())


async def main():
    await run_benchmark("-1")


if __name__ == "__main__":
    asyncio.run(main())