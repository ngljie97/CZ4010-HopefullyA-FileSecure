# basic libraries  
import base64

# cryptographic tools
import hashlib
from Crypto.Cipher import AES

class AESCipher(object):

    def __init__(self):
        self.key = 's$lphuTr?43&*u-eNlv*@+3re8!o5hi2H!1u5rus5op4asp1Bu&6C3Wr33?l-rEk'

    def nonce_from_OTP(self, otp):
        m = hashlib.sha256()
        m.update(otp)

        return m.digest()

    def encrypt(self, raw):
        raw = pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(enc[16:]))
