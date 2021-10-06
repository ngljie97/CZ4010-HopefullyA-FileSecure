import socket
from backend.globals import SERVER_IP, SERVER_PORT, USER_TOKEN

# Client - Basic functionalities


def secure_send(file):  # To send a file to the server
    # do something
    return 0


def secure_download(file_name):  # To download a file from the server
    # do something
    return 0


def start_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((SERVER_IP, SERVER_PORT))
        # s.sendall(b'Hello, world') <- Send data to server
        # data = s.recv(1024) <- Receive from server
