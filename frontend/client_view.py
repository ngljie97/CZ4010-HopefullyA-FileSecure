# Console base client application view
# To process data output and input

import os
import time
from getpass import getpass
from datetime import datetime

from backend import globals
from backend.controllers.auth_controller import AuthManager
from backend.implementations.input_validator import check_email, check_file, check_password
from backend.controllers.client_controller import get_dwnls, get_all_files, FileMeta, request_download, get_file_requests, process_request, secure_download, secure_send

from prettytable import PrettyTable

auth = AuthManager()


def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)


def index_page():
    clearConsole()
    print(' Welcome to CZ4010FileSecure Sharing platform!')
    print('===============================================')
    print('What would you like to do?')
    print('1. Log-in')
    print('2. Sign-up')
    print('3. Exit')
    return input('Enter your choice:\t')


def cred_prompt(op_type):
    user_email = input('Enter your email:\t')
    if check_email(user_email):
        user_passw = getpass('Enter your password:\t')

        if check_password(user_passw):
            if op_type == 'signin':
                print(auth.signin(email=user_email, password=user_passw))
            elif op_type == 'signup':
                print(auth.signup(email=user_email, password=user_passw))


def user_menu():
    clearConsole()
    user = globals.AUTH_USER['email']
    print(f'Logged in as: {user}')
    print('1. Upload a file.')
    print('2. Request file download.')
    print('3. Approve download requests.')
    print('4. View downloadable files.')
    print('5. Logout.')
    return input('Enter your choice:\t')


def upload_file_page():
    clearConsole()
    print('=-=-=-=-=-=-=-=-| File Upload |-=-=-=-=-=-=-=-=')

    file_location = input(
        'Enter the absolute path to the file. (e.g. C:/path/to/file.txt):\n'
    ).strip('"')
    if check_file(file_location):
        print(
            'Enter a passkey for encryption. Please keep the key safe and secure. Do not let anyone else know the key.\n This key will not be stored in the server so do not lose it.'
        )
        encryption_key = input('Passkey:\t')
        print(secure_send(file_location, encryption_key))

    input('Press ENTER to continue...')


def request_file_page():
    clearConsole()
    print('=-=-=-=-=-=-=-=-| Download a file |-=-=-=-=-=-=-=-=\n')

    try:
        entries = get_all_files()

        data = []
        i = 1
        file_table = PrettyTable(
            ['No.', 'File Name', 'Uploaded by', 'Uploaded on'])

        for user, files in entries.items():
            for file_name, file_info in files.items():
                file = FileMeta()
                file.file_name = file_name.replace('<dot>', '.')
                file.uploader_id = user
                file.uploader_name = file_info['display_name']
                file.file_size = file_info['filesize']
                file.timestamp = datetime.fromisoformat(
                    file_info['timestamp']).strftime("%d/%m/%Y")

                data.append(file)
                file_table.add_row(
                    [i, file.file_name, file.uploader_name, file.timestamp])

                i += 1

        if len(data) > 0:
            print(file_table)
            select = input(
                'Enter the number for the file to download (q to quit):\t')

            try:
                if select.upper() == 'Q':
                    input('Operation cancelled. Press ENTER to continue...')
                    return 0

                select = int(select)
            except ValueError:
                input('Invalid input. Press ENTER to continue...')

            if 0 <= (select - 1) < len(data):
                selected_file = data[select - 1]
                remarks = input(
                    'Enter a message to display for the owner of the file to approve your resquest (WARNING: do not enter any personal information/credentials):\n'
                )
                selected_file.remarks = remarks
                print(request_download(selected_file))
                input('Press ENTER to continue...')
        else:
            input('No files to download. Press ENTER to continue..')
    except:
        return 0


def dwnl_reqst_page():
    clearConsole()
    print('=-=-=-=-=-=-=-=-| File Approval |-=-=-=-=-=-=-=-=')

    try:
        entries = get_file_requests()

        if len(entries) > 0:
            req_table = PrettyTable(
                ['No.', 'File name', 'Requested by', 'Approval Status'])

            i = 1
            for entry in entries:
                file_name = entry['file_name'].replace('<dot>', '.')
                req_display_name = entry['req_display_name']
                approval_status = entry['approval_status']
                req_table.add_row(
                    [str(i), file_name, req_display_name, approval_status])

                i += 1

            print(req_table)

            while True:
                sel = input(
                    'Enter a file number for more options: (Enter q to return to main menu)\t'
                )
                try:
                    if sel.upper() == 'Q':
                        return 0
                    sel = int(sel)
                    break
                except ValueError:
                    print('Invalid input...')

            if 0 <= int(sel) - 1 < len(entries):
                message = file_submenu(entries[int(sel) - 1])
                if message == 'SUCCESS':
                    input(
                        'The requests has been approved. Press ENTER to continue...'
                    )
                elif message == 'REJECTED':
                    input(
                        'The requests has been rejected. Press ENTER to continue...'
                    )
                elif message == 'WRONG_PASSWORD':
                    print(
                        'The password you entered for the file is incorrect. Please check and retry.'
                    )
                    input('Press ENTER to continue...')
            else:
                input('Invalid file selected. Enter to continue.')
        else:
            raise Exception('Nothing to be done.')
    except:
        print('No one made any request to you yet! Nothing to be done here.')
        input('Press ENTER to continue...')
        return 0


def file_submenu(chosen_file):
    clearConsole()
    file_name = chosen_file['file_name'].replace('<dot>', '.')
    req_display_name = chosen_file['req_display_name']
    remarks = chosen_file['remarks']
    print(
        f'What do you want to do with {file_name} requested by {req_display_name}'
    )
    print(f'Message from requester: \n{remarks}\n')
    print('1. Approve')
    print('2. Reject')
    print('3. Do nothing')

    option = int(input('Enter your choice: '))
    if option == 1:
        password = input('Enter the password for the file:')
        return process_request(chosen_file, True, password)
    elif option == 2:
        return process_request(chosen_file, False, '')
    else:
        dwnl_reqst_page()


def dwload_file_page():
    clearConsole()
    print('=-=-=-=-=-=-=-=-| Approved downloads |-=-=-=-=-=-=-=-=\n')

    try:
        files = get_dwnls()

        if len(files) > 0:
            i = 1
            selectable_indexes = []
            dwnl_table = PrettyTable(['i', 'File Name', 'Approval Status'])

            for file_name, file_info in files.items():
                approval_status = file_info['approval_status']
                dwnl_table.add_row(
                    [str(i),
                     file_name.replace('<dot>', '.'), approval_status])

                if approval_status == 'APPROVED':
                    selectable_indexes.append(i)

                i = i + 1

            print(dwnl_table)

            if len(selectable_indexes) > 0:
                file_selection = int(
                    input('Enter file number (i) to be downloaded:\t'))

                if file_selection in selectable_indexes:
                    dest_dir = input('Enter destination directory:\t').strip(
                        '"')

                    file = list(files.items())[file_selection - 1]

                    print(secure_download(file, dest_dir))
                    input('Enter to continue...')
                else:
                    print(
                        'Invalid input. Please wait for owner to approve the requests.'
                    )
                    input('Enter to continue...')
            else:
                input(
                    'Nothing to do here, please wait for approvals. Press ENTER to continue...'
                )
        else:
            print(
                '\nNothing to display. Please make a file download requests first.'
            )
            input('Enter to continue...')

    except:
        input('No entries found. Press ENTER to continue...')
        return 0


def signout_page():
    select = input('Confirm sign out? Y/n\t').upper()

    if select == 'Y':
        auth.signout()
        input('Signed out. Press ENTER to continue...')
        return 0
    elif select == 'N':
        return 0
    else:
        print('Invalid input.')
        return signout_page()
