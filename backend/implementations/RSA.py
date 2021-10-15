from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from backend import globals as globals
# from diffiehellman import publicKey
import os

pk_file_name = 'file name pk'
# Generating key (Public key to be stored in database, private key stored in client machine)
def generateKey():
    key_list = []
    private_key = rsa.generate_private_key(public_exponent=65537,
                                           key_size=2048,
                                           backend=default_backend())
    public_key = private_key.public_key()
    key_list.append(private_key)
    key_list.append(public_key)
    return key_list


# Storing key
def storePrivateKey(private_key, key_name):
    
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption())
    key_name = key_name +'.pem'

    with open(globals.PROJ_ROOT + '\\privatekey\\' + key_name, 'wb') as x: 
        x.write(pem)

    return

def storePublicKey(public_key):
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo)

    with open('public_key.pem', 'wb') as f:
        f.write(pem)


# Getting keys
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
    cipher_text = public_key.encrypt(
        message,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                     algorithm=hashes.SHA256(),
                     label=None))
    return cipher_text


# Decrypt
def decryptRSA(private_key, cipher_text):
    plain_text = private_key.decrypt(
        cipher_text,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                     algorithm=hashes.SHA256(),
                     label=None))
    return plain_text

