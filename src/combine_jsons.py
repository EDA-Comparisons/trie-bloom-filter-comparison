import os
import re
import glob
import pandas as pd

from collections import defaultdict
from src.settings import JSON_DIR

PATTERNS = [re.compile(r"^benchmark_(\d{4})_(.+)_run_(\d+)\.json$"), 
            re.compile(r"^benchmark_(100get)_(.+)_run_(\d+)\.json$"),
            re.compile(r"^benchmark_(100set)_(.+)_run_(\d+)\.json$"),
            ]


def combine_benchmark_jsons():
    groups = defaultdict(list)

    for file in glob.glob(os.path.join(JSON_DIR, "*.json")):
        name = os.path.basename(file)
        match = None
        for pattern in PATTERNS:
            match = pattern.match(name)
            if match:
                break

        if not match:
            continue

        id = match.group(1)
        load = match.group(2)
        run = int(match.group(3))

        grupo = (id, load)

        groups[grupo].append({"path" : file, "run" : run})

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
        output = f"benchmark_{id}_{load}.json"
        output_path = os.path.join(JSON_DIR, output)
        df_combined.to_json(output_path, orient="records", indent=4)
        print(f"Resultados combinados! -> {output_path}")

if __name__ == "__main__":
    combine_benchmark_jsons()
