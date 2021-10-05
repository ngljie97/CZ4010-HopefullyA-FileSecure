# basic libraries
import globals
import base64

# cryptographic tools
import hashlib
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Util.Padding import pad, unpad
from Crypto.Protocol.KDF import PBKDF2


class AESCipher(object):

    def __init__(self):
        self.key = 's$lphuTr?43&*u-eNlv*@+3re8!o5hi2H!1u5rus5op4asp1Bu&6C3Wr33?l-rEk'
        self.salt = 'S=ad7eT+Z6TaDRL_'

    def nonce_from_OTP(self, otp):  # Generate a nonce using a time based OTP using SHA256
        m = hashlib.sha256()
        m.update(globals.USER_TOKEN)
        m.update(otp)

        return m.digest()

    def encrypt(self, file, otp):  # Encrypt file in CTR mode with AES
        iv = self.nonce_from_OTP(otp)
        cipher = AES.new(self.key, AES.MODE_CTR, iv)
        raw = pad(file, AES.block_size)
        ciphertext, tag = cipher.encrypt_and_digest(raw)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(enc[16:]))
