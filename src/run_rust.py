import asyncio
import sys
from asyncio import subprocess

from src.settings import TXT_DIR, RUST_BINARY, JSON_DIR, RUNS

async def run_rust(test_file_path, interval, result_file_name, verbose):
    for i in range(1, RUNS + 1):
            process = await asyncio.create_subprocess_exec(
                RUST_BINARY,
                str(test_file_path),
                interval,
                result_file_name + "_run_" + str(i),
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
    test_file_name = sys.argv[1]
    test_file_path = TXT_DIR / test_file_name
    interval = str(sys.argv[2]) if len(sys.argv) > 2 else "-1"
    verbose = sys.argv[3] if len(sys.argv) > 3 else ""
    await run_rust(test_file_path, interval, test_file_name.removesuffix(".txt"), verbose)

if __name__ == "__main__":
    asyncio.run(main())
