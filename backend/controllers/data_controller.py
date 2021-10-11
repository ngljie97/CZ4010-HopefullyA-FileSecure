import json
from datetime import datetime

from backend import globals
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

    def insert_upload_entry(self, user_id, file_name, file_size, display_name):
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
                "timestamp": str(timestamp)
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

        file_name = file_name.replace('.', '_')
        if (self.entry_exist(uploader_id, file_name)):
            if self.entry_exist(user_id, file_name, uploader_id):
                return 'DUPLICATE_REQUEST'
            else:
                data = {
                    'uploader_id': uploader_id,
                    'file_size': file_size,
                    'timestamp': str(timestamp),
                    'remarks': remarks,
                    'approval_status': False,
                    'exchange_secret': ''
                }

                db.child('DOWNLOAD').child(user_id).child(file_name).set(data)

                return 'SUCCESS'
        else:
            return 'FILE_NOT_FOUND'

    def approve_request():
        return 0

    def reject_request():
        return 0

    def get_uploaded_files(user_id):

        return 0

    def get_requested_files():
        return 0

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