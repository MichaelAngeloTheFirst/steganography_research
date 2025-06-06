from zwc_freq.message_finding import extract_secret_from_carrier
from zwc_freq.message_hiding import hide_secret_in_carrier


if __name__ == "__main__":
    # Example 1: Hide a short secret in a pangram carrier
    # secret_message1 = "hidden"
    # carrier_message1 = "the quick brown fox jumps over the lazy dog"
    # stego1 = hide_secret_in_carrier(secret_message1, carrier_message1, )
    # print("Example 1:")
    # print("Carrier:", carrier_message1)
    # print("Secret:", secret_message1)
    # print("Stego:", stego1)
    # print("Extracted:", extract_secret_from_carrier(stego1, ))
    # print()

    # Example 2: Hide a longer secret in a repeated carrier
    secret_message2 = "secret"
    carrier_message2 = "hello world, you can see whats hidden in here"
    stego2 = hide_secret_in_carrier(secret_message2, carrier_message2, './zwc_freq/unique_array.csv')
    print("Example 2:")
    print("Carrier:", carrier_message2)
    print("Secret:", secret_message2)
    print("Stego:", stego2)
    print("Extracted:", extract_secret_from_carrier(stego2, './zwc_freq/unique_array.csv'))
