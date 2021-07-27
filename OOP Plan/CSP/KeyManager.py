# imports..
# import paillier library etc
import pathlib
import sys
path = str(pathlib.Path.cwd().parents[2])
sys.path.append(path + '\\Crypte\\Lab Paillier')
import lab_paillier
import pickle

class KeyManager():
    def __init__(self):
        self.generate_keys() # Generate keys
        self.public_key = self.__read_public_key() # Read the public key and store it in the object
        self.private_key = self.__read_private_key()# Read the private key and store it in the object
        # Any other constructor logic required etc...

    def generate_keys(self):
        public_key, private_key = lab_paillier.generate_lab_paillier_keypair() 
        self.__write_public_key(public_key)
        self.__write_private_key(private_key)

    def __read_public_key(self):
        with open(path + '\\Crypte\\Public_Key\\public_key', 'rb') as public_key_file:
            return pickle.load(public_key_file)

    def __read_private_key(self):
        with open(path + '\\Crypte\\CSP\\private_key', 'rb') as private_key_file:
            return pickle.load(private_key_file)

    def __write_public_key(self, public_key):
        with open(path + '\\Crypte\\Public_Key\\public_key', 'wb') as public_key_file:
            pickle.dump(public_key, public_key_file)

    def __write_private_key(self, private_key):
        with open(path + '\\Crypte\\CSP\\private_key', 'wb') as private_key_file:
            pickle.dump(private_key, private_key_file)
    

