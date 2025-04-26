import string
import pandas as pd
import pytest

from main import fix_repetition, shift_single_column
from generation import generate_alphabet_df, generate_character_mapping
from frequency import get_frequency_df, count_frequency


## ----- TESTS FOR GENERATION ---- ##

def test_generate_character_mapping():
    mapping = generate_character_mapping()
    assert len(mapping) == 26  # Check if there are 26 letters
    assert all(len(t[1]) == 8 for t in mapping)  # Check if each letter has 8 values
    assert all(t[0] in string.ascii_lowercase for t in mapping)  # Check if all letters are lowercase
    assert len(set(t[0] for t in mapping)) == len(mapping)  # Check if all letters are unique

def test_generate_alphabet_df():
    df = generate_alphabet_df()
    assert len(df) == 26  # Check if there are 26 rows
    assert len(df.columns) == 8  # Check if there are 8 columns
    assert all(df["carrier_letter"].apply(lambda x: x in string.ascii_lowercase))  # Check if all letters are lowercase
    assert df["carrier_letter"].is_unique  # Check if all letters are unique



## ----- TESTS FOR SHIFTING COLUMNS ---- ##

def test_shift_single_column():
    data = {
        "carrier_letter": ["A", "B", "C", "D"],
        "column1": ["X", "Y", "Z", "W"],
    }
    df = pd.DataFrame(data)
    df_check = pd.DataFrame(data)
    shift_single_column(df, "column1", shift_value=1)

    assert df["column1"].iloc[0] == df_check["column1"].iloc[-1]


def test_fix_repetition():
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
        
#  ---- TESTS FOR FREQUENCY ---- ##
def test_get_frequency_df():
    df = get_frequency_df()
    assert len(df) == 26  # Check if there are 26 letters
    assert "Letter" in df.columns  # Check if 'Letter' column exists
    assert "Frequency" in df.columns  # Check if 'Frequency' column exists
    assert all(df["Letter"].apply(lambda x: x in string.ascii_uppercase))  # Check if all letters are uppercase
    assert df["Letter"].is_unique  # Check if all letters are unique
    

def test_count_frequency():
    df = generate_alphabet_df()
    