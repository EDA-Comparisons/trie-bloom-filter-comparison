import asyncio
from asyncio import subprocess

from src.settings import JSON_DIR, RUST_BINARY, TXT_DIR


async def run_test(test_id, interval, structures=None, verbose=False):
    file_path = TXT_DIR / f"{test_id}.txt"

    cmd = [RUST_BINARY, str(file_path), str(interval), test_id, str(JSON_DIR)]

    if structures:
        for s in structures:
            cmd.append(f"--{s}")

    if verbose:
        cmd.append("--verbose")

    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    if stdout:
        print(stdout.decode())
    if stderr:
        print(stderr.decode())


async def main():
    await run_test("example_operations", 1, verbose=True)


if __name__ == "__main__":
    asyncio.run(main())
