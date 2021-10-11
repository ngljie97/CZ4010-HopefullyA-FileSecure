import os
import socket

from backend.implementations.aescipher import AESCipher
from backend.implementations.raid import Raid3Manager
from backend import globals

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
        del_file(file)
    crypt.destroy()
    crypt = ''

    ## Send the file to the server from the queue, trx_q
    ### To be implemented (server should store userid, filesize, 3-part encrypted file)

    ### Create database entry
    ### Send file to server for storage

    return 0


# Download the file, file_name, from server to chosen directory, dest_dir.
def secure_download(file_name, dest_dir):

    ## Receive 3 files from server to the dest_dir
    ### To be implemented

    ## Retrieve file information from database
    filesize = 199
    host_user = ''
    host_pubkey = ''

    ## Exchange and decrypt the key for decryption
    dec_key = '123asd123!'

    ## Decrypt the 3-parts using the key obtained from the exchange
    crypt = AESCipher(dec_key)
    file = os.path.join(dest_dir, file_name)

    for i in range(1, 4):
        working_file = file + '.p' + str(i) + '.enc'
        crypt.decrypt(working_file)
        del_file(working_file)
    crypt.destroy()
    crypt = ''

    ## Joins the 3 parts
    file_p1 = file + '.p1'
    raid = Raid3Manager(filesize=filesize, input_file=file_p1)
    raid.check_and_construct()
    return 0


def del_file(file):
    if os.path.exists(file):
        os.remove(file)


def start_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((globals.SERVER_IP, globals.SERVER_PORT))
        # s.sendall(b'Hello, world') <- Send data to server
        # data = s.recv(1024) <- Receive from server
