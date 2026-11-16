
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer, test

@transformer
def evaluate(data, *args, **kwargs):
    y_test = data["y_test"]
    predictions = data["predictions"]

    metrics = {
        "accuracy": float(accuracy_score(y_test, predictions)),
        "precision": float(precision_score(y_test, predictions, average="weighted")),
        "recall": float(recall_score(y_test, predictions, average="weighted")),
        "f1_score": float(f1_score(y_test, predictions, average="weighted"))
    }

    cm = confusion_matrix(y_test, predictions)

    print("Evaluation Metrics:", metrics)
    print("Confusion Matrix:")
    print(cm)

    return {
        "metrics": metrics,
        "confusion_matrix": cm.tolist()
    }

@test
def test_output(output, *args):
    assert 0 <= output["metrics"]["accuracy"] <= 1
    assert len(output["confusion_matrix"]) == 3
    assert all(len(row) == 3 for row in output["confusion_matrix"])
