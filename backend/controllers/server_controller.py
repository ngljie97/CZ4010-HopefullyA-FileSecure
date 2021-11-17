from os import name, write
import socket
import tqdm
import os
# from CZ4010.backend.globals import SERVER_IP, SERVER_PORT
from backend import globals
# from backend.globals import SERVER_IP, SERVER_PORT


def start_server():
    SERVER_IP = globals.SERVER_IP
    SERVER_PORT = globals.SERVER_PORT
    BUFFER_SIZE = 4096
    SEPARATOR = "<SEPARATOR>"
    server_dir = 'C:\\CZ4010\\backend\\server\\'
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((SERVER_IP, SERVER_PORT))
        s.listen(10)  # A maximum queue of 10 unaccepted request
        print(f"[*] Listening as {SERVER_IP}:{SERVER_PORT}")
        conn, addr = s.accept()
        print(f"[+] {addr} is connected.")
        
        while True:
            # receive file information
            data_receive = conn.recv(BUFFER_SIZE).decode('utf-8')
            if not data_receive:
                break
            request_type, file_name, file_size = data_receive.split(SEPARATOR)  # receive from client socket        
           

            if (request_type == "Upload"):
                 # remove absolute path to prevent exceptions
                file_name = os.path.basename(file_name)

                # convert file size to integer
                file_size = int(file_size)
                chunk_size = 4096
                while file_size > 0:
                    if file_size < chunk_size:
                        chunk_size = file_size                                    
                    # start receiving the file from the socket
                    # and writing to the file stream
                    progress = tqdm.tqdm(range(
                        file_size), f"Receiving {file_name}", unit="B", unit_scale=True, unit_divisor=1024)
                    with open(server_dir+file_name, "wb") as f:
                        # while True:
                            # read 1024 bytes from the socket (receive)
                        bytes_read = conn.recv(chunk_size)
                        # if not bytes_read:
                        #     # if nothing is received
                        #     # file transmittion is complete
                        #     break
                        # write to the file the bytes we just received
                        f.write(bytes_read)
                        # update the progress bar
                        progress.update(len(bytes_read))
                    file_size -= len(bytes_read)
                    
                f.close()
            

            elif (request_type == "Download"):
                # reqFile = conn.recv(1024)
                # if not reqFile:
                #     break
                # file_name = reqFile.decode()
                
                progress = tqdm.tqdm(range(
                    file_size), f"Sending {file_name}", unit="B", unit_scale=True, unit_divisor=1024)
                with open(server_dir+file_name, 'rb') as f:
                    # while True:
                    for bytes_read in f:

                        # bytes_read = f.read(BUFFER_SIZE)
                        # if not bytes_read:
                            # file transmitting is done
                            # break
                        # we use sendall to assure transimission in
                        # busy networks
                        conn.sendall(bytes_read)
                        # update the progress bar
                        progress.update(len(bytes_read))
                    
        # close the socket
        # conn.close()
        # s.close()



          
