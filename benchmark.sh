set -e

LOAD=$1 
SEED=$2
PREFIX=$3

clean_json_runs(){
    TARGET_DIR="data/tests/json"
    if [ -d "$TARGET_DIR" ]; then
        find "$TARGET_DIR" -maxdepth 1 -type f -name "*_run_*.json*" -delete
    else
        return 1
    fi
}

uv run -m src.generate_benchmark_data $LOAD $SEED $PREFIX
uv run -m src.benchmark $LOAD
uv run -m src.combine_jsons
clean_json_runs
