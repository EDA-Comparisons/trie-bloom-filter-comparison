import os
import re
import glob
import pandas as pd

from collections import defaultdict
from src.settings import JSON_DIR


def combine_benchmark_jsons():
    groups = defaultdict(list)
    pattern = re.compile(r"^test_(?P<number>\d+)_(?P<id>.+)_(?P<load>\d+[km])_run_(?P<run_number>\d+)\.json$")
    for file in glob.glob(os.path.join(JSON_DIR, "*.json")):
        name = os.path.basename(file)
        match = pattern.match(name)
        if match:
            data = match.groupdict()
            grupo = (data.get("id"), data.get("load"))
            groups[grupo].append({"path" : file, "run" : int(data.get("run_number", 0))})

        if not match:
            continue


    for (id, load), files in groups.items():
        files.sort(key=lambda x : x["run"])
        df = []
        for file in files:
            try:
                df_file = pd.read_json(file["path"])
                df.append(df_file)

            except Exception as e:
                print(f"Não foi possível ler o arquivo {file}")

        df_combined = pd.concat(df, ignore_index=True)
        output = f"test_{id}_{load}.json"
        output_path = os.path.join(JSON_DIR, output)
        df_combined.to_json(output_path, orient="records", indent=4)
        print(f"Resultados combinados! -> {output_path}")

if __name__ == "__main__":
    combine_benchmark_jsons()