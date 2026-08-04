import asyncio

from src.run_benchmarks import run_all_benchmarks
from src.run_tests import generate_all_tests


async def main():
    print("=" * 60)
    print("ETAPA 1: Geração dos arquivos de teste")
    print("=" * 60)
    generate_all_tests()

    print("\n" + "=" * 60)
    print("ETAPA 2: Execução dos benchmarks")
    print("=" * 60)
    await run_all_benchmarks(interval=10000)

    print("\n" + "=" * 60)
    print("ETAPA 3: Análise")
    print("=" * 60)
    print("Benchmarks concluídos. Abra notebooks/analysis.ipynb para análise.")
    print("Execute: jupyter notebook notebooks/analysis.ipynb")


if __name__ == "__main__":
    asyncio.run(main())
