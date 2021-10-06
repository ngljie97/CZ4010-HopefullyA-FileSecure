import os


def init():
    global PROJ_ROOT
    global AUTH_USER
    global SERVER_IP
    global SERVER_PORT

    PROJ_ROOT = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
    AUTH_USER = {}
    SERVER_IP = '127.0.0.1'
    SERVER_PORT = 65432
