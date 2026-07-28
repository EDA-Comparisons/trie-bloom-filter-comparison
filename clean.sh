PREFIX="benchmark"

clean_json(){
    TARGET_DIR="data/tests/json"
    if [ -d "$TARGET_DIR" ]; then
        find "$TARGET_DIR" -maxdepth 1 -type f -name "${PREFIX}*" -delete
        echo "Os arquivos JSON foram limpos"
    else
        exit 1
    fi
}
clean_txt(){
    TARGET_DIR="data/tests/txt"
    if [ -d "$TARGET_DIR" ]; then
        find "$TARGET_DIR" -maxdepth 1 -type f -name "${PREFIX}*" -delete
        echo "Os arquivos TXT foram limpos"
    else
        exit 1
    fi
}

case "$1" in
    json)
        clean_json
        ;;
    txt)
        clean_txt
        ;;
    both)
        clean_json
        clean_txt
        ;;
    "")
        clean_json
        clean_txt
        ;;
    *)
        exit 1
        ;;
    
esac