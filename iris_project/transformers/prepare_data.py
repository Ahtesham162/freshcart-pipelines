import pandas as pd
from sklearn.model_selection import train_test_split

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer, test
@transformer
def transform(df, *args, **kwargs):
    X = df.drop(columns=["target", "target_name"])
    y = df["target"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    train = X_train.copy()
    train["target"] = y_train
    train["split"] = "train"

    test_data = X_test.copy()
    test_data["target"] = y_test
    test_data["split"] = "test"

    return pd.concat([train, test_data]).sort_index()

@test
def test_output(output, *args):
    assert len(output) == 150
    assert (output["split"] == "train").sum() == 120
    assert (output["split"] == "test").sum() == 30