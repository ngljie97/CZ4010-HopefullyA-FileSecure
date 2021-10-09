from backend import globals
from backend.authmanager import AuthManager
from frontend import client_view as view
import os

globals.init()
auth = AuthManager()

while (True):
    option = view.index_page()

    if option == '1':
        attmp = 3
        while (True):
            if attmp == 0:
                print(
                    'Too many failed attempts. Please sign up if you do not have an account.\nTerminating session...'
                )
                auth = 0
                exit()

            if attmp < 3:
                print('Login failed. Please try again.')

            email, password = view.cred_prompt()
            print(auth.signin(email=email, password=password))
            email, password = (0, 0)

            if len(globals.AUTH_USER) > 1:
                break
            else:
                attmp = attmp - 1

    elif option == '2':
        email, password = view.cred_prompt()
        print(auth.signup(email=email, password=password))
        email, password = (0, 0)
        input('Press enter to continue...')

    if len(globals.AUTH_USER) > 1:
        option = view.user_menu()

        if option == '1':
            file_location, passkey = view.upload_file_page()

        elif option == '2':
            view.dwload_file_page()
