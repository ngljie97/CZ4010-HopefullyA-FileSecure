from backend import globals
from backend.controllers import server_controller
import os

globals.init()

server_dir = 'C:\\CZ4010\\backend\\server\\'
if not os.path.exists(server_dir):
    os.makedirs(server_dir)

server_controller.start_server()