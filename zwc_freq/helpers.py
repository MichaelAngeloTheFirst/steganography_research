import pandas as pd


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
    sums = []
    df_freq = get_frequency_df()
    freq_map = dict(zip(df_freq["Letter"], df_freq["Frequency"]))
    for row in array:
        one_row_sum = 0
        for value in row:
            if value != "":
                if value in freq_map:
                    one_row_sum += freq_map[value]
            else:
                print("Empty value found in test_frequency")

        sums.append(one_row_sum)
    delta = max(sums) - min(sums)
    return sums, delta


def get_frequency_df():
    data = {
        "Letter": [
            "a",
            "b",
            "c",
            "d",
            "e",
            "f",
            "g",
            "h",
            "i",
            "j",
            "k",
            "l",
            "m",
            "n",
            "o",
            "p",
            "q",
            "r",
            "s",
            "t",
            "u",
            "v",
            "w",
            "x",
            "y",
            "z",
        ],
        "Frequency": [
            8.738241,
            1.739706,
            1.539737,
            5.01902,
            12.29746,
            1.919627,
            2.159564,
            6.338739,
            6.958567,
            0.37989,
            1.459672,
            3.839253,
            2.659487,
            6.178738662,
            8.058397106,
            1.099830039,
            0.060016268,
            4.559065585,
            6.458644322,
            9.658022196,
            2.899424227,
            0.99984549,
            2.819487665,
            0.079936562,
            1.979642993,
            0.099984549,
        ],
    }

    return pd.DataFrame(data)
