import asyncio
import time
from asyncio import subprocess

from src.settings import JSON_DIR, RUST_BINARY, TXT_DIR


async def run_single_benchmark(test_id, interval=10000, structures=None, verbose=False):
    """Roda o binário Rust para um arquivo de teste específico."""
    file_path = TXT_DIR / f"{test_id}.txt"

    if not file_path.exists():
        print(f"  [PULAR] {test_id}.txt não encontrado")
        return

    cmd = [str(RUST_BINARY), str(file_path), str(interval), test_id, str(JSON_DIR)]

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
        print(stdout.decode().strip())
    if stderr:
        print(stderr.decode().strip())


async def run_all_benchmarks(interval=10000, structures=None):
    """
    Lista todos os arquivos .txt em data/tests/txt/ e roda o benchmark
    para cada um com todas as estruturas (bloom, trie, hashset).

    Args:
        interval: Intervalo de medição para evolução de memória/tempo.
        structures: Lista de estruturas para testar. None = todas.
    """
    if structures is None:
        structures = ["bloom", "trie", "hashset"]

    txt_files = sorted(TXT_DIR.glob("*.txt"))
    total = len(txt_files)
    print(f"\n{'=' * 60}")
    print(f"Executando {total} benchmarks com intervalo={interval}")
    print(f"Estruturas: {', '.join(structures)}")
    print(f"{'=' * 60}\n")

    for i, txt_file in enumerate(txt_files, 1):
        test_id = txt_file.stem
        print(f"[{i}/{total}] Executando: {test_id}")
        start = time.time()
        await run_single_benchmark(test_id, interval, structures)
        elapsed = time.time() - start
        print(f"  Concluído em {elapsed:.1f}s\n")


if __name__ == "__main__":
    asyncio.run(run_all_benchmarks())
