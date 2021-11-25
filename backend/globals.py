import os

from pyrebase import pyrebase


def init():
    global PROJ_ROOT
    global AUTH_USER
    global SERVER_IP
    global SERVER_PORT
    global SERVER_ROOT
    global IS_AUTHENTICATED
    global MAX_LOGIN_ATTEMPTS
    global FIREBASE_CONN

    # Basic variables initialization for program to run
    PROJ_ROOT = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
    __PATH_TO_KEY = os.path.join(PROJ_ROOT, 'backend', 'secret',
                                 'firebase-privatekey.json')
    MAX_LOGIN_ATTEMPTS = 3
    AUTH_USER = {}
    IS_AUTHENTICATED = False
    SERVER_IP = '192.168.99.121'
    SERVER_PORT = 65432
    SERVER_ROOT = '/home/cz4010fs/'

    FIREBASE_CONN = pyrebase.initialize_app({
        "apiKey": "AIzaSyBd9GRTbL_lIZyJtpQkUfvGwfXmzwuDszc",
        "authDomain": "cz4010fs.firebaseapp.com",
        "databaseURL":
        "https://cz4010fs-default-rtdb.asia-southeast1.firebasedatabase.app/",
        "storageBucket": "cz4010fs.appspot.com",
        "serviceAccount": __PATH_TO_KEY
    })
