import time
from backend import globals
from frontend import client_view as view

globals.init()

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
                    input('Press ENTER to continue...')
                    break

                if attmp < 3:
                    print('Login failed. Please try again.')

                view.cred_prompt('signin')

                if globals.IS_AUTHENTICATED:
                    input('Press ENTER to continue...')
                    break
                else:
                    attmp -= 1

        elif option == '2':
            view.cred_prompt('signup')
            input('Press ENTER to continue...')

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
            view.signout_page()

        else:
            input('Invalid option. Press ENTER to continue...')
