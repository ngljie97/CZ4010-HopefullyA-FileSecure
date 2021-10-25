from os import name, write
import socket
import tqdm
import os
from backend import globals as globals
from backend.globals import SERVER_IP, SERVER_PORT

server_dir = globals.PROJ_ROOT + '\\backend\\server\\'

def start_server():
    BUFFER_SIZE = 4096
    SEPARATOR = "<SEPERATOR>"
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((SERVER_IP, SERVER_PORT))
        s.listen(4) # A maximum queue of 4 unaccepted request
        print(f"[*] Listening as {SERVER_IP}:{SERVER_PORT}")        
        conn, addr = s.accept()
        print(f"[+] {addr} is connected.")

        # receive file information
        data_receive = conn.recv(BUFFER_SIZE).decode()
        file_name, file_size = data_receive.split(SEPARATOR) # receive from client socket

        # remove absolute path to prevent exceptions
        file_name = os.path.basename(file_name)

        # convert file size to integer 
        file_size = int(file_size)

        # start receiving the file from the socket
        # and writing to the file stream
        progress = tqdm.tqdm(range(file_size), f"Receiving {file_name}", unit="B", unit_scale=True, unit_divisor=1024)
        with open(server_dir+file_name, "wb") as f:
            while True:
                # read 1024 bytes from the socket (receive)
                bytes_read = conn.recv(BUFFER_SIZE)
                if not bytes_read:    
                    # nothing is received
                    # file transmittion is done
                    break
                # write to the file the bytes we just received
                f.write(bytes_read)
                # update the progress bar
                progress.update(len(bytes_read))

        # close the client socket
        conn.close()
        # close the server socket
        s.close()

        ### Previous code ###        
        # with conn:
        #     print('Connected by', addr)
        #     while True:
        #         data = conn.recv(1024) # receive according to file size / 2
        #         # Store the data received in chunks
        #         with open(data, 'rb') as x:     
        #             for chunk in iter(lambda: x.read(4096), b""):
        #                 data_chunk.update(chunk)
                
        #         # Directly flushing data to the file
        #         with open(server_dir.append(file), 'wb', buffering = 0) as f:
        #             f.write(data_chunk)
                

        #         if not data:
        #             break
        #         # conn.sendall(data) <- to send data over to client
                
