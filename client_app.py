from backend import globals
from backend.controllers.auth_controller import AuthManager
from backend.controllers.client_controller import secure_download, secure_send
from frontend import client_view as view

globals.init()
auth = AuthManager()

while not globals.IS_AUTHENTICATED:
    option = view.index_page()

    if option == '1':
        attmp = globals.MAX_LOGIN_ATTEMPTS
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

            if globals.IS_AUTHENTICATED:
                break
            else:
                attmp = attmp - 1

    elif option == '2':
        email, password = view.cred_prompt()
        print(auth.signup(email=email, password=password))
        email, password = (0, 0)
        input('Press enter to continue...')

while globals.IS_AUTHENTICATED:

    option = view.user_menu()

    if option == '1':
        file_location, passkey = view.upload_file_page()
        secure_send(file_location, passkey)
        input('Press enter to continue...')

    elif option == '2':
        file_name, dest_dir = view.dwload_file_page()
        secure_download(file_name, dest_dir)
        input('Press enter to continue...')

    elif option == '3':
        #do something
        print()

    elif option == '4':
        auth.signout()
