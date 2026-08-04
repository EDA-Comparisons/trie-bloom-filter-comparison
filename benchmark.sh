DIR="$(dirname "$0")"

LOAD=$1
uv run -m src.main $LOAD
bash "$DIR/clean.sh" benchmark