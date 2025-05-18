import pandas as pd


ZWC = ("\u200c", "\u202c", "\u202d", "\u200e")
zw_space = "\u200b"
zw_non_joiner = "\u200c"
zw_joiner = "\u200d"
zw_no_break_space = "\ufeff"


# function to import unique array
def import_unique_array(file_path):
    try:
        df = pd.read_csv(file_path)
        unique_array = df.iloc[:, 0].unique()
        # add index to unique array

        return unique_array
    except Exception as e:
        print(f"Error reading file: {e}")
        return None


if __name__ == "__main__":
    # Example usage
    secret_message = "This is a hidden message."
    carrier_message = "This is the visible part of the message."

    message = f"Hello,{zw_joiner} World !"
    print("Original message:", message)
