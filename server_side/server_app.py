import os, tqdm, socket

SERVER_PORT = 65432
SERVER_ROOT = '/home/cz4010fs'
SERVER_IP = '0.0.0.0'
BUFFER_SIZE = 4096
SEPARATOR = "<||>"

if not os.path.exists(SERVER_ROOT):
    os.makedirs(SERVER_ROOT)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    s.bind((SERVER_IP, SERVER_PORT))
    s.listen(10)  # A maximum queue of 10 unaccepted request
    print(f"[*] Server started @ {SERVER_IP}:{SERVER_PORT}")

    while True:
        try:
            print(f"[*] Waiting for connection...")
            conn, addr = s.accept()
            print(f"[+] {addr} has connected.")
        except KeyboardInterrupt:
            s.close()

        while True:
            data_receive = conn.recv(BUFFER_SIZE).decode()

            request_type, user_id, file_name, file_size = data_receive.split(
                SEPARATOR)

            # convert file size to integer
            file_size = int(file_size)

            if (request_type == 'Upload'):
                conn.send('READY'.encode())

                progress = tqdm.tqdm(range(file_size),
                                     f"Receiving {file_name}",
                                     unit="B",
                                     unit_scale=True,
                                     unit_divisor=1024)

                dest_dir = os.path.join(SERVER_ROOT, user_id)
                if not os.path.exists(dest_dir):
                    os.makedirs(dest_dir)

                with open(os.path.join(dest_dir, file_name), "wb",
                          buffering=0) as f:
                    bytes_left = file_size
                    while bytes_left > 0:
                        # read data sent over
                        if (bytes_left < BUFFER_SIZE):
                            to_read = bytes_left
                        else:
                            to_read = BUFFER_SIZE

                        bytes_read = conn.recv(to_read)
                        bytes_left -= to_read

                        # write to the file the bytes we just received
                        f.write(bytes_read)

                        # update the progress bar
                        progress.update(len(bytes_read))
                    progress.close()

            elif (request_type == 'Download'):
                src_dir = os.path.join(SERVER_ROOT, user_id)
                file_path = os.path.join(src_dir, file_name)
                file_size = int(os.path.getsize(file_path))

                conn.send(str(file_size).encode())

                progress = tqdm.tqdm(range(file_size),
                                     f"Sending {file_name}",
                                     unit="B",
                                     unit_scale=True,
                                     unit_divisor=1024)

                with open(file_path, 'rb') as f:

                    bytes_left = file_size
                    while bytes_left > 0:
                        # read data sent over
                        if (bytes_left < BUFFER_SIZE):
                            to_read = bytes_left
                        else:
                            to_read = BUFFER_SIZE

                        bytes_read = f.read(BUFFER_SIZE)
                        bytes_left -= to_read

                        # send data over
                        conn.sendall(bytes_read)

                        # update the progress bar
                        progress.update(len(bytes_read))
                    progress.close()

            elif (request_type == 'Exit'):
                print(f"[+] {addr} has disconnected.")
                conn.close()
                break