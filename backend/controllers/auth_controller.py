import json
import pyrebase
from backend import globals


class AuthManager:
    def __init__(self):
        global auth

        seviceAccount = globals.PROJ_ROOT + '\\backend\\secret\\firebase-privatekey.json'
        config = {
            "apiKey": "AIzaSyBd9GRTbL_lIZyJtpQkUfvGwfXmzwuDszc",
            "authDomain": "cz4010fs.firebaseapp.com",
            "databaseURL":
            "https://cz4010fs-default-rtdb.asia-southeast1.firebasedatabase.app/",
            "storageBucket": "cz4010fs.appspot.com",
            "serviceAccount": seviceAccount
        }

        firebase = pyrebase.initialize_app(config)
        auth = firebase.auth()

    def signup(self, email, password):
        try:
            user = auth.create_user_with_email_and_password(email, password)
            # auth.send_email_verification(user['idToken'])

        except Exception as e:
            error_json = e.args[1]
            error = json.loads(error_json)['error']
            return 'Sign up failed with error: ' + error['message']

        return user['idToken']

    def signin(self, email, password):
        try:
            globals.AUTH_USER = auth.sign_in_with_email_and_password(
                email, password)

            globals.IS_AUTHENTICATED = True

            return 'Successfully signed in as ' + globals.AUTH_USER['localId']

        except Exception as e:
            error_json = e.args[1]
            error = json.loads(error_json)['error']
            return 'Sign in failed with error: ' + error['message']

    def signout(self):
        globals.IS_AUTHENTICATED = False
        globals.AUTH_USER = {}

    def refresh_session():
        globals.AUTH_USER = auth.refresh(globals.AUTH_USER['refreshToken'])

    def reset_password(self, email):
        auth.send_password_reset_email(email)