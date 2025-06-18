"""
aitsteg_functions.py
Functions for embedding and extracting a secret message using the AITSteg algorithm as implemented in the notebook.
"""
import math
import time

ZWC = {"00": '\u200C', "01": '\u202C', "10": '\u202D', "11": '\u200E'}
ZWC_reverse = {'\u200C': "00", '\u202C': "01", '\u202D': "10", '\u200E': "11"}

def get_factors(ni):
    return [i for i in range(1, ni+1) if (ni+1) % i == 0]

def get_alfa(factors, ni):
    natural_alphas = [math.log2(na) for na in factors if math.log2(na).is_integer()]
    return int(max(natural_alphas))

def my_xor(a, b, n):
    return ''.join('0' if a[i] == b[i] else '1' for i in range(n))

def embed_secret(SM, CM, MS_SK=111):
    """
    Embed a secret message SM into a cover message CM using the AITSteg algorithm.
    Optionally, provide MS_SK (int, 3 digits from current time by default).
    Returns the stego message (CM_HM).
    """
    if MS_SK is None:
        MS_SK = int(time.strftime("%H%M", time.localtime())[:3])
    MS_SK_bin = format(MS_SK, '08b')
    SM_binary = ''
    for letter in SM:
        ni = ord(letter)
        factors = get_factors(ni)
        alfa = get_alfa(factors, ni)
        beta = int((((ni + 1) / 2 ** alfa) - 1) / 2)
        alfa_bin = format(alfa, '06b')
        beta_bin = format(beta, '06b')
        bit_str = str(alfa_bin) + str(beta_bin)
        SM_binary += bit_str
    LSK = len(MS_SK_bin)
    LS = len(SM_binary)
    P = 0 if LS % LSK == 0 else 1
    NC = int(LS / LSK) + P
    hash_position_bits = NC * MS_SK_bin
    hashed_sm_binary = my_xor(SM_binary, hash_position_bits, LS)
    # Encode MS_SK_bin to ZWC
    HM_SK = ''
    i = 0
    while i < len(MS_SK_bin) - 1:
        x = MS_SK_bin[i:i+2]
        HM_SK += ZWC[x]
        i += 2
    # Encode hashed_sm_binary to ZWC
    HM_ZWC = ''
    i = 0
    while i < len(hashed_sm_binary) - 1:
        x = hashed_sm_binary[i:i+2]
        HM_ZWC += ZWC[x]
        i += 2
    HM = HM_SK + HM_ZWC
    CM_HM = CM[:-1] + HM + CM[-1]
    return CM_HM

def extract_secret(CM_HM, MR_SK=111):
    """
    Extract the secret message from a stego message CM_HM using the AITSteg algorithm.
    Optionally, provide MR_SK (int, 3 digits from current time by default).
    Returns the extracted secret message (SM_extract).
    """
    if MR_SK is None:
        MR_SK = int(time.strftime("%H%M", time.localtime())[:3])
    MR_SK_binary = '{0:08b}'.format(int(MR_SK))
    # Use the global ZWC_reverse directly (already correct)
    hashed_SM_binary_extract = ""
    for letter in CM_HM:
        if letter in ZWC_reverse:
            hashed_SM_binary_extract += ZWC_reverse[letter]
    MS_SK_extract = hashed_SM_binary_extract[0:8]
    SM_extract = ""
    if MS_SK_extract == MR_SK_binary:
        hashed_SM_binary_extract = hashed_SM_binary_extract[8:]
        LSK_extract = len(MR_SK_binary)
        P = 0 if (len(hashed_SM_binary_extract) % LSK_extract) == 0 else 1
        NC_extract = int((len(hashed_SM_binary_extract) / LSK_extract) + P)
        hash_position_bits_extract = NC_extract * MR_SK_binary
        SM_binary_extract = my_xor(hashed_SM_binary_extract, hash_position_bits_extract, len(hashed_SM_binary_extract))
        while len(SM_binary_extract) >= 12:
            alpha_beta = SM_binary_extract[0:12]
            SM_binary_extract = SM_binary_extract[12:]
            alpha_extract = alpha_beta[0:6]
            beta_extract = alpha_beta[6:12]
            alpha_final = int(alpha_extract, 2)
            beta_final = int(beta_extract, 2)
            n_final = ((pow(2, alpha_final) * (2 * beta_final + 1)) - 1)
            SM_extract = SM_extract + chr(n_final)
    return SM_extract