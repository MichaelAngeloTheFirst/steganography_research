import pandas as pd



def get_frequency_df():
    data = {
        "Letter": ['e', 't', 'a', 'o', 'i', 'n', 's', 'r', 'h', 'd', 'l', 'u', 'c', 'm', 'f', 'y', 'w', 'g', 'p', 'b', 'v', 'k', 'x', 'q', 'j', 'z'],
        "Frequency": [12.02, 9.10, 8.12, 7.68, 7.31, 6.95, 6.28, 6.02, 5.92, 4.32, 3.98, 2.88, 2.71, 2.61, 2.30, 2.11, 2.09, 2.03, 1.82, 1.49, 1.11, 0.69, 0.17, 0.11, 0.10, 0.07]
    }
     
    return pd.DataFrame(data)




def count_frequency(df):
    # TO DO: Implement the function to count frequency of letters in the dataframe
    # take dataframe and add sum of frequency of each letter in the row
    # and add it to the last column
    df_frequency = get_frequency_df()
    sum_frequency = []
    
    for column in df.columns[1:]:
        one_column_sum = 0
        for value in df[column]:
            # print(value)
            # one_column_sum += 
            print()

    
    pass
    
    
        