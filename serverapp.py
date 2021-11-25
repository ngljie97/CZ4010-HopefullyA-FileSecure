from backend import globals
import os, tqdm, socket

globals.init()

BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

if not os.path.exists(globals.SERVER_ROOT):
    os.makedirs(globals.SERVER_ROOT)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    try:
        s.bind((globals.SERVER_IP, globals.SERVER_PORT))
        s.listen(10)  # A maximum queue of 10 unaccepted request
        print(
            f"[*] Server started @ {globals.SERVER_IP}:{globals.SERVER_PORT}")

    except KeyboardInterrupt:
        s.close()

    while (True):
        conn, addr = s.accept()
        print(f"[+] {addr} has connected.")

        for i in range(0, 3):

            data_receive = ''

            while (True):
                data_receive += conn.recv(BUFFER_SIZE).decode('utf-8')
                if not data_receive:
                    break

            # receive from client socket
            request_type, user_id, file_name, file_size = data_receive.split(
                SEPARATOR)
            file_name = os.path.basename(file_name)
            # convert file size to integer
            file_size = int(file_size)

            if (request_type == "Upload"):
                progress = tqdm.tqdm(range(file_size),
                                     f"Receiving {file_name}",
                                     unit="B",
                                     unit_scale=True,
                                     unit_divisor=1024)

                dest_dir = os.path.join(globals.SERVER_ROOT, user_id)
                if not os.path.exists(dest_dir):
                    os.makedirs(dest_dir)
                bytes_read = ''
                with open(os.path.join(dest_dir, file_name), "wb") as f:
                    while (True):
                        # read data sent over
                        bytes_read = conn.recv(BUFFER_SIZE)
                        if not bytes_read:
                            break

                        # write to the file the bytes we just received
                        f.write(bytes_read)

                        # update the progress bar
                        progress.update(len(bytes_read))
                    progress.close()
                f.close()
                conn.send('success'.encode())

            elif (request_type == "Download"):
                progress = tqdm.tqdm(range(file_size),
                                     f"Sending {file_name}",
                                     unit="B",
                                     unit_scale=True,
                                     unit_divisor=1024)

                dest_dir = os.path.join(globals.SERVER_ROOT, user_id)
                file_path = os.path.join(dest_dir, file_name)
                file_size = int(os.path.getsize(file_path))
                bytes_read = ''
                with open(file_path, 'rb') as f:
                    while True:
                        bytes_read = f.read(BUFFER_SIZE)

                        # file transmitting is done
                        if not bytes_read:
                            break

                        # we use sendall to assure transimission in
                        # busy networks
                        conn.sendall(bytes_read)
                        # update the progress bar
                        progress.update(len(bytes_read))
                    progress.close()
                f.close()

        conn.close