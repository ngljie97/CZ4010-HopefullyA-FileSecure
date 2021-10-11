from os import name, write
import socket

from backend.globals import SERVER_IP, SERVER_PORT

server_dir = 'C:\Users\Joel Ng\Documents\GitHub\CZ4010\CZ4010\backend\server'

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((SERVER_IP, SERVER_PORT))
        s.listen()
        data_chunk = ''
        conn, addr = s.accept()
        
        file_name = 'test.txt' # retrieve from database
        file_size = 0 # retrieve from database
        file = '\\' + file_name
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024) # receive according to file size / 2
                # Store the data received in chunks
                with open(data, 'rb') as x:     
                    for chunk in iter(lambda: x.read(4096), b""):
                        data_chunk.update(chunk)
                
                # Directly flushing data to the file
                with open(server_dir.append(file), 'wb', buffering = 0) as f:
                    f.write(data_chunk)
                

                if not data:
                    break
                # conn.sendall(data) <- to send data over to client
                
