import socket
from backend.globals import SERVER_IP, SERVER_PORT, USER_TOKEN

# Client - Basic functionalities


def login(credentials):
    # do something
    global USER_TOKEN

    auth_token = ''
    USER_TOKEN = auth_token

    return 1


def logout():
    global USER_TOKEN

    USER_TOKEN = '0x0000000000'
    return -1


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
