import os


# XOR the entire array of bytes, byte by byte
def bytewise_xor(bytes1, bytes2):
    result_bytes = bytearray()

    for (a, b) in zip(bytes1, bytes2):
        result_bytes.append(a ^ b)

    return result_bytes


def compute_parity(enc_file):  # Function to compute the "parity file"
    filesize = len(enc_file)
    half = int(filesize / 2)

    share1 = enc_file[0:half]
    share2 = enc_file[half:]

    return bytewise_xor(share1, share2)


def repair_from(p1, p2):  # Function to repair broken down file
    return bytewise_xor(p1, p2)
