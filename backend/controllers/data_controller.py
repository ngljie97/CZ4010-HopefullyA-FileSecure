import json
from datetime import datetime

from backend import globals
from backend.implementations.aescipher import AESCipher
from backend.implementations.RSA import *
# Database Controller class which manages the database operations.


class DataManager(object):
    def __init__(self):
        global db
        db = globals.FIREBASE_CONN.database()

    """ 
    Inserts a new entry into the database.
        user_id     :   Id of the user performing the action.
        file_name   :   The name of the file for the operation.
        file_size   :   Size of the original file.
    """

    def insert_upload_entry(self, user_id, file_name, file_size, display_name,
                            hashedkey):

        # Current date time in local system.
        timestamp = datetime.now()

        file_name = file_name.replace('.', '_')

        # Checks if file with same name exists.
        if self.entry_exist(key_1=user_id, key_2=file_name):
            return 'FILE_EXISTS'
        else:
            data = {
                "filesize": file_size,
                "display_name": display_name,
                "timestamp": str(timestamp),
                "hashed_key": hashedkey
            }

            db.child('UPLOAD').child(user_id).child(file_name).set(data)

            return 'SUCCESS'

    """ 
    Inserts a new entry into the database.
        user_id     :   Id of the user performing the action.
        file_name   :   The name of the file for the operation.
        uploader_id :   Id of the user that uploaded the said file.
        file_size   :   Size of the original file.
    """

    def insert_download_request(self, user_id, file_name, uploader_id,
                                file_size, remarks):
        # Current date time in local system.
        timestamp = datetime.now()
        req_display_name = globals.AUTH_USER['email'].split('@')[0]
        file_name = file_name.replace('.', '_')
        if (self.entry_exist(uploader_id, file_name)):
            if self.entry_exist(user_id, file_name, uploader_id):
                return 'Request was previously made, please check if it has already been approved.'
            else:
                data = {
                    'uploader_id': uploader_id,
                    'file_size': file_size,
                    'timestamp': str(timestamp),
                    'remarks': remarks,
                    'approval_status': 'WAITING',
                    'req_display_name': req_display_name,
                    'exchange_secret': '',
                }

                db.child('DOWNLOAD').child(user_id).child(file_name).set(data)

                return 'Successfully requested for file. Please wait for the owner to approve.'
        else:
            return 'Requested file is no longer in the server.'

     # Insert public key
    def insert_public_key(self, user_id, public_key):

        db.child('PUBLICKEY').child(user_id).set(public_key)

        return 1

    def get_all_files(self):

        return db.child('UPLOAD').get().val()

    def get_uploaded_files(self, user_id):

        return db.child('UPLOAD').child(user_id).get().val()

    def get_requested_files(self):

        cur_user = globals.AUTH_USER['localId']
        files = db.child('DOWNLOAD').child(cur_user).get().val()
        return files

    def get_file_requests(self):

        cur_user = globals.AUTH_USER['localId']
        entries = db.child('DOWNLOAD').get().val()

        my_requests = []

        for requester, requests in entries.items():
            for file_name, request_info in requests.items():
                if request_info['uploader_id'] == cur_user:
                    my_requests.append({
                        'requester':
                        requester,
                        'file_name':
                        file_name,
                        'remarks':
                        request_info['remarks'],
                        'req_display_name':
                        request_info['req_display_name'],
                        'uploader_id':
                        request_info['uploader_id'],
                        'approval_status':
                        request_info['approval_status'],
                        'exchange_secret':
                        request_info['exchange_secret']
                    })

        return my_requests

    def process_approval(self, request_info, approval, password):

        file_hashed_pass = db.child('UPLOAD').child(
            request_info['uploader_id']).child(
                request_info['file_name']).child('hashed_key').get().val()

        if approval:
            cipher = AESCipher(password=password)
            hashed_password = cipher.getKeyHash()

            if (file_hashed_pass == hashed_password):
                data = db.child('DOWNLOAD').child(
                    request_info['requester']).child(
                        request_info['file_name']).get().val()
                data['approval_status'] = 'APPROVED'

                # Perform encryption of the password using asymetric key encryption using the requester public key (minimally)

                # @Joel this portion needs your input
                public_key = db.child('PUBLICKEY').child(
                    request_info['requester']).get().val()
                public_key = bytes(public_key, 'utf-8')    
                # encrypt this 'password' @Joel
                exchange_secret = encryptRSA(public_key, password)

                # ---------------------------------------------

                data['exchange_secret'] = exchange_secret.hex()

                db.child('DOWNLOAD').child(request_info['requester']).child(
                    request_info['file_name']).update(data)

                return 'APPROVED'
            else:
                return 'WRONG_PASSWORD'

        else:
            db.child('DOWNLOAD').child(request_info['requester']).child(
                request_info['file_name']).child(
                    request_info['approval_status']).update('REJECTED')
            return 'REJECTED'

    def entry_exist(self, key_1, key_2, key_3=0):

        if key_3 == 0:
            entry = db.child('UPLOAD').child(key_1).get().val()
            try:
                if len(entry) > 0:
                    return (len(entry[key_2]) > 0)
                else:
                    return False
            except:
                return False
        else:
            entry = db.child('DOWNLOAD').child(key_1).get().val()
            try:
                if len(entry) > 0:
                    return entry[key_2]['uploader_id'] == key_3
                else:
                    return False
            except:
                return False
