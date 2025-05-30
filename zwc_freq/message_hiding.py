import pandas as pd
import string


ZWC = ("\u200c", "\u202c", "\u202d", "\u200e")
zw_space = "\u200b"
zw_non_joiner = "\u200c"
zw_joiner = "\u200d"
zw_no_break_space = "\ufeff"


# Encode a column index (0-7) as a pair of ZWC characters
# 0-3: zwc1, 4-7: zwc2, etc. (00, 01, 02, 03, 10, 11, 12, 13)
def encode_col_to_zwc(col):
    zwc_list = list(ZWC)
    first = zwc_list[col // 4]
    second = zwc_list[col % 4]
    return first + second

# Decode a pair of ZWC characters to a column index
def decode_zwc_to_col(zwc_pair):
    zwc_list = list(ZWC)
    first, second = zwc_pair
    return zwc_list.index(first) * 4 + zwc_list.index(second)

# Hide secret message in carrier message 
# Each secret letter is hidden in the first matching carrier letter (row),
# with a ZWC pair before it encoding the column

def hide_secret_in_carrier(secret, carrier, unique_array):
    carrier = list(carrier)
    used = [False] * len(carrier)
    secret = [c.lower() for c in secret if c.lower() in string.ascii_lowercase]
    carrier_len = len(carrier)
    last_used_idx = -1
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

# Extract secret message from carrier message
# Looks for ZWC pairs before a character, decodes which row and col, and gets the letter

def extract_secret_from_carrier(stego, unique_array):
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

def load_unique_array(file_path):
    df = pd.read_csv(file_path)
    df = df.iloc[:26, :8]
    return df.values.tolist()


if __name__ == "__main__":
    # Example 1: Hide a short secret in a pangram carrier
    unique_array = load_unique_array("unique_array.csv")
    secret_message1 = "hidden"
    carrier_message1 = "the quick brown fox jumps over the lazy dog"
    stego1 = hide_secret_in_carrier(secret_message1, carrier_message1, unique_array)
    print("Example 1:")
    print("Carrier:", carrier_message1)
    print("Secret:", secret_message1)
    print("Stego:", stego1)
    print("Extracted:", extract_secret_from_carrier(stego1, unique_array))
    print()

    # Example 2: Hide a longer secret in a repeated carrier
    secret_message2 = "steganographyisfun"
    carrier_message2 = "lorem ipsum dolor sit amet consectetur adipiscing elit lorem ipsum dolor sit amet"
    stego2 = hide_secret_in_carrier(secret_message2, carrier_message2, unique_array)
    print("Example 2:")
    print("Carrier:", carrier_message2)
    print("Secret:", secret_message2)
    print("Stego:", stego2)
    print("Extracted:", extract_secret_from_carrier(stego2, unique_array))
