
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer, test

@transformer
def train(data, *args, **kwargs):
    train_data = data[data["split"] == "train"]
    test_data = data[data["split"] == "test"]

    X_train = train_data.drop(columns=["target", "split"])
    y_train = train_data["target"]

    X_test = test_data.drop(columns=["target", "split"])
    y_test = test_data["target"]

    max_depth = int(kwargs.get("max_depth", 3))

    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=max_depth,
        random_state=42
    )

    model.fit(X_train, y_train)
    predictions = model.predict(X_test).tolist()
    accuracy = accuracy_score(y_test, predictions)
    print(f"MAX_DEPTH={max_depth}, ACCURACY={accuracy:.4f}")

    return {
        "accuracy": float(accuracy),
        "max_depth": max_depth,
        "y_test": y_test.tolist(),
        "predictions": predictions
    }

@test
def test_output(output, *args):
    assert 0 <= output["accuracy"] <= 1
    assert len(output["predictions"]) == 30
    assert len(output["y_test"]) == 30
    
