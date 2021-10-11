import os


def init():
    global PROJ_ROOT
    global AUTH_USER
    global SERVER_IP
    global SERVER_PORT
    global IS_AUTHENTICATED
    global MAX_LOGIN_ATTEMPTS

    # Basic variables initialization for program to run
    PROJ_ROOT = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
    MAX_LOGIN_ATTEMPTS = 3
    AUTH_USER = {}
    IS_AUTHENTICATED = False
    SERVER_IP = '127.0.0.1'
    SERVER_PORT = 65432
