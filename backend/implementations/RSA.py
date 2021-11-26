from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from backend import globals as globals
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA512
# from diffiehellman import publicKey
import os


# Generating key (Public key to be stored in database, private key stored in client machine)


def generatePublicKey(key_name):

    private_key = rsa.generate_private_key(public_exponent=65537,
                                           key_size=2048,
                                           backend=default_backend())
    public_key = private_key.public_key()
    # Store the private key into pem file
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption())
    key_name = key_name + '.pem'
    path = 'C:\\CZ4010\\privatekey\\'
    if not os.path.exists(path):
        os.makedirs(path)
    with open(path + key_name, 'wb') as x:
        x.write(pem)

    # key_list.append(private_key)
    # key_list.append(public_key)
    # return key_list
    publicKey = (public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo)).decode('utf-8')
    return publicKey


# Storing key (Examples Only)
def storePrivateKey(private_key, key_name):

    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption())
    key_name = key_name + '.pem'

    with open(globals.PROJ_ROOT + '\\privatekey\\' + key_name, 'wb') as x:
        x.write(pem)

    return


def storePublicKey(public_key):
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo)

    with open('public_key.pem', 'wb') as f:
        f.write(pem)


# Getting keys (Examples Only)
def getPrivateKey(key_name):
    with open(globals.PROJ_ROOT + '\\privatekey\\' + key_name, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(), password=None, backend=default_backend())
    return private_key


def getPublicKey():
    with open("public_key.pem", "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(), backend=default_backend())
    return public_key


# Encrypting
def encryptRSA(public_key, message):
    message = bytes(message, 'utf-8')
    public_key = serialization.load_pem_public_key(
        public_key, backend=default_backend())
    cipher_text = public_key.encrypt(
        message,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                     algorithm=hashes.SHA256(),
                     label=None))
    return cipher_text


# Decrypt
def decryptRSA(key_name, cipher_text):
    # Retrieve the value of private key
    with open('C:\\CZ4010\\privatekey\\' + key_name + '.pem', "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(), password=None, backend=default_backend())

    # Decrypting...
    plain_text = private_key.decrypt(
        cipher_text,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                     algorithm=hashes.SHA256(),
                     label=None))
    return plain_text
