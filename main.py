import pandas as pd


def shift_single_column(df, column_name, shift_value=1):
    column_to_shift = df[column_name]

    lost_values = column_to_shift[-shift_value:]

    shifted_column = df[column_name].shift(shift_value)

    df[column_name] = pd.concat(
        [lost_values, shifted_column[shift_value:]]
    ).reset_index(drop=True)


def move_columns(df, column, column_to_change):
    """Function shifts the values of a column in one column, so there will be no same characters in the same row."""
    iter = 0
    was_shifted = False

    while any(df[column] == df[column_to_change]):
        # print(f"Column {column} has same values as {column_to_change}")
        shift_single_column(df, column_to_change)
        was_shifted = True
        iter += 1
        if iter > 100:
            print("Too many iterations, breaking out of the loop.")
            break

    return was_shifted


def fix_repetition_for_one_column(df, column_to_change, iter):
    was_shifted = False
    for column in df.columns[1:iter]:
        print(f"Checking column {column} for repetition with {column_to_change}")
        if column == column_to_change:
            continue
        was_shifted = move_columns(df, column, column_to_change)

    return was_shifted


def fix_repetition(df):
    """Function iterates over all columns comparing them and shifting the values; after shift it begins comparing columns from the start"""
    iter = -1 * len(df.columns[2:])

    was_shifted = True
    for column_to_change in df.columns[2:]:
        while was_shifted:
            was_shifted = False
            was_shifted = fix_repetition_for_one_column(df, column_to_change, iter)
            # print(column_to_change)

        iter += 1
        was_shifted = True
