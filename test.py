from backend import globals
from backend.controllers.auth_controller import AuthManager
from backend.controllers.data_controller import DataManager

globals.init()
auth = AuthManager()

auth.signin('abc@gmail.com', '123asd')

idToken = globals.AUTH_USER['localId']
