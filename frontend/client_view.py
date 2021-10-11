# Console base client application view

import os


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
    return input('Enter your choice:\t')


def cred_prompt():
    user_email = input('Enter your email:\t')
    user_passw = input('Enter your password:\t')
    return (user_email, user_passw)


def user_menu():
    print('1. Upload a file.')
    print('2. Download a file.')
    print('3. View file requests.')
    return input('Enter your choice:\t')


def upload_file_page():
    file_location = input('Enter the full directory to the file:\t')
    encryption_key = input('Enter a passkey for the encryption:\t')
    return (file_location, encryption_key)


def dwload_file_page():
    print('')