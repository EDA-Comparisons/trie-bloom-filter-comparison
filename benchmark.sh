DIR="$(dirname "$0")"

LOAD=$1
SEED=$2
uv run -m src.main $LOAD $SEED
bash "$DIR/clean.sh" benchmark