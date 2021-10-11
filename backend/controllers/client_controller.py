import os
import socket

from Crypto.Cipher import AES
from backend.implementations.aescipher import AESCipher
from backend.globals import SERVER_IP, SERVER_PORT, USER_TOKEN
from backend.implementations.raid import Raid3Manager

# Client - Basic functionalities


# Sending file to server
def secure_send(input_file, enc_key):

    ## Splice and introduce redundancy - using RAID3 concepts
    filesize = os.path.getsize(input_file)
    raid = Raid3Manager(input_file=input_file, filesize=filesize)
    out_3paths = raid.compute_parity_hash()

    ## Encrypt the 3-parts file, each with a different nonce
    trx_q = []  # queue for file transmission to the server
    crypt = AESCipher(enc_key)
    for file in out_3paths:
        trx_q.append(crypt.encrypt(file))
        if os.path.exists(file):
            os.remove(file)

    ## Send the file to the server from the queue, trx_q
    ### To be implemented (server should store userid, filesize, 3-part encrypted file)

    ### Create database entry
    ### Send file to server for storage

    return 0


# Download the file, file_name, from server to chosen directory, dest_dir.
def secure_download(file_name, dest_dir, prikey_dir):

    ## Receive 3 files from server to the dest_dir
    ### To be implemented

    ## Retrieve file information from database
    filesize = 99
    host_user = ''
    host_pubkey = ''

    ## Exchange and decrypt the key for decryption
    dec_key = ''

    ## Decrypt the 3-parts using the key obtained from the exchange
    crypt = AESCipher(dec_key)
    file = os.path.join(dest_dir, file_name)

    for i in range(1, 4):
        crypt.decrypt(file + '.p' + str(i) + '.enc')

    ## Joins the 3 parts
    file_p1 = file + '.p1'
    raid = Raid3Manager(filesize=filesize, input_file=file_p1)
    raid.check_and_construct()
    return 0


def start_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((SERVER_IP, SERVER_PORT))
        # s.sendall(b'Hello, world') <- Send data to server
        # data = s.recv(1024) <- Receive from server
