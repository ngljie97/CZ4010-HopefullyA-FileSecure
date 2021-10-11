import os
import socket
from backend.implementations.aescipher import AESCipher
from backend.globals import SERVER_IP, SERVER_PORT, USER_TOKEN
from backend.implementations.raid import Raid3Manager

# Client - Basic functionalities


def secure_send(input_file, enc_key):  # To send a file to the server

    # Splice and introduce redundancy - using RAID3 concepts
    filesize = os.path.getsize(input_file)
    raid = Raid3Manager(input_file=input_file, filesize=filesize)
    out_3paths = raid.compute_parity_hash()

    # Encrypt the 3-parts file, each with a different nonce
    trx_q = []  # queue for file transmission to the server
    crypt = AESCipher(enc_key)
    for file in out_3paths:
        trx_q.append(crypt.encrypt(file))

    # Send the file to the server from the queue, trx_q
    ### To be implemented

    return 0


def secure_download(file_name, dest_dir):  # To download a file from the server

    # Download the file, file_name, from server to chosen directory, dest_dir
    ### To be implemented

    
    return 0


def start_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((SERVER_IP, SERVER_PORT))
        # s.sendall(b'Hello, world') <- Send data to server
        # data = s.recv(1024) <- Receive from server
