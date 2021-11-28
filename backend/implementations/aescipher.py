# cryptographic tools
import hashlib
from Crypto.Cipher import AES
from Crypto.Hash import SHA512
from Crypto import Random
from Crypto.Protocol.KDF import PBKDF2


# implementation of AES256 symmetric key encryption for file encryption.
class AESCipher(object):
    def __init__(self, password):
        salt = '?4H-nUw_1GaG0t0I'
        self.key = PBKDF2(password,
                          salt,
                          32,
                          count=1000000,
                          hmac_hash_module=SHA512)

    def destroy(self):
        self.key = PBKDF2('0123456789',
                          '9876543210123122',
                          32,
                          count=1000000,
                          hmac_hash_module=SHA512)

    def encrypt(self, file):
        nonce = Random.new().read(AES.block_size)

        cipher = AES.new(self.key, AES.MODE_EAX, nonce=nonce)

        with open(file, 'rb') as f:
            input = f.read()
            ciphertext, tag = cipher.encrypt_and_digest(input)

        out_file = file + '.enc'

        with open(out_file, 'wb') as f:
            f.write(nonce + tag + ciphertext)

        return out_file

    def decrypt(self, enc_file):
        with open(enc_file, 'rb') as f:
            nonce = f.read(16)
            tag = f.read(16)
            ciphertext = f.read()

        cipher = AES.new(self.key, AES.MODE_EAX, nonce=nonce)

        data = cipher.decrypt_and_verify(ciphertext, tag)

        out_file = enc_file[:-4]

        with open(out_file, 'wb') as f:
            f.write(data)

        return out_file

    def getKeyHash(self):
        hash_md5 = hashlib.md5()
        hash_md5.update(self.key)

        return hash_md5.hexdigest()


def stringHash(string):
    out = hashlib.md5()
    salt = '1eVeflPhacHiklphEP7*$aMahoXlpH-?'
    out.update(string.encode())
    out.update(salt.encode())

    return out.hexdigest()
