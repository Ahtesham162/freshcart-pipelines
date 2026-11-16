
import pandas as pd
import os

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter, test

@data_exporter
def export(data, *args, **kwargs):
    os.makedirs("iris_project", exist_ok=True)
    df = pd.DataFrame([data["metrics"]])
    df.to_csv("iris_project/iris_metrics.csv", index=False)
    return {"rows_saved": len(df)}

@test
def test_output(output, *args):
    assert output["rows_saved"] == 1
    assert os.path.exists("iris_project/iris_metrics.csv")
