from typing import List
from backend import globals
from backend.implementations import RSA
globals.init()

plaintext = 'this is for testing!'
list = RSA.generateKey()
print(list)
RSA.storePrivateKey(list[0],'test')
# ciphertext = RSA.encryptRSA(list[1], plaintext)
# print('Cipher text is ' + str(ciphertext))
# decrypttext = RSA.decryptRSA(list[0],ciphertext)
# print('Decrypted msg is ' + str(decrypttext))

