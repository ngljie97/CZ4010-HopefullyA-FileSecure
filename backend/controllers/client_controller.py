import os
import socket
import tqdm
from backend.controllers.data_controller import DataManager
from backend.implementations.RSA import decryptRSA
from backend.implementations.aescipher import AESCipher
from backend.implementations.raid import Raid3Manager
from backend import globals

# Client - Basic functionalities

globals.init()

SEPARATOR = "<||>"
BUFFER_SIZE = 4096


class FileMeta(object):
    def __init__(self):
        self.uploader_id = ''
        self.uploader_name = ''
        self.file_name = ''
        self.file_size = ''
        self.remarks = ''
        self.timestamp = ''


# Sending file to server
def secure_send(input_file, enc_key):
    try:
        # Splice and introduce redundancy - using RAID3 concepts
        filesize = os.path.getsize(input_file)
        file_name = os.path.basename(input_file)
        raid = Raid3Manager(input_file=input_file, filesize=filesize)
        out_3paths = raid.compute_parity_hash()

        # Encrypt the 3-parts file, each with a different nonce
        trx_q = []  # queue for file transmission to the server
        crypt = AESCipher(enc_key)
        hashkey = crypt.getKeyHash()

        for file in out_3paths:
            trx_q.append(crypt.encrypt(file))
            del_file(file)
        crypt.destroy()
        crypt = ''

        # Create database entry
        display_name = globals.AUTH_USER['email'].split('@')[0]
        db_controller = DataManager()

        status = db_controller.insert_upload_entry(
            user_id=globals.AUTH_USER['localId'],
            file_name=file_name,
            file_size=filesize,
            display_name=display_name,
            hashedkey=hashkey)

        if status == 'FILE_EXIST':
            return 'File already exists in the server!'
        else:
            # Send the file to the server from the queue, trx_q
            # Send file to server for storage @Joel
            # Using trx_q[i] as file name
            request_type = "Upload"

            # Creating client socket
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                print(
                    f"[+] Attempting to send files to {globals.SERVER_IP}:{globals.SERVER_PORT}"
                )
                s.connect((globals.SERVER_IP, globals.SERVER_PORT))

                for file in trx_q:
                    user_id = globals.AUTH_USER['localId']
                    file_name = os.path.basename(file)
                    file_size = os.path.getsize(file)

                    s.send(
                        f"{request_type}{SEPARATOR}{user_id}{SEPARATOR}{file_name}{SEPARATOR}{file_size}"
                        .encode())

                    status = ''
                    while (status != 'READY'):
                        status = s.recv(5).decode()

                    progress = tqdm.tqdm(range(file_size),
                                         f"Sending {file_name}",
                                         unit="B",
                                         unit_scale=True,
                                         unit_divisor=1024)

                    with open(file, "rb") as f:

                        bytes_left = file_size
                        while bytes_left > 0:
                            # read data sent over
                            if (bytes_left < BUFFER_SIZE):
                                to_read = bytes_left
                            else:
                                to_read = BUFFER_SIZE

                            bytes_read = f.read(to_read)
                            bytes_left -= to_read

                            # send data to server
                            s.sendall(bytes_read)

                            # update the progress bar
                            progress.update(len(bytes_read))
                        progress.close()

                    del_file(file)
                s.send(f"Exit{SEPARATOR}0{SEPARATOR}0{SEPARATOR}0".encode())

        return 'Successfully uploaded file!'
    except:
        return 'Error occured!'


# Download the file, file_name, from server to chosen directory, dest_dir.
def secure_download(file, dest_dir):
    try:
        file_name, file_infos = file

        file_name = file_name.replace('<dot>', '.')
        filesize = file_infos['file_size']
        uploader_id = file_infos['uploader_id']

        # Receive 3 files from server to the dest_dir
        request_type = "Download"

        # Creating client socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            print(
                f"[+] Attempting to download files from {globals.SERVER_IP}:{globals.SERVER_PORT}"
            )
            s.connect((globals.SERVER_IP, globals.SERVER_PORT))

            for part_no in range(1, 4):
                part_name = file_name + '.p' + str(part_no) + '.enc'

                s.send(
                    f"{request_type}{SEPARATOR}{uploader_id}{SEPARATOR}{part_name}{SEPARATOR}0"
                    .encode())

                file_size = 0
                while (file_size == 0):
                    file_size = int(s.recv(10).decode())

                progress = tqdm.tqdm(range(file_size),
                                     f"Receiving {part_name}",
                                     unit="B",
                                     unit_scale=True,
                                     unit_divisor=1024)

                dest_file = os.path.join(dest_dir, part_name)

                with open(dest_file, "wb", buffering=0) as f:

                    bytes_left = file_size
                    while bytes_left > 0:
                        # read data sent over
                        if (bytes_left < BUFFER_SIZE):
                            to_read = bytes_left
                        else:
                            to_read = BUFFER_SIZE

                        bytes_read = s.recv(to_read)
                        bytes_left -= to_read

                        # write to the file the bytes we just received
                        f.write(bytes_read)

                        # update the progress bar
                        progress.update(len(bytes_read))
                    progress.close()

            # close the socket
            s.send(f"Exit{SEPARATOR}0{SEPARATOR}0{SEPARATOR}0".encode())

        # Exchange and decrypt the key for decryption
        key_name = globals.AUTH_USER['localId']
        dec_key = bytes.fromhex(file_infos['exchange_secret'])

        dec_key = (decryptRSA(key_name, dec_key)).decode()

        # Decrypt the 3-parts using the key obtained from the exchange
        crypt = AESCipher(dec_key)
        file = os.path.join(dest_dir, file_name)

        for i in range(1, 4):
            working_file = file + '.p' + str(i) + '.enc'
            crypt.decrypt(working_file)
            del_file(working_file)
        crypt.destroy()
        crypt = ''

        # Joins the 3 parts
        file_p1 = file + '.p1'
        raid = Raid3Manager(filesize=filesize, input_file=file_p1)
        raid.check_and_construct()

        for i in range(1, 4):
            del_file(file + '.p' + str(i))

        return 'Successfully downloaded file!'

    except:
        return 'Error occured downloading file.'


def request_download(file_meta):
    # Insert the download request to database.
    db_controller = DataManager()
    status = db_controller.insert_download_request(
        user_id=globals.AUTH_USER['localId'],
        file_name=file_meta.file_name,
        file_size=file_meta.file_size,
        remarks=file_meta.remarks,
        uploader_id=file_meta.uploader_id)

    return status


def get_all_files():
    db_controller = DataManager()
    return db_controller.get_all_files()


def get_file_requests():
    db_controller = DataManager()
    return db_controller.get_file_requests()


def get_dwnls():
    db_controller = DataManager()
    return db_controller.get_requested_files()


def del_file(file):
    if os.path.exists(file):
        os.remove(file)


def process_request(chosen_file, option, password):
    db_controller = DataManager()
    return db_controller.process_approval(chosen_file, option, password)


def start_client(file_name):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        s.connect((globals.SERVER_IP, globals.SERVER_PORT))
        for i in range(1, 4):  # Sending each part seperately to the server
            s.send(file_name + '.p' + str(i) + '.enc')

        # s.sendall(b'Hello, world') <- Send data to server
        # data = s.recv(1024) <- Receive from server
