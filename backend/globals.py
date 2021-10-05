import os


def init():
    global PROJ_ROOT
    global USER_TOKEN
    global SERVER_IP
    global SERVER_PORT

    PROJ_ROOT = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
    USER_TOKEN = '0x0000000000'
    SERVER_IP = '127.0.0.1'
    SERVER_PORT = 65432
