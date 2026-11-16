
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

@transformer
def train(data, *args, **kwargs):
    values = data.iloc[0] if isinstance(data, pd.DataFrame) else data

    X_train = values["X_train"]
    X_test = values["X_test"]

    y_train = [v["target"] for v in values["y_train"]]
    y_test = [v["target"] for v in values["y_test"]]

    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=3,
        random_state=42
    )

    model.fit(X_train, y_train)
    predictions = model.predict(X_test).tolist()
    accuracy = accuracy_score(y_test, predictions)

    return {
        "accuracy": float(accuracy),
        "y_test": y_test,
        "predictions": predictions
    }

@test
def test_output(output, *args):
    assert 0 <= output["accuracy"] <= 1
    assert len(output["predictions"]) == 30
    assert len(output["y_test"]) == 30
