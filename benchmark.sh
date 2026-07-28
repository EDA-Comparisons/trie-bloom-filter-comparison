set -e

LOAD=$1 
SEED=$2
PREFIX=$3
INTERVAL=$4
VERBOSE=$5

DIR="$(dirname "$0")"

run_ratioread_benchmark(){
    uv run -m src.generator_scripts.allreadratio_test_data $LOAD $SEED $PREFIX
    uv run -m src.benchmark $LOAD $INTERVAL 
}

run_noadd_benchmark(){
    OUTPUT_TXT_FILE="benchmark_noadd_${LOAD}.txt"
    uv run -m src.generator_scripts.setreadratio_test_data $OUTPUT_TXT_FILE $LOAD 1 $SEED $PREFIX
    uv run -m src.run_rust $OUTPUT_TXT_FILE $INTERVAL $VERBOSE
}

run_onlyuser_benchmark(){
    OUTPUT_TXT_FILE="benchmark_onlyuser_${LOAD}.txt"
    uv run -m src.generator_scripts.onlyuser_test_data 1 $OUTPUT_TXT_FILE $LOAD $SEED $PREFIX
    uv run -m src.run_rust $OUTPUT_TXT_FILE $INTERVAL $VERBOSE
}

run_onlyadd_benchmark(){
    OUTPUT_TXT_FILE="benchmark_onlyadd_${LOAD}.txt"
    uv run -m src.generator_scripts.setreadratio_test_data $OUTPUT_TXT_FILE $LOAD 0 $SEED $PREFIX
    uv run -m src.run_rust $OUTPUT_TXT_FILE $INTERVAL $VERBOSE
}

run_addonlyuser_benchmark(){
    OUTPUT_TXT_FILE="benchmark_addonlyuser_${LOAD}.txt"
    uv run -m src.generator_scripts.onlyuser_test_data 2 $OUTPUT_TXT_FILE $LOAD $SEED $PREFIX
    uv run -m src.run_rust $OUTPUT_TXT_FILE $INTERVAL $VERBOSE
}

run_ratioread_benchmark
run_noadd_benchmark
run_onlyuser_benchmark
run_onlyadd_benchmark
run_addonlyuser_benchmark

uv run -m src.combine_jsons
bash "$DIR/clean.sh" benchmark
