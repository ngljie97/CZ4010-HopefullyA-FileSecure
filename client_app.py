import time
from backend import globals
from backend.controllers.auth_controller import AuthManager
from frontend import client_view as view

globals.init()
auth = AuthManager()
while True:
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

                time.sleep(2)

                if globals.IS_AUTHENTICATED:
                    break
                else:
                    attmp = attmp - 1

        elif option == '2':
            email, password = view.cred_prompt()
            print(auth.signup(email=email, password=password))
            email, password = (0, 0)
            input('Press enter to continue...')

        elif option == '3':
            exit()

    while globals.IS_AUTHENTICATED:

        option = view.user_menu()

        if option == '1':
            view.upload_file_page()

        elif option == '2':
            view.request_file_page()

        elif option == '3':
            view.dwnl_reqst_page()

        elif option == '4':
            view.dwload_file_page()

        elif option == '5':
            auth.signout()
