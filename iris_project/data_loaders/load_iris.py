
from sklearn.datasets import load_iris
import pandas as pd

@data_loader
def load_data(*args, **kwargs):
    iris = load_iris(as_frame=True)
    df = iris.frame
    df["target_name"] = df["target"].map(dict(enumerate(iris.target_names)))
    return df

@test
def test_output(output, *args):
    assert output is not None
    assert len(output) == 150
    assert "target" in output.columns
