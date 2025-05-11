import pandas as pd
import numpy as np
import random
import string


def check_duplicates(array):
    for i in range(len(array)):
        if len(set(array[i])) != len(array[i]):
            return False  # Return False as soon as a duplicate is found
    return True


def generate_shuffled_alphabet():
    shuffled_alphabet = list(string.ascii_lowercase)
    random.shuffle(shuffled_alphabet)
    return shuffled_alphabet


def generate_unique_dataframe():
    rows, cols = 26, 8

    td_array = np.empty((rows, cols), dtype=str)

    for c in range(cols):
        td_array[:, c] = generate_shuffled_alphabet()

        iterations = 0
        while not check_duplicates(td_array[:, : c + 1]):
            td_array[:, c] = generate_shuffled_alphabet()
            iterations += 1

        print(f"Iteration: {iterations}")

    print(td_array)
    return pd.DataFrame(td_array, columns=[f"column_{i}" for i in range(1, 9)])


if __name__ == "__main__":
    df = generate_unique_dataframe()
    print(len(df.columns))
