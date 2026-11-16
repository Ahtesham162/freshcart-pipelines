
if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer, test

@transformer
def validate(df, *args, **kwargs):
    missing_values = int(df.isnull().sum().sum())
    class_count = int(df["target"].nunique())

    print("Missing values:", missing_values)
    print("Number of classes:", class_count)

    return {
        "missing_values": missing_values,
        "class_count": class_count
    }

@test
def test_output(output, *args):
    assert output["missing_values"] == 0
    assert output["class_count"] == 3
