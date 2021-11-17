import json
from backend.controllers.data_controller import DataManager
from backend.implementations.RSA import generatePublicKey
from backend import globals

# from backend.implementations import RSA


class AuthManager(object):
    def __init__(self):
        global auth
        auth = globals.FIREBASE_CONN.auth()

    def signup(self, email, password):
        try:
            user = auth.create_user_with_email_and_password(email, password)
            # auth.send_email_verification(user['idToken'])
            
        except Exception as e:
            error_json = e.args[1]
            error = json.loads(error_json)['error']
            return 'Sign up failed with error: ' + error['message']
        try:
            userid = user['localId']
            public_key = generatePublicKey(userid)
            db_controller = DataManager()
            db_controller.insert_public_key(userid, public_key)
        except Exception as e:
            print(e)
            
        return 'Succesfully created an account with ' + email

    def signin(self, email, password):
        try:
            globals.AUTH_USER = auth.sign_in_with_email_and_password(
                email, password)

            globals.IS_AUTHENTICATED = True

            return 'Successfully signed in as ' + email

        except Exception as e:
            error_json = e.args[1]
            error = json.loads(error_json)['error']
            return 'Sign in failed with error: ' + error['message']

    def signout(self):
        globals.IS_AUTHENTICATED = False
        globals.AUTH_USER = {}

    def refresh_session(self):
        globals.AUTH_USER = auth.refresh(globals.AUTH_USER['refreshToken'])

    def reset_password(self, email):
        auth.send_password_reset_email(email)