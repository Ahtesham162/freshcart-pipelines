
try:
    from mage_ai.data_preparation.decorators import transformer, test
except ImportError:
    def transformer(func):
        return func

    def test(func):
        return func

@transformer
def transform(df, *args, **kwargs):
    from sklearn.model_selection import train_test_split
    import pandas as pd

    X = df.drop(columns=["target"])
    y = df["target"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    train = X_train.copy()
    train["target"] = y_train
    train["split"] = "train"

    test = X_test.copy()
    test["target"] = y_test
    test["split"] = "test"

    return pd.concat([train, test]).sort_index()

@test
def test_output(output, *args):
    assert len(output) == 150
    assert output["split"].isin(["train", "test"]).all()
