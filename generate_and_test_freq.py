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

def check_column_duplicates(array):
    for col in range(array.shape[1]):
        if len(set(array[:, col])) != len(array[:, col]):
            return False  # Return False as soon as a duplicate is found
    return True

def test_frequency(array):
    df_freq = get_frequency_df()
    freq_map = dict(zip(df_freq["Letter"], df_freq["Frequency"]))
    sums = []
    # Check frequency of each row and match values with delta
    for row in array:
        one_row_sum = 0
        for value in row:
            one_row_sum += freq_map[value]
        sums.append(one_row_sum)
    return sums,  max(sums) - min(sums)


def generate_unique_arr():
    start_time = time.time()
    rows, cols = 26, 8
    td_array = np.empty((rows, cols), dtype=str)

    # Generate without duplicates
    for c in range(cols):
        td_array[:, c] = generate_shuffled_alphabet()

        while not check_duplicates(td_array[:, : c + 1]):
            td_array[:, c] = generate_shuffled_alphabet()

    # regenerate to match frequency
    df_freq = get_frequency_df()
    freq_map = dict(zip(df_freq["Letter"], df_freq["Frequency"]))

   

    
    while  True:
        # tracking count of excluded rows
        excluded_rows = 0
        
        # Check frequency of each row and match values with delta
        for row in td_array:
            one_row_sum = 0
            for value in row:
                one_row_sum += freq_map[value]
            if one_row_sum > 32 or one_row_sum < 28:
                excluded_rows += 1
                row.fill("")
        
        if excluded_rows == 0:
            break

        print(f"Excluded rows: {excluded_rows}")

        # Regenerate columns with empty rows
        for c in range(cols):
            # make array of existing values
            # existing_values = [value for value in td_array[:, c] if value != ""] #fix td_array[c] instead of td_array[:, c]
            
            # # Generate shuffled alphabet excluding existing values
            # new_values = generate_shuffled_alphabet(existing_values)
            
            # Fill empty rows with new values no duplicates in each row
            for i in range(len(td_array)):
                if td_array[i, c] == "":
                    existing_values = [value for value in td_array[:,c] if value != ""]
                    new_values = generate_shuffled_alphabet(existing_values)
                    td_array[i, c] = new_values.pop(0)
                    
                    # Check if the new value is unique in the row
                    while td_array[i, c] in td_array[i, :c]:
                        existing_values = [value for value in td_array[:,c] if value != ""]
                        new_values = generate_shuffled_alphabet(existing_values)
                        td_array[i, c] = new_values.pop(0)
                    

    end_time = time.time()
    print(f"Time taken to generate unique array: {end_time - start_time} seconds")
    return td_array


if __name__ == "__main__":
    # Test the function
    td_array = generate_unique_arr()
    print(td_array)
    print(f'are rows unique: {check_duplicates(td_array)}')
    print(f'are columns unique: {check_column_duplicates(td_array)}')
    sums, delta = test_frequency(td_array)
    print(f'max: {max(sums)} min: {min(sums)} delta: {delta}')
