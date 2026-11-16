
import subprocess
import json
import os

for depth in range(1, 6):
    print(f"\n========== MAX_DEPTH: {depth} ==========")

    path = "iris_project/iris_predictions.csv"

    if os.path.exists(path):
        os.remove(path)

    subprocess.run([
        "mage", "run", "iris_project", "iris_classifier",
        "--runtime-vars", json.dumps({"max_depth": depth}),
        "--test"
    ], check=True)

    print(f"CSV_CREATED: {os.path.exists(path)}")
