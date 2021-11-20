import os
import socket
import tqdm
from backend.controllers.data_controller import DataManager
from backend.implementations.RSA import decryptRSA
from backend.implementations.aescipher import AESCipher
from backend.implementations.raid import Raid3Manager
from backend import globals
# from backend.globals import SERVER_IP, SERVER_PORT

# Client - Basic functionalities

globals.init()


class FileMeta(object):
    def __init__(self):
        self.uploader_id = ''
        self.uploader_name = ''
        self.file_name = ''
        self.file_size = ''
        self.remarks = ''


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
            host = globals.SERVER_IP
            port = globals.SERVER_PORT
            SEPARATOR = "<SEPARATOR>"
            BUFFER_SIZE = 4096
            check = 'success'
            i=0
            # Creating client socket
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                print(f"[+] Attempting to send files to {host}:{port}")
                s.connect((host, port))

                # for i in trx_q:
                while True:

                    filesize = os.path.getsize(trx_q[i])
                    if check=='success':
                        check = 'fail'                        
                        s.send(f"{request_type}{SEPARATOR}{os.path.basename(trx_q[i])}{SEPARATOR}{filesize}".encode('utf-8'))

                        progress = tqdm.tqdm(range(
                            filesize), f"Sending {os.path.basename(trx_q[i])}", unit="B", unit_scale=True, unit_divisor=1024)
                        with open(trx_q[i], "rb") as f:
                            while True:
                                # read the bytes from the file
                                bytes_read = f.read(BUFFER_SIZE)
                                if not bytes_read:
                                    # file transmitting is done
                                    break
                                # we use sendall to assure transimission in
                                # busy networks                                                      
                                s.sendall(bytes_read)
                                # update the progress bar
                                progress.update(len(bytes_read))
                                
                        i+=1

                    if i>2:
                        break
                    else:
                        try: 
                            check = s.recv(1024).decode() 
                        except:
                            check = 'fail'                  

                    # close the socket
                    # s.send()
                    # s.close()
            
            return 'Successfully uploaded file!'

    except:
        return 'Error occured!'


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


# Download the file, file_name, from server to chosen directory, dest_dir.
def secure_download(file, dest_dir):
    try:
        db_controller = DataManager()

        file_name, file_infos = file

        file_name = file_name[:-4] + '.' + file_name[-3:]
        filesize = file_infos['file_size']

        # Receive 3 files from server to the dest_dir
        # To be implemented @Joel
        file = os.path.join(dest_dir, file_name)
        request_type = "Download"
        host = globals.SERVER_IP
        port = globals.SERVER_PORT
        SEPARATOR = "<SEPARATOR>"
        BUFFER_SIZE = 4096

        # Creating client socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            print(f"[+] Attempting to download files")
            s.connect((host, port))
            for i in range(1, 4):
                s.send(f"{request_type}{SEPARATOR}{file_name+'.p'+str(i)+'.enc'}{SEPARATOR}{filesize}".encode())
                file_path = os.path.join(dest_dir,file_name+'.p'+str(i)+'.enc')
                progress = tqdm.tqdm(range(
                    filesize), f"Receiving {file_name+'.p'+str(i)+'.enc'}", unit="B", unit_scale=True, unit_divisor=1024)
                with open(file_path, "wb") as f:
                    while True:
                        # read the bytes from the file

                        bytes_read = s.recv(BUFFER_SIZE)
                        if not bytes_read:
                            # file transmitting is done
                            break
                        # we use sendall to assure transimission in
                        # busy networks
                        f.write(bytes_read)
                        # update the progress bar
                        progress.update(len(bytes_read))
            # close the socket
        #     s.send()
            s.close()
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

        return 'Successfully downloaded file!'

    except:
        return 'Error occured downloading file.'


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
