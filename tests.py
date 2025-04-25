import pytest



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

    fix_repetition(df)

    for i in range(len(df)):
        assert len(set(df.iloc[i])) == len(df.iloc[i])


def test_shift_single_column():
    import pandas as pd

    from main import shift_single_column

    data = {
        "carrier_letter": ["A", "B", "C", "D"],
        "column1": ["X", "Y", "Z", "W"],
    }
    df = pd.DataFrame(data)
    df_check = pd.DataFrame(data)
    shift_single_column(df, "column1", shift_value=1)
    

    assert df["column1"].iloc[0] == df_check["column1"].iloc[-1]
