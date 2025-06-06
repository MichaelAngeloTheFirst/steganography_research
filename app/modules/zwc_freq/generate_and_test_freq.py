import pandas as pd
import numpy as np
import random
import string
from app.modules.zwc_freq.helpers import get_frequency_df
import time

from zwc_freq.helpers import check_duplicates, check_column_duplicates, test_frequency


def generate_shuffled_alphabet(values_to_remove=[]):
    shuffled_alphabet = list(set(string.ascii_lowercase) - set(values_to_remove))
    random.shuffle(shuffled_alphabet)
    return shuffled_alphabet


def first_not_in_second(list1, list2):
    difference = set(list1) - set(list2)
    for item in list1:
        if item in difference:
            return item
    return None


def no_empty_values(array):
    for row in array:
        if "" in row:
            return False
    return True

# the function to be used to generate the unique array
def generate_unique_arr():
    start_time = time.time()
    rows, cols = 26, 8
    td_array = np.empty((rows, cols), dtype=str)

    # 1------- GENERATE WITH DUPLICATES -------
    for c in range(cols):
        td_array[:, c] = generate_shuffled_alphabet()

        while not check_duplicates(td_array[:, : c + 1]):
            td_array[:, c] = generate_shuffled_alphabet()

    # 2------- CHECK FREQUENCY  -------
    # Get frequency map from the frequency dataframe
    df_freq = get_frequency_df()
    freq_map = dict(zip(df_freq["Letter"], df_freq["Frequency"]))

    long_loop = 0

    while True:
        # tracking count of excluded rows
        excluded_rows = 0
        long_loop += 1
        if long_loop > 50:
            long_loop = 0
            # print(td_array)
            print("Long loop detected, regenerating the entire array")
            td_array = np.empty((rows, cols), dtype=str)

            # 1------- GENERATE WITH DUPLICATES -------
            for c in range(cols):
                td_array[:, c] = generate_shuffled_alphabet()

                while not check_duplicates(td_array[:, : c + 1]):
                    td_array[:, c] = generate_shuffled_alphabet()

        # Check frequency of each row and match values with delta
        for row in td_array:
            one_row_sum = 0
            for value in row:
                # Check if the value is in the frequency map
                if value in freq_map:
                    one_row_sum += freq_map[value]
            if one_row_sum > 32 or one_row_sum < 28:
                excluded_rows += 1
                row.fill("")

        if excluded_rows == 0 and no_empty_values(td_array):
            break

        print(f"Excluded rows: {excluded_rows}")

        # Regenerate values for columns with empty rows
        for c in range(cols):
            existing_values = [value for value in td_array[:, c] if value != ""]
            missing_values = generate_shuffled_alphabet(existing_values)

            for i in range(len(td_array)):
                if td_array[i, c] == "":
                    # get values from the row
                    row_values = [value for value in td_array[i, :] if value != ""]

                    value_to_add = first_not_in_second(missing_values, row_values)
                    if value_to_add is not None:
                        td_array[i, c] = value_to_add
                        missing_values.remove(value_to_add)
                    else:
                        print("No value to add")
                        break

    end_time = time.time()
    print(f"Time taken to generate unique array: {end_time - start_time} seconds")
    return td_array


def save_to_csv(array, filename="unique_array.csv"):
    df = pd.DataFrame(array, columns=[f"column_{i}" for i in range(1, 9)])
    df.to_csv(filename, index=False, header=True)




# if __name__ == "__main__":

#     # Test the function
#     td_array = generate_unique_arr()
#     print(td_array)
#     print(f"are rows unique: {check_duplicates(td_array)}")
#     print(f"are columns unique: {check_column_duplicates(td_array)}")
#     sums, delta = test_frequency(td_array)
#     print(f"max: {max(sums)} min: {min(sums)} \n delta: {delta}")
#     # save the array to a CSV file
#     save_to_csv(td_array)

