
import pandas as pd
import os

@data_exporter
def export(data, *args, **kwargs):
    os.makedirs("iris_project", exist_ok=True)

    results = pd.DataFrame({
        "actual": data["y_test"],
        "predicted": data["predictions"]
    })

    results.to_csv("iris_project/iris_predictions.csv", index=False)

    return {"accuracy": data["accuracy"], "rows_saved": len(results)}

@test
def test_output(output, *args):
    assert output["rows_saved"] == 30
    assert output["accuracy"] > 0
    assert os.path.exists("iris_project/iris_predictions.csv")
