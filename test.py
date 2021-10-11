from backend import globals
from backend.implementations import RSA
globals.init()

list = generateKey()
print(list)
storePrivateKey(list[0],'test')
