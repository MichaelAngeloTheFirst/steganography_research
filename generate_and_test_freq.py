import pandas as pd
import numpy as np
import random
import string
from frequency import get_frequency_df
import time


def generate_shuffled_alphabet(values_to_remove=[]):
    shuffled_alphabet = list(set(string.ascii_lowercase) - set(values_to_remove))
    random.shuffle(shuffled_alphabet)
    return shuffled_alphabet


def check_duplicates(array):
    for i in range(len(array)):
        if len(set(array[i])) != len(array[i]):
            return False  # Return False as soon as a duplicate is found
    return True


def generate_unique_arr():
    start_time = time.time()
    rows, cols = 26, 8
    td_array = np.empty((rows, cols), dtype=str)

    # Generate without duplicates
    for c in range(cols):
        td_array[:, c] = generate_shuffled_alphabet()

        while not check_duplicates(td_array[:, : c + 1]):
            td_array[:, c] = generate_shuffled_alphabet()

    # regenerate to much frequency
    df_freq = get_frequency_df()
    freq_map = dict(zip(df_freq["Letter"], df_freq["Frequency"]))

    for row in td_array:
        one_row_sum = 0
        for value in row:
            one_row_sum += freq_map[value]
            if one_row_sum > 38 or one_row_sum < 22:
                # empty the row
                row.fill("")
    print(f"Row sum: {one_row_sum}")

    # Regenerate columns with empty rows
    for c in range(cols):
        # make array of existing values
        existing_values = [value for value in td_array[c] if value != ""]
        # Generate shuffled alphabet excluding existing values

    end_time = time.time()
    print(f"Time taken to generate unique array: {end_time - start_time} seconds")
    return td_array


if __name__ == "__main__":
    # Test the function
    td_array = generate_unique_arr()
    print(td_array)
