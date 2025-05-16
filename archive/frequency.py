import pandas as pd


def get_frequency_df():
    data ={"Letter": [
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


def count_frequency(df):
    # TO DO: Implement the function to count frequency of letters in the dataframe
    # take dataframe and add sum of frequency of each letter in the row
    # and add it to the last column
    df_frequency = get_frequency_df()
    freq_map = dict(zip(df_frequency["Letter"], df_frequency["Frequency"]))
    df_transposed = df.transpose()
    # print(df_transposed)
    sum = []
    for column in df_transposed:
        # print(f"Column: {column}")
        one_column_sum = 0
        for value in df_transposed[column]:
            # print(df_transposed[column][1:])
            # print(freq_map[value])
            one_column_sum += freq_map[value]
            # one_column_sum +=
        # P = (one_column_sum / 26) * 8

        # print(P)

        sum.append(one_column_sum)
    # print(sum)
    delta = max(sum) - min(sum)
    print(f"{max(sum)} - {min(sum)}={delta}")
    if delta > 15:
        return True
    return False
