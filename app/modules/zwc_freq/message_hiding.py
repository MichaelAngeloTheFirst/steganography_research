from json import load
import pandas as pd
import string

#available zwc characters
ZWC = ("\u200c", "\u202c", "\u202d", "\u200e")


# Encode a column index (0-7) as a pair of ZWC characters
# 0-3: zwc1, 4-7: zwc2, etc. (00, 01, 02, 03, 10, 11, 12, 13)
def encode_col_to_zwc(col):
    zwc_list = list(ZWC)
    first = zwc_list[col // 4]
    second = zwc_list[col % 4]
    return first + second


# Hide secret message in carrier message 
# Each secret letter is hidden in the first matching carrier letter (row),
# with a ZWC pair before it encoding the column

def hide_secret_in_carrier(secret, carrier, file_path = "./unique_array.csv"):
    #load unique array
    df = pd.read_csv(file_path)
    df = df.iloc[:26, :8]
    unique_array =df.values.tolist()
    #-------------------------------
    
    carrier = list(carrier)
    used = [False] * len(carrier)
    secret = [c.lower() for c in secret if c.lower() in string.ascii_lowercase]
    carrier_len = len(carrier)
    last_used_idx = -1
    #--------------------------
    for s in secret:
        row = ord(s) - ord('a')
        found = False
        # Only search forward from the last used index to preserve order
        for i in range(last_used_idx + 1, carrier_len):
            if used[i]:
                continue
            c = carrier[i]
            # Check if this carrier letter is present in the unique array row for this secret letter
            for col in range(8):
                if unique_array[row][col] == c:
                    zwc_pair = encode_col_to_zwc(col)
                    # Insert ZWC pair before the carrier character (hide secret)
                    carrier[i] = zwc_pair + c
                    used[i] = True
                    found = True
                    last_used_idx = i
                    break
            if found:
                break
        if not found:
            print(f"Cannot hide letter '{s}' in carrier message at position {last_used_idx+1} or later: no suitable character found while preserving order.")
            return None
    return ''.join(carrier)
