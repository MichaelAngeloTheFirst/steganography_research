import pandas as pd

ZWC = ("\u200c", "\u202c", "\u202d", "\u200e")

# Decode a pair of ZWC characters to a column index
def decode_zwc_to_col(zwc_pair):
    zwc_list = list(ZWC)
    first, second = zwc_pair
    return zwc_list.index(first) * 4 + zwc_list.index(second)

# Extract secret message from carrier message
# Looks for ZWC pairs before a character, decodes which row and col, and gets the letter

def extract_secret_from_carrier(stego, file_path= "./unique_array.csv"):
    df = pd.read_csv(file_path)
    
    df = df.iloc[:26, :8]
    unique_array = df.values.tolist()

    zwc_set = set(ZWC)
    i = 0
    secret = []
    while i < len(stego):
        if i+2 <= len(stego) and stego[i] in zwc_set and stego[i+1] in zwc_set:
            zwc_pair = stego[i] + stego[i+1]
            col = decode_zwc_to_col(zwc_pair)
            c = stego[i+2]
            # Find which row this character is in for this column
            for row in range(26):
                
                if unique_array[row][col] == c:
                    secret.append(chr(ord('a') + row))
                    break
            i += 3
        else:
            i += 1
    return ''.join(secret)

# Helper to load unique_array as a 2D list