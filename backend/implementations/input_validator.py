import re
import os


# Source: https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/
def check_email(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    if (re.fullmatch(regex, email)):
        return True
    else:
        print("Invalid Email")
        return False


def check_password(password):
    length = True
    complexity = True

    if len(password) < 8:
        print('[x] Password should be at least 6 characters.')
        length = False

    if not re.search("[_@$!]", password):
        print('[x] Password should contains at least one @ or _ or $ or !.')
        complexity = False

    if not re.search("[a-z]", password):
        print(
            '[x] Password should contains at least one lower case character.')
        complexity = False

    if not re.search("[A-Z]", password):
        print(
            '[x] Password should contains at least one UPPER case character.')
        complexity = False

    if not re.search("[0-9]", password):
        print('[x] Password should contains at least one numeric character.')
        complexity = False

    return (length and complexity)


def check_file(path):
    if (os.path.isdir(path)):
        print('[x] Input path is a directory.')

    return os.path.isfile(path)