import pandas as pd
import numpy as np
import random
import string
from archive.frequency import get_frequency_df
import time

benchmark_for_generate_unique_arr = []


def generate_shuffled_alphabet():
    shuffled_alphabet = list(string.ascii_lowercase)
    random.shuffle(shuffled_alphabet)
    return shuffled_alphabet


def check_duplicates(array):
    for i in range(len(array)):
        if len(set(array[i])) != len(array[i]):
            return False  # Return False as soon as a duplicate is found
    return True


def check_no_duplicates(array):
    """Checks for duplicates in both rows and columns."""
    # Check for duplicates in columns
    # for col in range(array.shape[1]):
    #     if len(set(array[:, col])) != len(array[:, col]):
    #         return False

    # Check for duplicates in rows
    for row in range(array.shape[0]):
        if len(set(array[row, :])) != len(array[row, :]):
            return False

    return True


def generate_unique_dataframe():
    td_array = generate_unique_arr()
    return pd.DataFrame(td_array, columns=[f"column_{i}" for i in range(1, 9)])


def generate_unique_arr():
    # check time
    start_time = time.time()
    rows, cols = 26, 8

    td_array = np.empty((rows, cols), dtype=str)

    for c in range(cols):
        td_array[:, c] = generate_shuffled_alphabet()

        # iterations = 0
        while not check_duplicates(td_array[:, : c + 1]):
            td_array[:, c] = generate_shuffled_alphabet()
            # iterations += 1

    # print(f"Iteration: {iterations}")
    end_time = time.time()
    benchmark_for_generate_unique_arr.append(end_time - start_time)

    # print(td_array)
    # rows, cols = 26, 8
    # td_array = np.empty((rows, cols), dtype=str)
    # seen_rows = set()

    # for r in range(rows):
    #     max_attempts = 1000
    #     attempts = 0

    #     while attempts < max_attempts:
    #         new_row = generate_shuffled_alphabet()[:cols]
    #         row_tuple = tuple(new_row)

    #         if row_tuple not in seen_rows:
    #             td_array[r] = new_row
    #             seen_rows.add(row_tuple)
    #             break

    #         attempts += 1

    #     if attempts == max_attempts:
    #         raise RuntimeError(
    #             f"Failed to generate a unique row {r} after {max_attempts} attempts"
    #         )

    return td_array


def test_frequency(arr):
    df_freq = get_frequency_df()
    freq_map = dict(zip(df_freq["Letter"], df_freq["Frequency"]))
    sums = []
    for row in arr:
        one_row_sum = 0
        for value in row:
            one_row_sum += freq_map[value]
        sums.append(one_row_sum)

    delta = max(sums) - min(sums)
    print(f"{max(sums)} - {min(sums)}={delta}")

    if delta > 20:
        return False
    return True


if __name__ == "__main__":
    print("Generating unique dataframe...")
    arr = generate_unique_arr()
    i = 0

    start_time = time.time()
    while not test_frequency(arr):
        print(f"Iteration: {i}")
        i += 1
        arr = generate_unique_arr()
    print(arr)
    end_time = time.time()
    print(f"Time taken: {end_time - start_time} seconds")

    # for i in range(500):
    #     arr = generate_unique_arr()

    # print(arr)
    # print(arr[0])
    # print("Benchmark for generate_unique_arr:")
    # print(np.mean(benchmark_for_generate_unique_arr))
    # print(np.sum(benchmark_for_generate_unique_arr))
