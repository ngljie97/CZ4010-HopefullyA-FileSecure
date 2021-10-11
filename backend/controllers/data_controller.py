import json
from datetime import datetime

from backend import globals

# Database Controller class which manages the database operations.


class DataManager:
    def __init__(self):
        global db
        db = globals.FIREBASE_CONN.database()

    """ 
    Inserts a new entry into the database.
        user_id     :   Id of the user performing the action.
        file_name   :   The name of the file for the operation.
        file_size   :   Size of the original file.
    """

    def insert_upload_entry(self, user_id, file_name, file_size):
        # Current date time in local system.
        timestamp = datetime.now()

        table = db.child('UPLOAD')

        # Checks if file with same name exists.
        if self.entry_exist(key_1=user_id, key_2=file_name):
            return 'FILE_EXISTS'
        else:
            data = {"filesize": file_size, "timestamp": timestamp}

            table.child(user_id).child(file_name).push(data)

            return 'SUCCESS'

    """ 
    Inserts a new entry into the database.
        user_id     :   Id of the user performing the action.
        file_name   :   The name of the file for the operation.
        uploader_id :   Id of the user that uploaded the said file.
        file_size   :   Size of the original file.
    """

    def insert_download_request(self, user_id, file_name, uploader_id,
                                file_size):
        # Current date time in local system.
        timestamp = datetime.now()

        table = db.child('DOWNLOAD')

        if self.entry_exist(user_id, file_name, uploader_id):
            return 'DUPLICATE_REQUEST'
        else:
            data = {
                'uploader_id': uploader_id,
                'file_size': file_size,
                'timestamp': timestamp
            }

            table.child(user_id).child(file_name).push(data)

            return 'SUCCESS'

    def entry_exist(self, key_1, key_2, key_3=0):
        entry = json.load(self.get_file_uploaded_by_user(user_id=key_1))

        if key_3 == 0:
            return entry.has_key(key_2)
        else:
            return entry[key_2]['uploader_id'] == key_3

    def get_file_uploaded_by_user(self, user_id):
        table = db.child('UPLOAD')

        return table.get(user_id)


globals.init()
dbcon = DataManager()

print(dbcon.insert_upload_entry('abc', '123.txt', 199))
