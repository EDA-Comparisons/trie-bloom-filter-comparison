import asyncio
from asyncio import subprocess

from src.settings import TXT_DIR, RUST_BINARY, JSON_DIR

async def run_test(test_id, interval, verbose):

    file_path = TXT_DIR / f"{test_id}.txt"
    print(file_path)
    process = await asyncio.create_subprocess_exec(
        RUST_BINARY,
        str(file_path),
        interval,
        test_id,
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
    await run_test("example_operations", "1", "--verbose")


if __name__ == "__main__":
    asyncio.run(main())
