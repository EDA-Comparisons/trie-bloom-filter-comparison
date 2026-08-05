set -e

VERBOSE=""
ARGS=""
DIR="$(dirname "$0")"

while [ $# -gt 0 ]; do
  case "$1" in
    --verbose)
      VERBOSE="--verbose"
      shift 1
      ;;
    *)
      ARGS="$ARGS \"$1\""
      shift 1
      ;;
  esac
done

eval set -- "$ARGS"

if [ $# -lt 3 ] || [ $# -gt 4 ]; then
  echo "Quantidade inválida de argumentos"
  echo "Use: $0 <load> <seed> <measure-interval> [--verbose]"
  exit 1
fi

LOAD=$1 
SEED=$2
INTERVAL=$3

format_number() {
  echo "$1" | awk '
    $1 >= 1000000 {printf "%.0fm\n", $1 / 1000000; next}
    $1 >= 1000    {printf "%.0fk\n", $1 / 1000; next}
    $1 <  1000    {print $1}
  '
}

LOAD_FORMATTED=$(format_number "$LOAD")

run_ratioread_benchmark(){
    uv run -m src.generator_scripts.allreadratio_test_data $LOAD $SEED
    uv run -m src.benchmark $LOAD $INTERVAL $VERBOSE
}

run_100get_benchmark(){
    OUTPUT_TXT_FILE="benchmark_100get_${LOAD_FORMATTED}.txt"
    uv run -m src.generator_scripts.setreadratio_test_data $OUTPUT_TXT_FILE $LOAD 1 $SEED
    uv run -m src.run_rust $OUTPUT_TXT_FILE $INTERVAL $VERBOSE
}

run_100set_benchmark(){
    OUTPUT_TXT_FILE="benchmark_100set_${LOAD_FORMATTED}.txt"
    uv run -m src.generator_scripts.setreadratio_test_data $OUTPUT_TXT_FILE $LOAD 0 $SEED
    uv run -m src.run_rust $OUTPUT_TXT_FILE $INTERVAL $VERBOSE
}

run_ratioread_benchmark
run_100get_benchmark
run_100set_benchmark

uv run -m src.combine_jsons
bash "$DIR/clean.sh" benchmark                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
