import string
import pandas as pd
import pytest



from frequency import count_frequency
from generation import generate_unique_dataframe, check_duplicates


def test_generate_uniqe_dataframe():
    alphabet_tuples = generate_unique_dataframe()
    assert len(alphabet_tuples) == 26, "Should generate 26 unique characters"
    assert len(alphabet_tuples.columns) == 8, (
        "Should generate 8 unique characters per letter"
    )
    assert check_duplicates([t[1] for t in alphabet_tuples]), (
        "Mappings should be unique"
    )


def test_count_frequency():
    df = generate_unique_dataframe()
    i=0
    while count_frequency(df):
        df = generate_unique_dataframe()
        print(f"Iteration: {i}")
        i+=1
    
    # print(df)