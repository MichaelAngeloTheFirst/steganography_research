import pytest


def test_addition():
    assert 1 + 1 == 2


def test_fix_repetition():
    import pandas as pd

    from main import fix_repetition

    data = {
        "carrier_letter": ["A", "B", "C", "D"],
        "column1": ["X", "Y", "Z", "W"],
        "column2": ["Y", "Z", "W", "X"],
        "column3": ["Z", "W", "X", "Y"],
    }
    df = pd.DataFrame(data)

    fixed_df = fix_repetition(df)

    for i in range(len(fixed_df)):
        assert len(set(fixed_df.iloc[i])) == len(fixed_df.iloc[i])


def test_shift_single_column():
    import pandas as pd

    from main import shift_single_column

    data = {
        "carrier_letter": ["A", "B", "C", "D"],
        "column1": ["X", "Y", "Z", "W"],
    }
    df = pd.DataFrame(data)

    shifted_df = shift_single_column(df, "column1", shift_value=1)
    df = pd.DataFrame(data)

    assert shifted_df["column1"].iloc[0] == df["column1"].iloc[-1]
