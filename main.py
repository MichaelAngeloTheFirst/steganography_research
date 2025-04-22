import pandas as pd
import random
import string


def generate_alphabet_tuples():
    return [(chr(i), []) for i in range(ord("a"), ord("z") + 1)]


def generate_character_mapping():
    alphabet_tuples = generate_alphabet_tuples()
    for i in range(8):
        ascii_low = string.ascii_lowercase
        for t in alphabet_tuples:
            c = random.choice(ascii_low)
            t[1].append(c)
            ascii_low = ascii_low.replace(c, "")

    return alphabet_tuples


def generate_alphabet_df():
    # dataframe with indexes from 'a' to 'z' and columns 'value_1' to 'value_8'
    alphabet_df = pd.DataFrame(
        index=[chr(i) for i in range(ord("a"), ord("d") + 1)],
        columns=["column_" + str(i) for i in range(1, 3)],
    )
    alphabet_df.index.name = "carrier_letter"

    for each_column in alphabet_df.columns:
        ascii_low = string.ascii_lowercase
        for each_index in alphabet_df.index:
            c = random.choice(ascii_low)
            alphabet_df.loc[each_index, each_column] = c
            ascii_low = ascii_low.replace(c, "")

    alphabet_df.reset_index(level=0, inplace=True)

    return alphabet_df


def shift_single_column(df, column_name, shift_value=1):
    column_to_shift = df[column_name]

    lost_values = column_to_shift[-shift_value:]

    shifted_column = df[column_name].shift(shift_value)

    df[column_name] = pd.concat(
        [lost_values, shifted_column[shift_value:]]
    ).reset_index(drop=True)

    return df


def move_columns(df, column, column_to_change):
    """Function shifts the values of a column in one column, so there will be no same characters in the same row.
    Function should return df with columns with no same characters in the same row.
    """
    iter = 0
    was_shifted = False

    while any(df[column] == df[column_to_change]):
        print(f"Column {column} has same values as {column_to_change}")
        df = shift_single_column(df, column_to_change)
        was_shifted = True
        iter += 1
        if iter > 100:
            print("Too many iterations, breaking out of the loop.")
            break

    return df, was_shifted


def fix_repetition_for_one_column(df, column_to_change, iter):
    was_shifted = False
    for column in df.columns[1:iter]:
        print(f"Checking column {column} for repetition with {column_to_change}")
        if (
            column == column_to_change
        ):  # necessary to skip the column that is being changed
            continue
        df, was_shifted = move_columns(df, column, column_to_change)

    return df, was_shifted


def fix_repetition(df):
    """Function iterates over all columns comparing them and shifting the values; after shift it begins comparing columns from the start"""
    iter = -1 * len(df.columns[2:])

    was_shifted = True
    # skip carrier_letter and first column and fix repetition in the rest of the columns
    for column_to_change in df.columns[2:]:
        # print(column_to_change)
        while was_shifted:
            was_shifted = False
            df, was_shifted = fix_repetition_for_one_column(df, column_to_change, iter)
            print(column_to_change)

        iter += 1
        was_shifted = True

    return df
