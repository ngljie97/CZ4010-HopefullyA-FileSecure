# Console base client application view
# To process data output and input

import os
import time

from backend import globals
from backend.controllers.client_controller import get_dwnls, get_all_files, FileMeta, request_download, get_file_requests, process_request, secure_download, secure_send


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


def cred_prompt():
    user_email = input('Enter your email:\t')
    user_passw = input('Enter your password:\t')
    return (user_email, user_passw)


def user_menu():
    clearConsole()
    user = globals.AUTH_USER['email']
    print(f'Logged in as: {user}')
    print('1. Upload a file.')
    print('2. Request file download.')
    print('3. View download requests.')
    print('4. View downloadable files.')
    print('5. Logout.')
    return input('Enter your choice:\t')


def upload_file_page():
    clearConsole()
    file_location = input('Enter the full directory to the file:\t')
    encryption_key = input('Enter a passkey for the encryption:\t')
    print(secure_send(file_location, encryption_key))


def request_file_page():
    print('List of files:')
    entries = get_all_files()

    data = []
    i = 1

    for user, files in entries.items():
        for file_name, file_info in files.items():
            file = FileMeta()
            file.file_name = file_name
            file.uploader_id = user
            file.uploader_name = file_info['display_name']
            file.file_size = file_info['filesize']

            data.append(file)
            print(
                f'{str(i)}. {file.file_name}\t uploaded by {file.uploader_name}'
            )

            i = i + 1

    if len(data) > 0:
        select = int(
            input('Enter file to download (the number on the left):\t'))
        if 0 <= (select - 1) < len(data):
            selected_file = data[select - 1]
            remarks = input(
                'Enter a message to display for the owner of the file to approve your resquest (WARNING: do not enter any personal information/credentials):\n'
            )
            selected_file.remarks = remarks
            print(request_download(selected_file))
    else:
        print('No files to download. Exitting..')


def dwnl_reqst_page():
    clearConsole()
    print('Here are the lists of file requests made to you:')
    print('i\tFile\tRequested by\tApproval Status\t')
    entries = get_file_requests()

    if len(entries) < 1:
        print('\nNothing to display here. Returning...\n')

    else:
        i = 1
        for entry in entries:
            file_name = entry['file_name']
            req_display_name = entry['req_display_name']
            approval_status = entry['approval_status']
            print(
                f'{str(i)}\t{file_name}\t{req_display_name}\t{approval_status}'
            )
            i = i + 1

        sel = input('Enter a file number(i) for more options:\t')
        if 0 <= int(sel) - 1 < len(entries):
            message = file_submenu(entries[int(sel) - 1])
            if message == 'SUCCESS':
                print('The requests has been approved successfully.')
            elif message == 'REJECTED':
                print('The requests has been approved successfully.')
            elif message == 'WRONG_PASSWORD':
                print(
                    'The password you entered for the file is incorrect. Please check and retry.'
                )
        else:
            print('Invalid file selected.')

    time.sleep(2)
    return 0


def file_submenu(chosen_file):
    clearConsole()
    file_name = chosen_file['file_name']
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
    print('List of files:')
    print('i\tFile Name\tAprroval Status')
    files = get_dwnls()

    if len(files) > 0:
        i = 1
        selectable_indexes = []

        for file_name, file_info in files.items():
            approval_status = file_info['approval_status']
            print(f'{str(i)}\t{file_name}\t{approval_status}')
            if approval_status:
                selectable_indexes.append(i)
            i = i + 1

        if len(selectable_indexes) > 0:
            file_selection = int(
                input('Enter file number (i) to be downloaded:\t'))

            if file_selection in selectable_indexes:
                dest_dir = input('Enter destination directory:\t')

                file = list(files.items())[file_selection - 1]

                print(secure_download(file, dest_dir))
            else:
                print(
                    'Invalid input. Please wait for owner to approve the requests.'
                )
    else:
        print(
            '\nNothing to display. Please make a file download requests first.'
        )

    time.sleep(2)
