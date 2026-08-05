from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
TEST_DIR = DATA_DIR / "tests"
JSON_DIR = TEST_DIR / "json"
TXT_DIR = TEST_DIR / "txt"

GRAPHS_DIR = DATA_DIR / "graphs"

RUST_BINARY = BASE_DIR / "rust" / "target" / "release" / "benchmark"
