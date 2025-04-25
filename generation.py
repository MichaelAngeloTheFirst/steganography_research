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
